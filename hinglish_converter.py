"""
Hindi to Natural Hinglish Converter
Customized transliteration for conversational Hinglish (not ITRANS)
Optimized with LRU caching for high performance
"""

import re
from functools import lru_cache
from typing import Dict, List, Tuple


class HinglishConverter:
    """
    A highly accurate Hindi to Hinglish converter that produces
    natural conversational Hinglish instead of ITRANS format.
    """

    def __init__(self):
        # Vowel mappings - natural Hinglish style
        self.vowels = {
            "अ": "a",  # Short 'a' as in 'about'
            "आ": "aa",  # Long 'a' as in 'father'
            "इ": "i",  # Short 'i' as in 'sit'
            "ई": "ee",  # Long 'i' as in 'feet'
            "उ": "u",  # Short 'u' as in 'put'
            "ऊ": "oo",  # Long 'u' as in 'boot'
            "ऋ": "ri",  # Vocalic 'r'
            "ए": "e",  # 'e' as in 'bed'
            "ऐ": "ai",  # 'ai' as in 'aisle'
            "ओ": "o",  # 'o' as in 'go'
            "औ": "au",  # 'au' as in 'how'
            "अं": "an",  # Anusvara - nasal
            "अः": "ah",  # Visarga
        }

        # Matra (vowel sign) mappings
        self.matra_map = {
            "ा": "a",
            "ि": "i",
            "ी": "ee",
            "ु": "u",
            "ू": "oo",
            "े": "e",
            "ै": "ai",
            "ो": "o",
            "ौ": "au",
            "ं": "n",  # Anusvara - becomes 'n' or 'm' based on context
            "ः": "h",
            "ृ": "ri",
        }

        # Consonant mappings - natural Hinglish
        self.consonants = {
            # Velar consonants
            "क": "k",
            "ख": "kh",
            "ग": "g",
            "घ": "gh",
            "ङ": "ng",
            # Palatal consonants
            "च": "ch",
            "छ": "chh",
            "ज": "j",
            "झ": "jh",
            "ञ": "ny",
            # Retroflex consonants
            "ट": "t",
            "ठ": "th",
            "ड": "d",
            "ढ": "dh",
            "ण": "n",
            # Dental consonants
            "त": "t",
            "थ": "th",
            "द": "d",
            "ध": "dh",
            "न": "n",
            # Labial consonants
            "प": "p",
            "फ": "f",
            "ब": "b",
            "भ": "bh",
            "म": "m",
            # Semi-vowels
            "य": "y",
            "र": "r",
            "ल": "l",
            "व": "v",
            # Sibilants
            "श": "sh",
            "ष": "sh",
            "स": "s",
            # Aspirate
            "ह": "h",
            # Additional
            "क्ष": "ksh",
            "त्र": "tr",
            "ज्ञ": "gy",
            "श्र": "shr",
            "क़": "q",
            "ख़": "kh",
            "ग़": "gh",
            "ज़": "z",
            "झ़": "zh",
            "ड़": "r",
            "ढ़": "rh",
            "फ़": "f",
        }

        # Half consonants (when combined with virama)
        self.halant = "्"

        # Nukta for extended sounds
        self.nukta = "़"

        # Common words dictionary for better accuracy
        self.common_words = {
            "है": "hai",
            "हैं": "hain",
            "हो": "ho",
            "था": "tha",
            "थी": "thi",
            "थे": "the",
            "हूं": "hoon",
            "होगा": "hoga",
            "होगी": "hogi",
            "होंगे": "honge",
            "कर": "kar",
            "किया": "kiya",
            "करना": "karna",
            "कीजिए": "kijiye",
            "कीजिये": "kijiye",
            "एक": "ek",
            "यह": "yeh",
            "वह": "woh",
            "घूमने": "ghoomne",
            "बाहर": "bahar",
            "नाम": "naam",
            "भारत": "bharat",
            "हिंदी": "hindi",
            "पसंद": "pasand",
            "बाहर": "bahar",
            "स्वादिष्ट": "swaadisht",
            "सब्जियां": "sabziyaan",
            "सब्जी": "sabzi",
            "सब्जियाँ": "sabziyaan",
            "खरीदना": "khareedna",
            "खरीदने": "khareedne",
            "फल": "phal",
            "चाहिए": "chahiye",
            "चाहिए?": "chahiye?",
            "गर्मी": "garmi",
            "धूप": "dhoop",
            "तेज": "tej",
            "शायद": "shaayad",
            "बारिश": "baarish",
            "होगी": "hogi",
            "समय": "samay",
            "बिताना": "bitaana",
            "हंसते": "hansate",
            "मज़ा": "maza",
            "मोबाइल": "mobile",
            "फोन": "phone",
            "खराब": "kharaab",
            "इंटरनेट": "internet",
            "ऑर्डर": "order",
            "करूंगा": "karunga",
            "सिरदर्द": "sirdard",
            "दवा": "dawa",
            "लूंगा": "loonga",
            "ट्रेन": "train",
            "रिश्तेदारों": "rishtedaaron",
            "पकाना": "pakaana",
            "आलू": "aaloo",
            "दाल": "daal",
            "चावल": "chawal",
            "बनाऊंगा": "banaunga",
            "सिनेमा": "cinema",
            "फिल्म": "film",
            "देखी": "dekhi",
            "अच्छी": "achhi",
            "लड़का": "ladka",
            "लड़की": "ladki",
            "कहानी": "kahaani",
            "दोस्ती": "dostee",
            "एंजॉय": "enjoy",
            "किया": "kiya",
            "समय": "samay",
            "कहानियां": "kahaaniyaan",
            "सुना": "suna",
            "सुनाती": "sunaati",
            "थीं": "thiin",
            "अपनी": "apni",
            "दादी": "dadi",
            "रहता": "rehta",
            "मिलने": "milne",
            "बैठकर": "baithkar",
            "खाएंगे": "khaaenge",
            "घर": "ghar",
            "आए": "aaye",
            "वहाँ": "vahaan",
            "पढ़ाई": "padhaai",
            "हमें": "hamein",
            "करनी": "karni",
            "केल": "khel",
            "खेलना": "khelna",
            "गांव": "gaanv",
            "बूढ़ा": "boodha",
            "आदमी": "aadmi",
            "रहता": "rehta",
            "बेटा": "beta",
            "बेटी": "beti",
            "गरीब": "gareeb",
            "ईमानदार": "imaandaar",
            "रहा": "raha",
            "रही": "rahi",
            "रहे": "rahe",
            "जा": "ja",
            "गया": "gaya",
            "गयी": "gayi",
            "गये": "gaye",
            "आ": "aa",
            "आया": "aaya",
            "आयी": "aayi",
            "आये": "aaye",
            "चुका": "chuka",
            "चुकी": "chuki",
            "चुके": "chuke",
            "सकता": "sakta",
            "सकती": "sakti",
            "सकते": "sakte",
            "लिया": "liya",
            "दिया": "diya",
            "पड़ा": "pada",
            "वाला": "wala",
            "वाली": "wali",
            "वाले": "wale",
            "भी": "bhi",
            "ही": "hi",
            "तो": "to",
            "बहुत": "bahut",
            "ज्यादा": "zyada",
            "कम": "kam",
            "अच्छा": "achha",
            "अच्छी": "achhi",
            "अच्छे": "achhe",
            "बड़ा": "bada",
            "बड़ी": "badi",
            "छोटा": "chhota",
            "छोटी": "chhoti",
            "नया": "naya",
            "नयी": "nayi",
            "पुराना": "purana",
            "पुरानी": "purani",
            "और": "aur",
            "या": "ya",
            "लेकिन": "lekin",
            "क्योंकि": "kyunki",
            "अगर": "agar",
            "तो": "to",
            "तोह": "toh",
            "जब": "jab",
            "तब": "tab",
            "जहां": "jahan",
            "वहां": "vahan",
            "कहां": "kahan",
            "यहां": "yahan",
            "कैसे": "kaise",
            "क्या": "kya",
            "क्यों": "kyun",
            "कब": "kab",
            "कौन": "kaun",
            "किस": "kis",
            "जो": "jo",
            "सो": "so",
            "वो": "wo",
            "ये": "ye",
            "वो": "vo",
            "मैं": "main",
            "मुझे": "mujhe",
            "फाइल": "file",
            "पसंदीदा": "pasandida",
            "फिल्में": "filmein",
            "इडियट्स": "idiots",
            "मेरा": "mera",
            "मेरी": "meri",
            "मेरे": "mere",
            "हम": "hum",
            "हमें": "hamein",
            "हमारा": "hamara",
            "हमारी": "hamari",
            "हमारे": "hamare",
            "तुम": "tum",
            "तुझे": "tujhe",
            "तेरा": "tera",
            "तेरी": "teri",
            "तेरे": "tere",
            "आप": "aap",
            "आपको": "aapko",
            "आपका": "aapka",
            "आपकी": "aapki",
            "आपके": "aapke",
            "वह": "vah",
            "उसे": "use",
            "उसका": "uska",
            "उसकी": "uski",
            "उसके": "uske",
            "यह": "yah",
            "इसे": "ise",
            "इसका": "iska",
            "इसकी": "iski",
            "इसके": "iske",
            "वे": "ve",
            "उन्हें": "unhein",
            "उनका": "unka",
            "उनकी": "unki",
            "उनके": "unke",
            "ये": "ye",
            "इन्हें": "inhein",
            "इनका": "inka",
            "इनकी": "inki",
            "इनके": "inke",
            "नहीं": "nahi",
            "ना": "na",
            "मत": "mat",
            "माँ": "maa",
            "पापा": "papa",
            "भाई": "bhai",
            "बहन": "behan",
            "दोस्त": "dost",
            "यार": "yaar",
            "साला": "saala",
            "घर": "ghar",
            "काम": "kaam",
            "पैसा": "paisa",
            "पैसे": "paise",
            "खाना": "khana",
            "पानी": "paani",
            "रोटी": "roti",
            "सब्जी": "sabzi",
            "दाल": "daal",
            "चावल": "chawal",
            "नमक": "namak",
            "मिर्च": "mirch",
            "मीठा": "meetha",
            "खट्टा": "khatta",
            "तीखा": "teekha",
            "दिन": "din",
            "रात": "raat",
            "सुबह": "subah",
            "शाम": "shaam",
            "आज": "aaj",
            "कल": "kal",
            "परसों": "parson",
            "साल": "saal",
            "महिना": "mahina",
            "हफ्ता": "hafta",
            "घंटा": "ghanta",
            "मिनट": "minute",
            "पल": "pal",
            "वक्त": "waqt",
            "समय": "samay",
            "देखो": "dekho",
            "सुनो": "suno",
            "बोलो": "bolo",
            "चलो": "chalo",
            "आओ": "aao",
            "जाओ": "jao",
            "लो": "lo",
            "दो": "do",
            "ले": "le",
            "दे": "de",
            "रुको": "ruko",
            "बैठो": "baitho",
            "खड़े": "khade",
            "खड़ा": "khada",
            "खड़ी": "khadi",
            "पढ़ो": "padho",
            "लिखो": "likho",
            "समझो": "samjho",
            "प्यार": "pyaar",
            "मोहब्बत": "mohabbat",
            "इश्क": "ishq",
            "दिल": "dil",
            "जान": "jaan",
            "जानू": "jaanu",
            "बेबी": "baby",
            "शादी": "shaadi",
            "बच्चा": "bachcha",
            "बच्ची": "bachchi",
            "लड़का": "ladka",
            "लड़की": "ladki",
            "आदमी": "aadmi",
            "औरत": "aurat",
            "भूख": "bhookh",
            "प्यास": "pyaas",
            "नींद": "neend",
            "ठंड": "thand",
            "गर्मी": "garmi",
            "बारिश": "baarish",
            "धूप": "dhoop",
            "हवा": "hawa",
            "रास्ता": "rasta",
            "सड़क": "sadak",
            "गली": "gali",
            "मोहल्ला": "mohalla",
            "शहर": "shehar",
            "गांव": "gaanv",
            "देश": "desh",
            "दुनिया": "duniya",
            "जिंदगी": "zindagi",
            "मौत": "maut",
            "भगवान": "bhagwan",
            "अल्लाह": "allah",
            "रब": "rab",
            "मंदिर": "mandir",
            "मस्जिद": "masjid",
            "गिरजा": "girja",
            "गुरुद्वारा": "gurudwara",
            "स्कूल": "school",
            "कॉलेज": "college",
            "यूनिवर्सिटी": "university",
            "अस्पताल": "aspatal",
            "दवा": "dawa",
            "डॉक्टर": "doctor",
            "पुलिस": "police",
            "सरकार": "sarkar",
            "नेता": "neta",
            "पार्टी": "party",
            "चुनाव": "chunaav",
            "वोट": "vote",
            "पैसा": "paisa",
            "पैसे": "paise",
            "रुपया": "rupaya",
            "रुपये": "rupaye",
            "डॉलर": "dollar",
            "बैंक": "bank",
            "दुकान": "dukaan",
            "बाजार": "bazaar",
            "कीमत": "keemat",
            "कम": "kam",
            "ज्यादा": "zyada",
            "सस्ता": "sasta",
            "महंगा": "mahanga",
            "अमीर": "ameer",
            "गरीब": "garib",
            "किताब": "kitaab",
            "अखबार": "akhbaar",
            "पन्ना": "panna",
            "फिल्म": "film",
            "गाना": "gaana",
            "गीत": "geet",
            "नाच": "naach",
            "खेल": "khel",
            "खिलाड़ी": "khiladi",
            "जीत": "jeet",
            "हार": "haar",
            "बराबर": "barabar",
            "जीतना": "jeetna",
            "हारना": "haarna",
            "मज़ा": "maza",
            "मस्ती": "masti",
            "झूठ": "jhooth",
            "सच": "sach",
            "गलत": "galat",
            "सही": "sahi",
            "आसान": "aasaan",
            "मुश्किल": "mushkil",
            "तकलीफ": "takleef",
            "मुसीबत": "museebat",
            "खुशी": "khushi",
            "गम": "gam",
            "हंसी": "hansi",
            "रोना": "rona",
            "हसना": "hasna",
            "मुस्कुराना": "muskurana",
            "शुक्रिया": "shukriya",
            "धन्यवाद": "dhanyavaad",
            "माफ़ी": "maafi",
            "सॉरी": "sorry",
            "प्लीज": "please",
            "थैंक्यू": "thankyou",
            "नमस्ते": "namaste",
            "सलाम": "salaam",
            "अलविदा": "alvida",
            "फिरमिलेंगे": "phirmilenge",
            "फिर": "phir",
            "अब": "ab",
            "तब": "tab",
            "कभी": "kabhi",
            "हमेशा": "hamesha",
            "कभी-कभी": "kabhi-kabhi",
            "जल्दी": "jaldi",
            "देर": "der",
            "पहले": "pehle",
            "बाद": "baad",
            "आगे": "aage",
            "पीछे": "peeche",
            "ऊपर": "upar",
            "नीचे": "neeche",
            "अंदर": "andar",
            "बाहर": "baahar",
            "बीच": "beech",
            "पास": "paas",
            "दूर": "door",
            "साथ": "saath",
            "अकेला": "akele",
            "अकेली": "akelee",
            "वापस": "waapas",
            "फिरसे": "phirse",
            "दोबारा": "dobaara",
            "बिल्कुल": "bilool",
            "सीधा": "seedha",
            "उल्टा": "ulta",
            "साफ": "saaf",
            "गंदा": "ganda",
            "ठीक": "theek",
            "बेहतर": "behtar",
            "बढ़िया": "badhiya",
            "कमाल": "kamaal",
            "ज़बरदस्त": "zabardast",
            "झक्कास": "jhakaas",
            "ढेरसारा": "dhersaara",
            "बहुतसारा": "bahutsaara",
            "थोड़ा": "thoda",
            "थोड़ी": "thodi",
            "कुछ": "kuch",
            "सब": "sab",
            "सारा": "saara",
            "हर": "har",
            "कोई": "koi",
            "किसी": "kisi",
            "कुछ": "kuchh",
            "ज़रा": "zara",
            "बस": "bas",
            "रुको": "ruko",
            "चलो": "chalo",
            "आओ": "aao",
            "देखो": "dekho",
            "सुनो": "suno",
            "समझे": "samjhe",
            "पता": "pata",
            "मालूम": "maaloom",
            "खबर": "khabar",
            "ख्याल": "khayaal",
            "सोच": "soch",
            "बात": "baat",
            "वादा": "vaada",
            "वचन": "vachan",
            "मिलना": "milna",
            "मिलो": "milo",
            "मिला": "mila",
            "गया": "gaya",
            "आया": "aaya",
            "लाया": "laaya",
            "दिया": "diya",
            "किया": "kiya",
            "हुआ": "hua",
            "सोया": "soya",
            "रोया": "roya",
            "हंसा": "hansa",
            "नाचा": "naacha",
            "गाया": "gaaya",
            "बजाया": "bajaaya",
            "सुनाया": "sunaaya",
            "सिखाया": "sikhaaya",
            "बताया": "bataaya",
            "लगाया": "lagaaya",
            "चलाया": "chalaaya",
            "दिखाया": "dikhaaya",
            "लिखा": "likha",
            "पढ़ा": "padha",
            "सुना": "suna",
            "बोला": "bola",
            "मिला": "mila",
            "खोला": "khola",
            "बंद": "band",
            "बंदकिया": "band kiya",
            "शुरू": "shuru",
            "खत्म": "khatm",
            "पूरा": "poora",
            "आधा": "aadha",
            "जीना": "jeena",
            "मरना": "marna",
            "आना": "aana",
            "जाना": "jaana",
            "आकर": "aakar",
            "जाकर": "jaakar",
            "देकर": "dekar",
            "लेकर": "lekar",
            "होकर": "hokar",
            "करके": "karke",
            "होके": "hoke",
            "देके": "deke",
            "लेके": "leke",
            "जाके": "jake",
            "आके": "aake",
            "पाके": "paake",
            "खाके": "khaake",
            "पीके": "peke",
            "रोके": "roke",
            "हंसके": "hanske",
            "मुस्कुराके": "muskurake",
        }

        # Build combined character list for tokenization
        self.all_hindi_chars = set(
            list(self.vowels.keys())
            + list(self.consonants.keys())
            + list(self.matra_map.keys())
            + [
                self.halant,
                self.nukta,
                "०",
                "१",
                "२",
                "३",
                "४",
                "५",
                "६",
                "७",
                "८",
                "९",
            ]
        )

    def _is_hindi(self, char: str) -> bool:
        """Check if character is Hindi (Devanagari)"""
        if not char:
            return False
        return "\u0900" <= char <= "\u097f"

    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text into Hindi words and non-Hindi segments"""
        tokens = []
        current_token = ""
        current_is_hindi = None

        for char in text:
            if char.isspace():
                if current_token:
                    tokens.append(current_token)
                    current_token = ""
                tokens.append(char)
                current_is_hindi = None
            elif self._is_hindi(char):
                if current_is_hindi is False and current_token:
                    tokens.append(current_token)
                    current_token = ""
                current_is_hindi = True
                current_token += char
            else:
                if current_is_hindi is True and current_token:
                    tokens.append(current_token)
                    current_token = ""
                current_is_hindi = False
                current_token += char

        if current_token:
            tokens.append(current_token)

        return tokens

    def _apply_schwa_deletion(self, result: str) -> str:
        """
        Apply schwa deletion and vowel normalization rules for natural Hinglish.
        """
        if len(result) <= 2:
            return result

        original = result
        result_lower = result.lower()

        # Common verb infinitive endings: -na (should be -na not -n)
        if result_lower.endswith("ana") and len(result) > 4:
            # bolana -> bolna, karna -> karna (keep), dekhana -> dekhna
            stem = result[:-3]
            if stem and stem[-1] not in "aeiou":
                result = stem + "na"

        # Past tense / continuous: -ta, -te, -ti (should drop middle 'a' sometimes)
        # chalate -> chalte, karta -> karta (keep)
        if result_lower.endswith("ate") and len(result) > 4:
            stem = result[:-3]
            result = stem + "te"
        if result_lower.endswith("ati") and len(result) > 4:
            stem = result[:-3]
            result = stem + "ti"
        if result_lower.endswith("ata") and len(result) > 4:
            # Check if it's a 3-syllable pattern
            stem = result[:-3]
            if len(stem) >= 3:
                result = stem + "ta"

        # Feminine -ee -> -i at end of words
        # lagee -> lagi, chhotee -> chhoti
        if result_lower.endswith("ee") and len(result) > 3:
            # Check if it's a feminine form
            result = result[:-2] + "i"

        # Final 'a' deletion for non-verb words
        keep_final_a = {
            "papa",
            "mama",
            "baba",
            "dada",
            "nana",
            "data",
            "kana",
            "tana",
            "pana",
            "sana",
            "vana",
            "jana",
            "gaana",
            "shaana",
            "maana",
            "jaana",
            "paana",
            "laana",
            "haana",
            "yaar",
            "saara",
        }

        if result_lower.endswith("a") and result_lower not in keep_final_a:
            if len(result) > 3:
                # Don't delete from verb forms
                verb_keep = {"na", "ta", "ti", "te", "ni", "ne", "ya"}
                if result_lower[-2:] not in verb_keep:
                    result = result[:-1]

        # Middle 'a' deletion in common patterns
        # bharaata -> bharat
        if "aa" in result_lower:
            # Reduce double a to single a
            result = result.replace("aa", "a")

        return result

    def _transliterate_word(self, word: str) -> str:
        """Transliterate a single Hindi word to Hinglish"""

        # Check if it's in common words dictionary
        if word in self.common_words:
            return self.common_words[word]

        result = []
        i = 0
        n = len(word)

        while i < n:
            char = word[i]

            # Check for nukta (modified consonants)
            if i + 1 < n and word[i + 1] == self.nukta:
                combined = char + self.nukta
                if combined in self.consonants:
                    result.append(self.consonants[combined])
                    i += 2
                    # Add 'a' if not followed by matra or halant
                    if (
                        i < n
                        and word[i] not in self.matra_map
                        and word[i] != self.halant
                    ):
                        result.append("a")
                    continue

            # Check for halant (half consonant)
            if char == self.halant:
                i += 1
                continue

            # Check if it's a vowel
            if char in self.vowels:
                # If it's at the start or after a space, use full vowel
                if i == 0 or word[i - 1].isspace():
                    result.append(self.vowels[char])
                else:
                    result.append(self.vowels[char])
                i += 1
                continue

            # Check if it's a matra
            if char in self.matra_map:
                result.append(self.matra_map[char])
                i += 1
                continue

            # Check if it's a consonant
            if char in self.consonants:
                # Check for two-character consonants (like क्ष, त्र, ज्ञ, श्र)
                if i + 1 < n:
                    two_char = char + word[i + 1]
                    if two_char in self.consonants:
                        result.append(self.consonants[two_char])
                        i += 2
                        # Check for halant after
                        if i < n and word[i] == self.halant:
                            i += 1
                        elif i < n and word[i] not in self.matra_map:
                            result.append("a")
                        continue

                result.append(self.consonants[char])
                i += 1

                # Check if next char is halant (half consonant - no schwa)
                if i < n and word[i] == self.halant:
                    i += 1
                # Check if next char is a matra (vowel modifies the consonant)
                elif i < n and word[i] in self.matra_map:
                    # Don't add 'a', matra will be processed in next iteration
                    pass
                # Check if it's end of word or next is not a vowel modifier
                elif (
                    i >= n
                    or not self._is_hindi(word[i])
                    or word[i] not in self.matra_map
                ):
                    # Add inherent 'a' vowel
                    result.append("a")
                continue

            # Handle digits
            digit_map = {
                "०": "0",
                "१": "1",
                "२": "2",
                "३": "3",
                "४": "4",
                "५": "5",
                "६": "6",
                "७": "7",
                "८": "8",
                "९": "9",
            }
            if char in digit_map:
                result.append(digit_map[char])
                i += 1
                continue

            # Handle Hindi danda (punctuation mark)
            if char == "।":
                result.append(".")
                i += 1
                continue

            # Keep other characters as is (punctuation, etc.)
            result.append(char)
            i += 1

        # Join and apply schwa deletion
        final_result = "".join(result)
        final_result = self._apply_schwa_deletion(final_result)

        return final_result

    def convert(self, text: str, use_cache: bool = True) -> str:
        """
        Convert Hindi text to natural conversational Hinglish.

        Args:
            text: Hindi text in Devanagari script
            use_cache: Whether to use LRU caching (default: True)

        Returns:
            Hinglish text (Hindi written in Roman script)
        """
        if not isinstance(text, str):
            return ""

        if not text:
            return ""

        if use_cache:
            return self._convert_cached(text)
        return self._convert_impl(text)

    @lru_cache(maxsize=5000)
    def _convert_cached(self, text: str) -> str:
        """Cached version of convert for repeated texts."""
        return self._convert_impl(text)

    def _convert_impl(self, text: str) -> str:
        """Internal conversion implementation."""
        tokens = self._tokenize(text)
        result = []

        for token in tokens:
            if token.isspace():
                result.append(token)
            elif any(self._is_hindi(char) for char in token):
                # It's a Hindi word
                result.append(self._transliterate_word(token))
            else:
                # Keep non-Hindi as is
                result.append(token)

        return "".join(result)

    def clear_cache(self) -> None:
        """Clear the LRU cache."""
        self._convert_cached.cache_clear()

    def get_cache_info(self):
        """Get cache statistics."""
        return self._convert_cached.cache_info()

    def convert_file(
        self, input_path: str, output_path: str | None = None
    ) -> str | None:
        """
        Convert Hindi text from a file to Hinglish.

        Args:
            input_path: Path to input file with Hindi text
            output_path: Optional path to save output (if None, returns text)

        Returns:
            Hinglish text if output_path is None, else None
        """
        try:
            with open(input_path, "r", encoding="utf-8") as f:
                text = f.read()

            hinglish = self.convert(text)

            if output_path:
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(hinglish)
                return None

            return hinglish

        except FileNotFoundError:
            raise FileNotFoundError(f"Input file not found: {input_path}")
        except Exception as e:
            raise Exception(f"Error processing file: {str(e)}")


# Create a singleton instance for easy use
_converter = HinglishConverter()


def convert(text: str) -> str:
    """Convenience function to convert Hindi text to Hinglish"""
    return _converter.convert(text)


def convert_file(input_path: str, output_path: str | None = None) -> str | None:
    """Convenience function to convert Hindi file to Hinglish"""
    return _converter.convert_file(input_path, output_path)


if __name__ == "__main__":
    # Fix Windows console encoding
    import sys
    import io

    if sys.platform == "win32":
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

    # Test with some examples
    test_sentences = [
        "नमस्ते, आप कैसे हैं?",
        "मैं ठीक हूं, धन्यवाद!",
        "आज मौसम बहुत अच्छा है",
        "मुझे हिंदी बोलना पसंद है",
        "यह एक बढ़िया दिन है",
        "मेरा नाम राहुल है",
        "मैं भारत से हूं",
        "क्या आप मेरी मदद कर सकते हैं?",
        "मुझे भूख लगी है",
        "चलो बाहर घूमने चलते हैं",
    ]

    print("=" * 60)
    print("HINDI TO HINGLISH CONVERTER - TEST RESULTS")
    print("=" * 60)

    converter = HinglishConverter()

    for hindi in test_sentences:
        hinglish = converter.convert(hindi)
        print(f"\nHindi:   {hindi}")
        print(f"Hinglish: {hinglish}")

    print("\n" + "=" * 60)
