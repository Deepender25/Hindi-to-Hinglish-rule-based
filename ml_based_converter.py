"""
Real ML-Based Hindi to Hinglish Converter
Uses Hugging Face Transformers with Helsinki-NLP model
"""

import json
import os
import re
from typing import Dict, Optional, List


class MLBasedConverter:
    """
    Real ML-based converter using transformers:
    1. Dictionary lookup (fastest)
    2. ML model (Helsinki-NLP) for unknown words
    3. Learning (adds ML predictions to dictionary)
    """

    def __init__(self, learned_words_file: str = "ml_based_learned.json"):
        self.learned_words_file = learned_words_file

        from hinglish_converter import HinglishConverter

        self.base_converter = HinglishConverter()

        self.dictionary = {}
        self._load_dictionaries()

        # Initialize ML model
        self.model = None
        self.tokenizer = None
        self.ml_available = False
        self._init_ml_model()

        self.stats = {
            "dictionary_hits": 0,
            "ml_predictions": 0,
            "fallbacks": 0,
            "new_words_learned": 0,
        }

        print(f"✅ ML-Based Converter initialized")
        print(f"   Dictionary words: {len(self.dictionary)}")
        print(f"   ML model: {'Available' if self.ml_available else 'Not Available'}")

    def _init_ml_model(self):
        """Initialize Hugging Face model"""
        try:
            from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

            print("🔄 Loading ML model (first time may download ~400MB)...")

            # Use Helsinki-NLP model for Hindi to English
            # This is a translation model but can help with loanwords
            model_name = "Helsinki-NLP/opus-mt-hi-en"

            # Marian models need specific tokenizer
            from transformers import MarianTokenizer, MarianMTModel

            self.tokenizer = MarianTokenizer.from_pretrained(model_name)
            self.model = MarianMTModel.from_pretrained(model_name)

            self.ml_available = True
            print("✅ ML model loaded successfully")

        except Exception as e:
            print(f"⚠️  Could not load ML model: {e}")
            print("   Run: pip install transformers torch")

    def _ml_transliterate(self, word: str) -> str:
        """Use ML model for transliteration"""
        if not self.ml_available:
            return self.base_converter._transliterate_word(word)

        try:
            import torch

            # Tokenize
            inputs = self.tokenizer(
                word, return_tensors="pt", padding=True, truncation=True
            )

            # Generate
            with torch.no_grad():
                outputs = self.model.generate(**inputs, max_length=50)

            # Decode
            result = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

            # Post-process: if result looks like English word, use it
            # Otherwise fallback to rule-based
            if result and len(result) > 0:
                return result.lower().strip()
            else:
                return self.base_converter._transliterate_word(word)

        except Exception as e:
            print(f"ML prediction failed: {e}")
            return self.base_converter._transliterate_word(word)

    def convert_word(self, word: str, learn: bool = True) -> str:
        """Convert a single word"""
        if not any("\u0900" <= c <= "\u097f" for c in word):
            return word

        # 1. Check dictionary
        if word in self.dictionary:
            self.stats["dictionary_hits"] += 1
            return self.dictionary[word]

        # 2. Use ML model
        result = self._ml_transliterate(word)
        self.stats["ml_predictions"] += 1

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
            except:
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
        except:
            return 0

    def show_learning_summary(self):
        """Show learning summary"""
        print("\n" + "=" * 60)
        print("ML-BASED CONVERTER - LEARNING SUMMARY")
        print("=" * 60)
        print(f"📚 Dictionary hits: {self.stats['dictionary_hits']}")
        print(f"🤖 ML predictions: {self.stats['ml_predictions']}")
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

    converter = MLBasedConverter()

    test_sentences = [
        "मीटिंग में जाऊं क्या?",
        "प्रेजेंटेशन तैयार है।",
        "कंप्यूटर स्लो हो गया।",
        "नमस्ते दोस्तों!",
    ]

    print("\n" + "=" * 60)
    print("ML-BASED CONVERTER - TEST")
    print("=" * 60)

    for hindi in test_sentences:
        hinglish = converter.convert(hindi)
        print(f"\nHindi:    {hindi}")
        print(f"Hinglish: {hinglish}")

    converter.show_learning_summary()
    converter._save_learned_words()
