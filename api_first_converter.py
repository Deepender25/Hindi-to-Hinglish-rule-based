"""
API-First Hindi to Hinglish Converter
Uses Google Translate API (hi-Latn) for ALL unknown words
Falls back to rule-based only if API fails
"""

import json
import os
import re
from typing import Dict, Optional, List


class APIFirstConverter:
    """
    API-First converter:
    1. Dictionary lookup (fastest)
    2. Google Translate API (hi-Latn) for ALL unknown words
    3. Fallback to rule-based only if API fails
    4. Learning (adds all predictions to dictionary)
    """

    def __init__(self, learned_words_file: str = "api_first_learned.json"):
        self.learned_words_file = learned_words_file

        from hinglish_converter import HinglishConverter

        self.base_converter = HinglishConverter()

        self.dictionary = {}
        self._load_dictionaries()

        # Initialize translator
        self.translator = None
        self.api_available = False
        self._init_translator()

        self.stats = {
            "dictionary_hits": 0,
            "api_success": 0,
            "api_failed": 0,
            "fallbacks": 0,
            "new_words_learned": 0,
        }

        print(f"✅ API-First Converter initialized")
        print(f"   Dictionary words: {len(self.dictionary)}")
        print(f"   API available: {self.api_available}")

    def _init_translator(self):
        """Initialize Google Translator"""
        try:
            from googletrans import Translator

            self.translator = Translator()
            self.api_available = True
            print("✅ Google API connected")
        except Exception as e:
            print(f"⚠️  Google API not available: {e}")

    def _load_dictionaries(self):
        """Load dictionaries"""
        self.dictionary.update(self.base_converter.common_words)
        self.dictionary.update(self.base_converter.english_loanwords)
        self.dictionary.update(self.base_converter.compound_words)

        if os.path.exists(self.learned_words_file):
            try:
                with open(self.learned_words_file, "r", encoding="utf-8") as f:
                    learned = json.load(f)
                    self.dictionary.update(learned)
                    print(f"   Loaded {len(learned)} learned words")
            except Exception as e:
                pass

    def _save_learned_words(self):
        """Save learned words"""
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
            return 0

    def _api_transliterate(self, word: str) -> Optional[str]:
        """Use Google API (hi-Latn) for transliteration"""
        if not self.api_available:
            return None

        try:
            # Use hi-Latn for Romanized Hindi
            result = self.translator.translate(word, src="hi", dest="hi-Latn")
            return result.text.lower().strip()
        except Exception as e:
            return None

    def convert_word(self, word: str, learn: bool = True) -> str:
        """Convert a single word - API first approach"""
        if not any("\u0900" <= c <= "\u097f" for c in word):
            return word

        # 1. Check dictionary
        if word in self.dictionary:
            self.stats["dictionary_hits"] += 1
            return self.dictionary[word]

        # 2. Try API for ALL unknown words
        api_result = self._api_transliterate(word)
        if api_result:
            self.stats["api_success"] += 1
            result = api_result
        else:
            # 3. Fallback to rule-based only if API fails
            self.stats["fallbacks"] += 1
            result = self.base_converter._transliterate_word(word)

        # Learn the word
        if learn:
            self.dictionary[word] = result
            self.stats["new_words_learned"] += 1

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
        """Convert multiple texts"""
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
        print("API-FIRST CONVERTER - LEARNING SUMMARY")
        print("=" * 60)
        print(f"📚 Dictionary hits: {self.stats['dictionary_hits']}")
        print(f"🌐 API success: {self.stats['api_success']}")
        print(f"❌ API failed: {self.stats['api_failed']}")
        print(f"📏 Fallbacks: {self.stats['fallbacks']}")
        print(f"📝 New words learned: {self.stats['new_words_learned']}")
        print(f"📖 Total dictionary size: {len(self.dictionary)}")
        print("=" * 60)


if __name__ == "__main__":
    import sys
    import io

    if sys.platform == "win32":
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

    converter = APIFirstConverter()

    test_sentences = [
        "मीटिंग में जाऊं क्या?",
        "प्रेजेंटेशन तैयार है।",
        "कंप्यूटर स्लो हो गया।",
        "नमस्ते दोस्तों!",
        "आज बहुत खुशी हो रही है।",
    ]

    print("\n" + "=" * 60)
    print("API-FIRST CONVERTER - TEST")
    print("=" * 60)

    for hindi in test_sentences:
        hinglish = converter.convert(hindi)
        print(f"\nHindi:    {hindi}")
        print(f"Hinglish: {hinglish}")

    converter.show_learning_summary()
    converter._save_learned_words()
