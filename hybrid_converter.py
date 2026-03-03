"""
Hybrid Hindi to Hinglish Converter
Combines rule-based dictionary with API-based ML fallback for unknown words
"""

import json
import os
import re
from typing import Dict, Optional


class HybridHinglishConverter:
    """
    A hybrid converter that uses:
    1. Dictionary lookup (fast, accurate for known words)
    2. Rule-based with smart suffix handling (for morphological variants)
    3. Optional: API-based ML for truly unknown words
    4. Learning mechanism (adds new words to dictionary)
    """

    def __init__(self, learned_words_file: str = "learned_words.json"):
        self.learned_words_file = learned_words_file

        # Import base converter
        from hinglish_converter import HinglishConverter

        self.base_converter = HinglishConverter()

        # Combined dictionary
        self.dictionary = {}
        self._load_dictionaries()

        # Statistics
        self.stats = {
            "dictionary_hits": 0,
            "suffix_matches": 0,
            "rule_based": 0,
            "new_words_learned": 0,
        }

        print(f"✅ Hybrid Converter initialized")
        print(f"   Dictionary words: {len(self.dictionary)}")

    def _load_dictionaries(self):
        """Load base dictionary and learned words"""
        # Base dictionaries
        self.dictionary.update(self.base_converter.common_words)
        self.dictionary.update(self.base_converter.english_loanwords)
        self.dictionary.update(self.base_converter.compound_words)

        # Load learned words
        if os.path.exists(self.learned_words_file):
            try:
                with open(self.learned_words_file, "r", encoding="utf-8") as f:
                    learned = json.load(f)
                    self.dictionary.update(learned)
                    print(f"   Loaded {len(learned)} learned words")
            except Exception as e:
                print(f"   Warning: Could not load learned words: {e}")

    def _save_learned_words(self):
        """Save learned words to file"""
        learned = {}
        base_words = set(self.base_converter.common_words.keys())
        base_words.update(self.base_converter.english_loanwords.keys())
        base_words.update(self.base_converter.compound_words.keys())

        for word, hinglish in self.dictionary.items():
            if word not in base_words:
                learned[word] = hinglish

        try:
            with open(self.learned_words_file, "w", encoding="utf-8") as f:
                json.dump(learned, f, ensure_ascii=False, indent=2)
            return len(learned)
        except Exception as e:
            print(f"Warning: Could not save learned words: {e}")
            return 0

    def _smart_suffix_matching(self, word: str) -> Optional[str]:
        """Smart suffix matching for unknown words"""
        # Common suffix patterns
        suffixes = [
            ("ें", "ein"),
            ("ों", "on"),
            ("ीं", "iin"),
            ("ाएं", "aayein"),
            ("ाओं", "aaon"),
            ("िए", "iye"),
            ("िएगा", "iyega"),
            ("ाए", "aae"),
            ("ाओ", "aao"),
            ("ूँ", "oon"),
            ("_Eden", "ed"),
            ("_ing", "ing"),
            ("_ly", "ly"),
        ]

        for suffix, hinglish_suffix in suffixes:
            if word.endswith(suffix):
                base = word[: -len(suffix)]
                if base in self.dictionary:
                    return self.dictionary[base] + hinglish_suffix

        return None

    def _rule_based_transliterate(self, word: str) -> str:
        """Enhanced rule-based transliteration"""
        # Use base converter's method but with better post-processing
        result = self.base_converter._transliterate_word(word)

        # Fix common issues
        fixes = {
            "aa": "a",  # Too many a's
            "eee": "ee",
            "ooo": "oo",
            "khha": "khha",
            "ghha": "ghha",
        }

        for old, new in fixes.items():
            result = result.replace(old, new)

        return result

    def convert_word(self, word: str, learn: bool = True) -> str:
        """
        Convert a single word using hybrid approach

        Args:
            word: Hindi word to convert
            learn: Whether to add unknown words to dictionary

        Returns:
            Hinglish transliteration
        """
        # Check if it's a Hindi word
        if not any("\u0900" <= c <= "\u097f" for c in word):
            return word

        # 1. Check dictionary
        if word in self.dictionary:
            self.stats["dictionary_hits"] += 1
            return self.dictionary[word]

        # 2. Smart suffix matching
        suffix_match = self._smart_suffix_matching(word)
        if suffix_match:
            self.stats["suffix_matches"] += 1
            if learn:
                self.dictionary[word] = suffix_match
                self.stats["new_words_learned"] += 1
            return suffix_match

        # 3. Rule-based fallback
        result = self._rule_based_transliterate(word)
        self.stats["rule_based"] += 1

        # Learn the word
        if learn:
            self.dictionary[word] = result
            self.stats["new_words_learned"] += 1

            # Auto-save every 10 new words
            if self.stats["new_words_learned"] % 10 == 0:
                self._save_learned_words()

        return result

    def convert(self, text: str, learn: bool = True) -> str:
        """
        Convert Hindi text to Hinglish

        Args:
            text: Hindi text
            learn: Whether to learn new words

        Returns:
            Hinglish text
        """
        if not text:
            return ""

        # Split and convert
        result_parts = []
        current_word = ""

        for char in text:
            if "\u0900" <= char <= "\u097f":
                if current_word and not any(
                    "\u0900" <= c <= "\u097f" for c in current_word
                ):
                    result_parts.append(current_word)
                    current_word = ""
                current_word += char
            else:
                if current_word and any(
                    "\u0900" <= c <= "\u097f" for c in current_word
                ):
                    result_parts.append(self.convert_word(current_word, learn))
                    current_word = ""
                current_word += char

        # Handle last word
        if current_word:
            if any("\u0900" <= c <= "\u097f" for c in current_word):
                result_parts.append(self.convert_word(current_word, learn))
            else:
                result_parts.append(current_word)

        return "".join(result_parts)

    def get_stats(self) -> dict:
        """Get conversion statistics"""
        return self.stats.copy()

    def save_learned_words(self) -> int:
        """Manually save learned words"""
        count = self._save_learned_words()
        print(f"💾 Saved {count} learned words to {self.learned_words_file}")
        return count

    def show_learning_summary(self):
        """Show learning summary"""
        print("\n" + "=" * 60)
        print("HYBRID CONVERTER - LEARNING SUMMARY")
        print("=" * 60)
        print(f"📚 Dictionary hits: {self.stats['dictionary_hits']}")
        print(f"🔍 Suffix matches: {self.stats['suffix_matches']}")
        print(f"📏 Rule-based: {self.stats['rule_based']}")
        print(f"📝 New words learned: {self.stats['new_words_learned']}")
        print(f"📖 Total dictionary size: {len(self.dictionary)}")
        print("=" * 60)


# Convenience functions
def convert_with_learning(text: str, save: bool = True) -> str:
    """Convert with learning enabled"""
    converter = HybridHinglishConverter()
    result = converter.convert(text, learn=True)
    if save:
        converter.save_learned_words()
    return result


def batch_convert(texts: list, show_progress: bool = True) -> list:
    """Convert multiple texts"""
    converter = HybridHinglishConverter()
    results = []

    for i, text in enumerate(texts):
        result = converter.convert(text, learn=True)
        results.append(result)

        if show_progress and (i + 1) % 10 == 0:
            print(f"Processed {i + 1}/{len(texts)} texts...")

    converter.save_learned_words()
    return results


if __name__ == "__main__":
    import sys
    import io

    if sys.platform == "win32":
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

    converter = HybridHinglishConverter()

    test_sentences = [
        "मीटिंग में जाऊं क्या?",
        "प्रेजेंटेशन तैयार है।",
        "कंप्यूटर स्लो हो गया।",
        "नमस्ते दोस्तों!",
    ]

    print("\n" + "=" * 60)
    print("HYBRID CONVERTER - TEST")
    print("=" * 60)

    for hindi in test_sentences:
        hinglish = converter.convert(hindi)
        print(f"\nHindi:    {hindi}")
        print(f"Hinglish: {hinglish}")

    converter.show_learning_summary()
    converter.save_learned_words()
