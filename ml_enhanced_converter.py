"""
ML-Enhanced Hindi to Hinglish Converter
Uses Google Translate API for high-quality transliteration
Learns from predictions and adds them to dictionary
"""

import json
import os
import re
from typing import Dict, Optional, List


class MLEnhancedConverter:
    """
    ML-Enhanced converter that uses:
    1. Dictionary lookup (fastest - O(1))
    2. Google Translate API (ML-quality for unknown words)
    3. Learning mechanism (adds ML predictions to dictionary)
    """

    def __init__(self, learned_words_file: str = "ml_learned_words.json"):
        self.learned_words_file = learned_words_file

        # Import base converter
        from hinglish_converter import HinglishConverter

        self.base_converter = HinglishConverter()

        # Combined dictionary
        self.dictionary = {}
        self._load_dictionaries()

        # Initialize Google Translator
        self.translator = None
        self.ml_available = False
        self._init_translator()

        # Statistics
        self.stats = {
            "dictionary_hits": 0,
            "ml_predictions": 0,
            "fallbacks": 0,
            "new_words_learned": 0,
        }

        print(f"✅ ML-Enhanced Converter initialized")
        print(f"   Dictionary words: {len(self.dictionary)}")
        print(
            f"   ML (Google API): {'Available' if self.ml_available else 'Not Available'}"
        )

    def _init_translator(self):
        """Initialize Google Translator"""
        try:
            from googletrans import Translator

            self.translator = Translator()
            # Test the translator
            test = self.translator.translate("नमस्ते", src="hi", dest="en")
            self.ml_available = True
            print("✅ Google Translate API connected")
        except Exception as e:
            print(f"⚠️  Google Translate API not available: {e}")
            print("   Falling back to rule-based transliteration")

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
                    print(f"   Loaded {len(learned)} ML-learned words")
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

    def _ml_transliterate(self, word: str) -> str:
        """Use Google Translate API for transliteration with hi-Latn"""
        if not self.ml_available:
            return self.base_converter._transliterate_word(word)

        try:
            # Use hi-Latn for better Romanized Hindi transliteration
            result = self.translator.translate(word, src="hi", dest="hi-Latn")
            return result.text.lower().strip()

        except Exception as e:
            print(f"ML prediction failed for '{word}': {e}")
            return self.base_converter._transliterate_word(word)

        try:
            # Translate Hindi to English (gives transliteration)
            result = self.translator.translate(word, src="hi", dest="en")

            # The result.pronunciation contains the transliteration
            if result.pronunciation:
                return result.pronunciation.lower().strip()
            else:
                # Fallback to text if pronunciation not available
                return result.text.lower().strip()

        except Exception as e:
            print(f"ML prediction failed for '{word}': {e}")
            return self.base_converter._transliterate_word(word)

    def convert_word(self, word: str, learn: bool = True) -> str:
        """
        Convert a single word using ML-enhanced approach
        """
        # Check if it's a Hindi word
        if not any("\u0900" <= c <= "\u097f" for c in word):
            return word

        # 1. Check dictionary
        if word in self.dictionary:
            self.stats["dictionary_hits"] += 1
            return self.dictionary[word]

        # 2. Use ML for unknown words
        if self.ml_available:
            result = self._ml_transliterate(word)
            self.stats["ml_predictions"] += 1
        else:
            # Fallback to rule-based
            result = self.base_converter._transliterate_word(word)
            self.stats["fallbacks"] += 1

        # Learn the word
        if learn:
            self.dictionary[word] = result
            self.stats["new_words_learned"] += 1

            # Auto-save every 5 new words
            if self.stats["new_words_learned"] % 5 == 0:
                self._save_learned_words()

        return result

    def convert(self, text: str, learn: bool = True) -> str:
        """Convert Hindi text to Hinglish"""
        if not text:
            return ""

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

        if current_word:
            if any("\u0900" <= c <= "\u097f" for c in current_word):
                result_parts.append(self.convert_word(current_word, learn))
            else:
                result_parts.append(current_word)

        return "".join(result_parts)

    def batch_convert(
        self, texts: List[str], learn: bool = True, show_progress: bool = True
    ) -> List[str]:
        """Convert multiple texts efficiently"""
        results = []

        for i, text in enumerate(texts):
            result = self.convert(text, learn)
            results.append(result)

            if show_progress and (i + 1) % 10 == 0:
                print(f"  Processed {i + 1}/{len(texts)} texts...")

        if learn:
            self._save_learned_words()

        return results

    def show_learning_summary(self):
        """Show learning summary"""
        print("\n" + "=" * 60)
        print("ML-ENHANCED CONVERTER - LEARNING SUMMARY")
        print("=" * 60)
        print(f"📚 Dictionary hits: {self.stats['dictionary_hits']}")
        print(f"🤖 ML predictions: {self.stats['ml_predictions']}")
        print(f"📏 Fallbacks: {self.stats['fallbacks']}")
        print(f"📝 New words learned: {self.stats['new_words_learned']}")
        print(f"📖 Total dictionary size: {len(self.dictionary)}")
        print("=" * 60)


# Test function
def test_ml_converter():
    """Test the ML converter"""
    import sys
    import io

    if sys.platform == "win32":
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

    converter = MLEnhancedConverter()

    test_sentences = [
        "मीटिंग में जाऊं क्या?",
        "प्रेजेंटेशन तैयार है।",
        "कंप्यूटर स्लो हो गया।",
        "नमस्ते दोस्तों!",
        "इंटरनेट कनेक्शन खराब है।",
    ]

    print("\n" + "=" * 60)
    print("ML-ENHANCED CONVERTER - TEST")
    print("=" * 60)

    for hindi in test_sentences:
        hinglish = converter.convert(hindi)
        print(f"\nHindi:    {hindi}")
        print(f"Hinglish: {hinglish}")

    converter.show_learning_summary()
    converter._save_learned_words()


if __name__ == "__main__":
    test_ml_converter()
