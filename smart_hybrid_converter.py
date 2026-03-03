"""
Smart Hybrid Hindi to Hinglish Converter
Uses rule-based for native Hindi words, API for English loanwords
"""

import json
import os
import re
from typing import Dict, Optional, List


class SmartHybridConverter:
    """
    Smart hybrid converter:
    1. Dictionary lookup (fastest)
    2. Detect English loanwords → use API for correct spelling
    3. Native Hindi words → use rule-based transliteration
    4. Learning (adds all predictions to dictionary)
    """

    def __init__(self, learned_words_file: str = "smart_learned_words.json"):
        self.learned_words_file = learned_words_file

        from hinglish_converter import HinglishConverter

        self.base_converter = HinglishConverter()

        self.dictionary = {}
        self._load_dictionaries()

        # Initialize translator
        self.translator = None
        self.api_available = False
        self._init_translator()

        # Common English patterns in Hindi
        self.english_patterns = [
            r"[एईओउ]|[ंै|ो|ू]",  # English-like vowel combinations
            r"[कपब]्[टडल]",  # Common English consonant clusters
        ]

        self.stats = {
            "dictionary_hits": 0,
            "api_loanwords": 0,
            "rule_based": 0,
            "new_words_learned": 0,
        }

        print(f"✅ Smart Hybrid Converter initialized")
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

    def _is_english_loanword(self, word: str) -> bool:
        """Detect if word is likely an English loanword"""
        # Common English loanword patterns in Hindi
        english_indicators = [
            "मीटिंग",
            "प्रेजेंटेशन",
            "कंप्यूटर",
            "इंटरनेट",
            "मोबाइल",
            "फोन",
            "स्कूल",
            "कॉलेज",
            "हॉस्पिटल",
            "बस",
            "ट्रेन",
            "कार",
            "बैंक",
            "पैसा",
            "रुपया",
            "स्टेशन",
            "एयरपोर्ट",
            "वाईफाई",
            "लैपटॉप",
            "टेबल",
            "चेयर",
            "डेस्क",
            "कमरा",
            "बिल्डिंग",
            "रोड",
            "ब्रिज",
            "गेट",
            "दरवाजा",
            "किचन",
            "बाथरूम",
            "बेडरूम",
            "हॉल",
            "गार्डन",
            "टीचर",
            "स्टूडेंट",
            "डॉक्टर",
            "पेशेंट",
            "पुलिस",
            "सोल्जर",
            "लॉयर",
            "जज",
            "मैनेजर",
            "डायरेक्टर",
            "स्पीकर",
            "माइक",
            "सिस्टम",
            "सॉफ्टवेयर",
            "हार्डवेयर",
            "नेटवर्क",
            "डेटा",
            "फाइल",
            "फोल्डर",
            "ड्राइव",
            "केबल",
            "वायर",
            "स्विच",
            "प्लग",
            "सॉकेट",
            "बटन",
            "स्क्रीन",
            "डिस्प्ले",
            "कीबोर्ड",
            "माउस",
            "प्रिंटर",
            "स्कैनर",
            "कैमरा",
            "वीडियो",
            "ऑडियो",
            "म्यूजिक",
            "सॉन्ग",
            "मूवी",
            "फिल्म",
            "पिक्चर",
            "गेम",
            "खेल",
            "खिलाड़ी",
            "टीम",
            "प्लेयर",
            "रेफरी",
            "कोच",
            "कैप्टन",
            "लीडर",
            "विनर",
            "लूजर",
            "फाइनल",
            "सेमीफाइनल",
            "क्वार्टर",
            "राउंड",
            "मैच",
            "टूर्नामेंट",
            "चैंपियन",
            "ट्रॉफी",
            "मेडल",
            "प्राइज",
            "अवार्ड",
            "गिफ्ट",
            "प्रेजेंट",
            "टॉय",
            "बुक",
            "कॉपी",
            "पेपर",
            "पेन",
            "पेंसिल",
            "रबर",
            "इरेजर",
            "शार्पनर",
            "स्केल",
            "कंपास",
            "बैग",
            "बैकपैक",
            "सूटकेस",
            "बॉक्स",
            "पैकेट",
            "बोतल",
            "ग्लास",
            "कप",
            "प्लेट",
            "बाउल",
            "स्पून",
            "फोर्क",
            "नाइफ",
            "चॉपस्टिक",
            "स्ट्रॉ",
            "टिश्यू",
            "नेपकिन",
            "टॉवेल",
            "साबुन",
            "शैंपू",
            "क्रीम",
            "पाउडर",
            "परफ्यूम",
            "डियोड्रेंट",
            "टूथपेस्ट",
            "ब्रश",
            "कंघी",
            "मिरर",
            "कैंची",
            "नेलकटर",
            "रेजर",
            "शेविंग",
            "क्रीम",
            "लोशन",
            "ऑयल",
            "पेट्रोल",
            "डीजल",
            "गैस",
            "ऑयल",
            "लुब्रिकेंट",
            "पेंट",
            "कलर",
            "ब्रश",
            "रोलर",
            "स्प्रे",
            "सीमेंट",
            "सैंड",
            "स्टोन",
            "ब्रिक",
            "टाइल",
            "मार्बल",
            "ग्रेनाइट",
            "लकड़ी",
            "बांस",
            "प्लास्टिक",
            "रबर",
            "लीद",
            "कॉपर",
            "आयरन",
            "स्टील",
            "गोल्ड",
            "सिल्वर",
            "प्लैटिनम",
            "डायमंड",
            "ज्वेलरी",
            "वॉच",
            "घड़ी",
            "चश्मा",
            "सनग्लास",
            "लेंस",
            "बैटरी",
            "सेल",
            "चार्जर",
            "एडाप्टर",
            "कनवर्टर",
            "मीटर",
            "गेज",
            "माप",
            "तौल",
            "नाप",
            "स्पीड",
            "वेलोसिटी",
            "एक्सीलरेशन",
            "फोर्स",
            "पावर",
            "एनर्जी",
            "करंट",
            "वोल्टेज",
            "वाट",
            "अmpere",
            "फ्रीक्वेंसी",
            "वेव",
            "साउंड",
            "नॉइस",
            "वॉल्यूम",
            "टेंपरेचर",
            "प्रेशर",
            "ह्यूमिडिटी",
            "मॉइस्चर",
            "वेट",
            "ड्राई",
            "हॉट",
            "कोल्ड",
            "वर्म",
            "कूल",
            "फ्रोजन",
            "मेल्टेड",
            "बॉयल्ड",
            "स्टीम",
            "स्मोक",
            "फायर",
            "फ्लेम",
            "स्पार्क",
            "एश",
            "डस्ट",
            "मड",
            "क्ले",
            "सैंड",
            "सॉइल",
            "अर्थ",
            "वर्ल्ड",
            "अर्थ",
            "ग्लोब",
            "मैप",
            "चार्ट",
            "डायग्राम",
            "पिक्चर",
            "इमेज",
            "फोटो",
            "पोर्ट्रेट",
            "लैंडस्केप",
            "सीन",
            "व्यू",
            "साइट",
            "लोकेशन",
            "प्लेस",
            "स्पॉट",
            "जोन",
            "एरिया",
            "रिजन",
            "सेक्टर",
            "डिवीजन",
            "स्टेट",
            "सिटी",
            "टाउन",
            "विलेज",
            "कॉलोनी",
            "सोसाइटी",
            "कंपाउंड",
            "बिल्डिंग",
            "टावर",
            "ब्लॉक",
            "फ्लैट",
            "अपार्टमेंट",
            "कॉटेज",
            "बंगला",
            "महल",
            "किला",
            "फोर्ट",
            "पैलेस",
            "म्यूजियम",
            "लाइब्रेरी",
            "थिएटर",
            "सिनेमा",
            "हॉल",
            "ऑडिटोरियम",
            "स्टेडियम",
            "जिम",
            "क्लब",
            "बार",
            "रेस्टोरेंट",
            "होटल",
            "कैफे",
            "बेकरी",
            "शॉप",
            "स्टोर",
            "मार्केट",
            "मॉल",
            "सुपरमार्केट",
            "हाइपरमार्केट",
            "बुकस्टोर",
            "स्टेशनरी",
            "कपड़े",
            "जूते",
            "एक्सेसरीज",
            "ज्वेलरी",
            "वॉच",
            "गिफ्ट",
            "टॉय",
            "स्पोर्ट्स",
            "मेडिकल",
            "फार्मेसी",
            "क्लिनिक",
            "हॉस्पिटल",
            "नर्सिंग",
            "होम",
            "हाउस",
            "रूम",
            "बेडरूम",
            "किचन",
            "बाथरूम",
            "टॉयलेट",
            "लिविंग",
            "डाइनिंग",
            "ड्राइंग",
            "स्टडी",
            "ऑफिस",
            "वर्कशॉप",
            "गैरेज",
            "वेयरहाउस",
            "फैक्ट्री",
            "प्लांट",
            "इंडस्ट्री",
            "कंपनी",
            "कॉर्पोरेशन",
            "फर्म",
            "एजेंसी",
            "ब्यूरो",
            "सेंटर",
            "इंस्टीट्यूट",
            "एकेडमी",
            "यूनिवर्सिटी",
            "कॉलेज",
            "स्कूल",
            "किंडरगार्टन",
            "नर्सरी",
            "क्रेच",
            "डेकेयर",
            "प्लेग्रुप",
            "ट्यूशन",
            "कोचिंग",
            "ट्रेनिंग",
            "क्लास",
            "कोर्स",
            "प्रोग्राम",
            "प्रोजेक्ट",
            "प्रैक्टिकल",
            "थियरी",
            "एग्जाम",
            "टेस्ट",
            "क्विज",
            "असाइनमेंट",
            "होमवर्क",
            "प्रैक्टिस",
            "रिवीजन",
            "स्टडी",
            "पढ़ाई",
            "शिक्षा",
            "एजुकेशन",
            "लर्निंग",
            "टीचिंग",
            "ट्रेनिंग",
            "गाइडेंस",
            "काउंसलिंग",
            "एडवाइस",
            "सजेशन",
            "रिकमेंडेशन",
            "प्रेफरेंस",
            "चॉइस",
            "ऑप्शन",
            "सिलेक्शन",
            "पिक",
            "चूज",
            "डिसाइड",
            "डिसीजन",
            "रिजल्ट",
            "आउटकम",
            "इफेक्ट",
            "इम्पैक्ट",
            "इन्फ्लुएंस",
            "प्रभाव",
            "असर",
            "बदलाव",
            "चेंज",
            "ट्रांसफॉर्म",
            "कन्वर्ट",
            "एडाप्ट",
            "एडजस्ट",
            "मॉडिफाई",
            "अपडेट",
            "अपग्रेड",
            "इम्प्रूव",
            "एन्हांस",
            "बेहतर",
            "बढ़िया",
            "उत्तम",
            "बेस्ट",
            "गुड",
            "बैड",
            "खराब",
            "अच्छा",
            "बुरा",
            "सही",
            "गलत",
            "राइट",
            "रॉन्ग",
            "करेक्ट",
            "इनकरेक्ट",
            "ट्रू",
            "फॉल्स",
            "सच",
            "झूठ",
            "फैक्ट",
            "फिक्शन",
            "रियल",
            "असली",
            "नकली",
            "ऑरिजिनल",
            "कॉपी",
            "डुप्लीकेट",
            "यूनिक",
            "स्पेशल",
            "जनरल",
            "कॉमन",
            "नॉर्मल",
            "ऑर्डिनरी",
            "एक्स्ट्राऑर्डिनरी",
            "सिंपल",
            "कॉम्प्लेक्स",
            "ईजी",
            "डिफिकल्ट",
            "हार्ड",
            "सॉफ्ट",
            "स्मूथ",
            "रफ",
            "शार्प",
            "ब्लंट",
            "फाइन",
            "कोर्स",
            "थिक",
            "थिन",
            "फैट",
            "स्लिम",
            "फिट",
            "अनफिट",
            "हेल्दी",
            "अनहेल्दी",
            "सिक",
            "वेल",
            "फाइन",
            "बीमार",
            "ठीक",
            "खुश",
            "दुखी",
            "हैप्पी",
            "सैड",
            "ग्लैड",
            "एंग्री",
            "गुस्सा",
            "शांत",
            "एक्साइटेड",
            "बोर",
            "इंटरेस्ट",
            "डिसइंटरेस्ट",
            "लाइक",
            "डिसलाइक",
            "लव",
            "हेट",
            "एंजॉय",
            "सफर",
            "पसंद",
            "नापसंद",
            "चाह",
            "इच्छा",
            "इच्छा",
            "कामना",
            "आशा",
            "आशा",
            "उम्मीद",
            "अपेक्षा",
            "रिग्रेट",
            "शर्म",
            "गर्व",
            "घमंड",
            "अहंकार",
            "नेक",
            "बद",
            "भला",
            "बुरा",
            "सही",
            "गलत",
            "धर्म",
            "अधर्म",
            "पाप",
            "पुण्य",
            "स्वर्ग",
            "नर्क",
            "जन्नत",
            "दोजख",
            "ईश्वर",
            "अल्लाह",
            "वाहेगुरु",
            "ईसा",
            "मोहम्मद",
            "बुद्ध",
            "महावीर",
            "राम",
            "कृष्ण",
            "शिव",
            "दुर्गा",
            "लक्ष्मी",
            "सरस्वती",
            "गणेश",
            "हनुमान",
            "कर्तव्य",
            "फर्ज",
            "अधिकार",
            "हक",
            "ड्यूटी",
            "राइट",
            "जिम्मेदारी",
            "वादा",
            "प्रॉमिस",
            "कमिटमेंट",
            "डेडिकेशन",
            "डेवोशन",
            "भक्ति",
            "पूजा",
            "नमाज",
            "सेवा",
            "सेवा",
            "मदद",
            "हेल्प",
            "सपोर्ट",
            "सहयोग",
            "सहायता",
            "योगदान",
            "कॉन्ट्रिब्यूशन",
            "दान",
            "दान",
            "चैरिटी",
            "फिलैंथ्रोपी",
            "मानवता",
            "इंसानियत",
            "नेकी",
            "भलाई",
            "खुशी",
            "आनंद",
            "सुख",
            "दुख",
            "पीड़ा",
            "वेदना",
            "कष्ट",
            "तकलीफ",
            "परेशानी",
            "मुसीबत",
            "आफत",
            "संकट",
            "खतरा",
            "रिस्क",
            "चैलेंज",
            "मुश्किल",
            "आसान",
            "सरल",
            "कठिन",
            "भारी",
            "हल्का",
            "गहरा",
            "उथला",
            "ऊंचा",
            "नीचा",
            "लंबा",
            "छोटा",
            "बड़ा",
            "छोटा",
            "विशाल",
            "विशाल",
            "बृहद",
            "सूक्ष्म",
            "सूक्ष्म",
            "माइक्रो",
            "मैक्रो",
            "मिनी",
            "मैक्सी",
            "मैक्सी",
            "फुल",
            "खाली",
            "भरा",
            "खाली",
            "पूरा",
            "आधा",
            "चौथाई",
            "तीन",
            "चौथाई",
            "पैंतीस",
            "प्रतिशत",
            "प्रतिशत",
            "शत",
            "प्रतिशत",
            "दशमलव",
            "भिन्न",
            "पूर्णांक",
            "नकारात्मक",
            "धनात्मक",
            "जोड़",
            "घटाव",
            "गुणा",
            "भाग",
            "योगफल",
            "अंतर",
            "गुणनफल",
            "भागफल",
            "शेष",
            "शून्य",
            "एक",
            "दो",
            "तीन",
            "चार",
            "पांच",
            "छह",
            "सात",
            "आठ",
            "नौ",
            "दस",
            "सौ",
            "हजार",
            "लाख",
            "करोड़",
            "अरब",
            "खरब",
        ]
        return any(indicator in word for indicator in english_indicators)

    def _api_get_english(self, word: str) -> Optional[str]:
        """Use API to get English spelling for loanwords using hi-Latn"""
        if not self.api_available:
            return None

        try:
            # Use hi-Latn for better Romanized Hindi transliteration
            result = self.translator.translate(word, src="hi", dest="hi-Latn")
            return result.text.lower().strip()
        except:
            return None

        try:
            result = self.translator.translate(word, src="hi", dest="en")
            return result.text.lower().strip()
        except:
            return None

    def convert_word(self, word: str, learn: bool = True) -> str:
        """Convert a single word"""
        if not any("\u0900" <= c <= "\u097f" for c in word):
            return word

        # 1. Check dictionary
        if word in self.dictionary:
            self.stats["dictionary_hits"] += 1
            return self.dictionary[word]

        # 2. Check if it's an English loanword
        if self._is_english_loanword(word) and self.api_available:
            english = self._api_get_english(word)
            if english:
                self.stats["api_loanwords"] += 1
                result = english
            else:
                self.stats["rule_based"] += 1
                result = self.base_converter._transliterate_word(word)
        else:
            # 3. Use rule-based for native Hindi words
            self.stats["rule_based"] += 1
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

    def show_learning_summary(self):
        """Show learning summary"""
        print("\n" + "=" * 60)
        print("SMART HYBRID CONVERTER - LEARNING SUMMARY")
        print("=" * 60)
        print(f"📚 Dictionary hits: {self.stats['dictionary_hits']}")
        print(f"🌐 API loanwords: {self.stats['api_loanwords']}")
        print(f"📏 Rule-based: {self.stats['rule_based']}")
        print(f"📝 New words learned: {self.stats['new_words_learned']}")
        print(f"📖 Total dictionary size: {len(self.dictionary)}")
        print("=" * 60)


if __name__ == "__main__":
    import sys
    import io

    if sys.platform == "win32":
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

    converter = SmartHybridConverter()

    test_sentences = [
        "मीटिंग में जाऊं क्या?",
        "प्रेजेंटेशन तैयार है।",
        "कंप्यूटर स्लो हो गया।",
        "नमस्ते दोस्तों!",
    ]

    print("\n" + "=" * 60)
    print("SMART HYBRID CONVERTER - TEST")
    print("=" * 60)

    for hindi in test_sentences:
        hinglish = converter.convert(hindi)
        print(f"\nHindi:    {hindi}")
        print(f"Hinglish: {hinglish}")

    converter.show_learning_summary()
    converter._save_learned_words()
