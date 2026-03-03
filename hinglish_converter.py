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
            "व": "w",  # Alternative
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
            "ज्ञ": "gyn",  # Alternative
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

        # Common suffix patterns for smarter transliteration
        self.suffix_patterns = {
            # Verb conjugations
            "ना": "na",  # karna -> karna
            "नी": "ni",  # karni -> karni
            "ने": "ne",  # karne -> karne
            "ा": "a",  # kiya -> kiya ( masculine past)
            "ी": "i",  # kiyi -> kiyi (feminine past)
            "े": "e",  # kare -> kare (subjunctive)
            "ें": "en",  # karen -> karen (plural subjunctive)
            "ो": "o",  # karo -> karo (imperative)
            "ता": "ta",  # karta -> karta (present continuous masc)
            "ती": "ti",  # karti -> karti (present continuous fem)
            "ते": "te",  # karte -> karte (present continuous plural)
            "ों": "on",  # "on" sound (plural oblique)
            "ां": "an",  # "aan" sound (plural oblique fem)
            "ई": "i",  # feminine ending
            "ए": "e",  # plural ending
            "इए": "iye",  # respectful request
            "िए": "iye",  # alternate
            "आ": "aa",  # masculine ending
            "आओ": "aao",  # plural request
            "ूँ": "oon",  # first person ending
            "ूं": "oon",  # alternate
        }

        # Common prefixes
        self.prefix_patterns = {
            "अ": "a",
            "आ": "aa",
            "अन": "an",
            "बे": "be",
            "घ": "gh",
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
            "वाला": "waala",
            "वाली": "waali",
            "वाले": "waale",
            "वालों": "waalon",
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
            # Additional words for better coverage
            "त्योहार": "tyohaar",
            "वाईफाई": "wifi",
            "लड़कियों": "ladkiyon",
            "लड़कियाँ": "ladkiyaan",
            "दीपावली": "deepaavali",
            "दीवाली": "diwali",
            "शहर": "shehar",
            "शहरों": "sheharon",
            "गांव": "gaanv",
            "गांवों": "gaanvon",
            "दोस्तों": "doston",
            "बच्चों": "bachchon",
            "बच्चे": "bachche",
            "लोगों": "logon",
            "घरों": "gharon",
            "मकानों": "makaanon",
            "दुकानें": "dukaanein",
            "दुकानों": "dukaanon",
            "बातें": "baatein",
            "रातें": "raatein",
            "सड़कें": "sadkein",
            "गलियाँ": "galiyan",
            "कहानियाँ": "kahaaniyaan",
            "कहानियां": "kahaaniyaan",
            "फिल्में": "filmein",
            "चिट्ठी": "chitthi",
            "चिट्ठियाँ": "chitthiyaan",
            # Essential common words that were missing
            "में": "mein",
            "को": "ko",
            "से": "se",
            "ने": "ne",
            "का": "ka",
            "की": "ki",
            "के": "ke",
            "हो": "ho",
            "वो": "wo",
            "वह": "woh",
            "यह": "yeh",
            "सब": "sab",
            "उस": "us",
            "इस": "is",
            "जो": "jo",
            "तो": "toh",
            "ही": "hi",
            "भी": "bhi",
            "था": "tha",
            "थी": "thi",
            "थे": "the",
            "हूँ": "hoon",
            "हैं": "hain",
            "गया": "gaya",
            "गई": "gayi",
            "गए": "gaye",
            "आया": "aaya",
            "आई": "aayi",
            "आए": "aaye",
            "लिया": "liya",
            "दिया": "diya",
            "किया": "kiya",
            "रहा": "raha",
            "रही": "rahi",
            "रहे": "rahe",
            "चला": "chala",
            "देखा": "dekha",
            "सुना": "suna",
            "बोला": "bola",
            "पढ़ा": "padha",
            "लिखा": "likha",
            "खाना": "khana",
            "पाना": "paana",
            "जाना": "jaana",
            "आना": "aana",
            "लेना": "lena",
            "देना": "dena",
            "पीना": "peena",
            "सोना": "sona",
            "होना": "hona",
            "रहना": "rehna",
            "कहना": "kehna",
            "सुनना": "sunna",
            "देखना": "dekhna",
            "समझना": "samajhna",
            "बोलना": "bolna",
            "चलना": "chalna",
            "मिलना": "milna",
            "बैठना": "baithna",
            "उठना": "uthna",
            "सोचना": "sochna",
            "मानना": "maanna",
            "जानना": "jaanna",
            "पहचानना": "pehchaanna",
            "बचाना": "bachaana",
            "बताना": "bataana",
            "सिखाना": "sikhaana",
            "बुलाना": "bulaana",
            "भेजना": "bhejna",
            "मांगना": "maangna",
            "लगाना": "lagaana",
            "रखना": "rakhna",
            "दिखाना": "dikhaana",
            "निकालना": "nikaalna",
            "डालना": "daalna",
            "फेंकना": "fenkna",
            "तोड़ना": "todna",
            "जोड़ना": "jodna",
            "खोलना": "kholna",
            "चाहना": "chaahna",
            "चाहिए": "chahiye",
            "पसंद": "pasand",
            "मालूम": "maaloom",
            "पता": "pata",
            "समझ": "samajh",
            "सोच": "soch",
            "बात": "baat",
            "काम": "kaam",
            "वक्त": "waqt",
            "दिन": "din",
            "रात": "raat",
            "सुबह": "subah",
            "शाम": "shaam",
            "दोपहर": "dopahar",
            "आज": "aaj",
            "कल": "kal",
            "परसों": "parson",
            "हफ्ता": "hafta",
            "महीना": "mahina",
            "साल": "saal",
            "पहले": "pehle",
            "बाद": "baad",
            "जल्दी": "jaldi",
            "देर": "der",
            "अभी": "abhi",
            "बादमें": "baad mein",
            "थोड़ा": "thoda",
            "थोड़ी": "thodi",
            "ज्यादा": "zyada",
            "बहुत": "bahut",
            "कम": "kam",
            "कुछ": "kuchh",
            "सारा": "saara",
            "पूरा": "poora",
            "आधा": "aadha",
            "बाकी": "baaki",
            "आदमी": "aadmi",
            "औरत": "aurat",
            "लड़का": "ladka",
            "लड़की": "ladki",
            "बच्चा": "bachcha",
            "इंसान": "insaan",
            "दोस्त": "dost",
            "यार": "yaar",
            "माँ": "maa",
            "पापा": "papa",
            "पिता": "pita",
            "माता": "maata",
            "भाई": "bhai",
            "बहन": "behan",
            "बेटा": "beta",
            "बेटी": "beti",
            "पति": "pati",
            "पत्नी": "patni",
            "नानी": "nani",
            "दादी": "dadi",
            "नाना": "nana",
            "दादा": "dada",
            "घर": "ghar",
            "दरवाज़ा": "darvaaza",
            "दीवार": "deevaar",
            "छत": "chhat",
            "फर्श": "farsh",
            "कमरा": "kamra",
            "रसोई": "rasoi",
            "बाथरूम": "bathroom",
            "बैठक": "baithak",
            "बगीचा": "bageecha",
            "गली": "gali",
            "सड़क": "sadak",
            "बाज़ार": "baazaar",
            "दुकान": "dukaan",
            "शहर": "shehar",
            "गांव": "gaanv",
            "देश": "desh",
            "दुनिया": "duniya",
            "जगह": "jagah",
            "कहीं": "kahin",
            "जहाँ": "jahaan",
            "वहाँ": "vahaan",
            "यहाँ": "yahaan",
            "सामने": "saamne",
            "पीछे": "peechhe",
            "आगे": "aage",
            "ऊपर": "upar",
            "नीचे": "neeche",
            "दाएँ": "daayen",
            "बाएँ": "baayen",
            "अंदर": "andar",
            "बाहर": "baahar",
            "साथ": "saath",
            "पास": "paas",
            "दूर": "door",
            "पानी": "paani",
            "दूध": "doodh",
            "चाय": "chai",
            "दवा": "dawa",
            "दवाई": "dawaai",
            "किताब": "kitaab",
            "कागज़": "kaagaz",
            "पन्ना": "panna",
            "अख़बार": "akhbaar",
            "पत्रिका": "patrika",
            "चिट्ठी": "chitthi",
            "तस्वीर": "tasveer",
            "गाड़ी": "gaadi",
            "बस": "bus",
            "ट्रेन": "train",
            "हवाईजहाज़": "hawaaijahaaz",
            "साइकिल": "cycle",
            "सड़क": "sadak",
            "रास्ता": "rasta",
            "पुल": "pul",
            "स्टेशन": "station",
            "पार्क": "park",
            "होटल": "hotel",
            "अस्पताल": "aspatal",
            "मंदिर": "mandir",
            "मस्जिद": "masjid",
            "गिरजा": "girja",
            "गुरुद्वारा": "gurudwara",
            "दुकान": "dukaan",
            "बैंक": "bank",
            "डाकखाना": "daakkhana",
            "थाना": "thaana",
            "विद्यालय": "vidyaalay",
            "कॉलेज": "college",
            "अदालत": "adaalat",
            "दफ़्तर": "daftar",
            "चैनल": "channel",
            "सिनेमा": "cinema",
            "थिएटर": "theater",
            "म्यूज़ियम": "museum",
            "पुस्तकालय": "pustakaalay",
            "ब्यूटीपार्लर": "beautyparlour",
            "सैलून": "saloon",
            "जेल": "jail",
            "कब्रिस्तान": "kabristaan",
            "श्मशान": "shmashaan",
            "मेला": "mela",
            "हाट": "haat",
            "बाज़ार": "baazaar",
            "मार्केट": "market",
            "मॉल": "mall",
            "दुकान": "dukaan",
            "किराना": "kiraana",
            "सब्जी": "sabzi",
            "मिठाई": "mithaai",
            "हलवाई": "halwaai",
            "नाई": "naai",
            "दर्जी": "darzi",
            "मोची": "mochi",
            "लुहार": "luhaar",
            "बढ़ई": "badhai",
            "कुम्हार": "kumhaar",
            "जुलाहा": "julaaha",
        }

        # Build reverse lookup for partial matching (after common_words is defined)
        self._build_reverse_lookup()

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
        More conservative approach - only apply well-established patterns.
        """
        if len(result) <= 2:
            return result

        original = result
        result_lower = result.lower()

        # DON'T over-process: keep common verb forms intact
        # Only apply schwa deletion for clear cases

        # Pattern 1: -ana -> -na for infinitives (but be careful)
        # Only apply to longer stems to avoid false positives
        if result_lower.endswith("ana") and len(result) > 5:
            stem = result[:-3]
            # Check stem doesn't end with vowel
            if stem and stem[-1].lower() not in "aeiou":
                # Be conservative: only if stem looks like a verb root
                # Don't apply to: paana, jaana, laana, aana, etc.
                if not any(
                    x in result_lower
                    for x in ["paana", "jaana", "laana", "aana", "gaana"]
                ):
                    result = stem + "na"

        # Pattern 2: Continuous tense forms
        # -ata/-ati/-ate should become -ta/-ti/-te in longer words
        # But NOT for: data, gata, etc.
        if len(result) > 5:
            if result_lower.endswith("ate") and not result_lower.endswith("gate"):
                stem = result[:-3]
                if len(stem) >= 4:
                    result = stem + "te"
            elif result_lower.endswith("ati") and not result_lower.endswith("gati"):
                stem = result[:-3]
                if len(stem) >= 4:
                    result = stem + "ti"
            elif result_lower.endswith("ata") and not result_lower.endswith("gata"):
                stem = result[:-3]
                if len(stem) >= 4:
                    result = stem + "ta"

        # Pattern 3: Feminine forms -ee -> -i
        # Common pattern but be careful with names
        if result_lower.endswith("ee") and len(result) > 4:
            # Check if it's likely a feminine verb form
            # Don't change: Puneet, Sangeet, etc. (keep those with ee)
            if not result_lower.startswith(("p", "s", "r", "n")):
                result = result[:-2] + "i"

        # Pattern 4: Final 'a' deletion - BE VERY CAREFUL
        # Only delete from long words where it's clearly not needed
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
            "khana",
            "pina",
            "sona",
            "rona",
            "hona",
            "lena",
            "dena",
            "aana",
            "jaana",
            "paana",
            "laana",
            "gaana",
            "khana",
            "rahana",
            "kahana",
            "sunana",
            "dekhana",
            "bolana",
            "pita",
            "maata",
            "dadi",
            "nani",
            "dada",
            "nana",
            "beta",
            "beti",
            "bhai",
            "behen",
            "maan",
            "baap",
            "haan",
            "naa",
            "jahan",
            "vahan",
            "yahan",
            "kahan",
            "ki",
            "ka",
            "ke",
            "ko",
            "se",
            "me",
            "ne",
            "he",
        }

        # Only delete final 'a' from longer words (>4 chars) and if not in keep list
        if result_lower.endswith("a") and result_lower not in keep_final_a:
            if len(result) > 4:
                # Check if it's a verb ending
                verb_endings = ("na", "ta", "ti", "te", "ni", "ne", "ya")
                if not result_lower.endswith(verb_endings):
                    # One more check: don't delete if word ends with consonant + a
                    # This preserves words like "karna", "hona"
                    if result_lower[-2] in "aeiou":
                        result = result[:-1]

        # Pattern 5: Reduce triple vowels and excessive doubles
        # aa -> a (but keep in specific words)
        if "aa" in result_lower and len(result) > 5:
            # Be selective: only reduce in longer words
            # Don't reduce: gaana, paana, jaana, laana, haana, shaana, maana
            keep_double_a = [
                "gaana",
                "paana",
                "jaana",
                "laana",
                "haana",
                "shaana",
                "maana",
                "saara",
                "kaale",
                "baarah",
                "saal",
                "daal",
                "kaagaz",
            ]
            if not any(x in result_lower for x in keep_double_a):
                # Reduce only one occurrence
                result = result.replace("aa", "a", 1)

        return result

    def _build_reverse_lookup(self):
        """Build a reverse lookup for pattern-based matching."""
        # This helps find words by their endings
        self.word_by_suffix = {}
        for word, hinglish in self.common_words.items():
            # Index by last 2-4 characters
            for i in range(2, min(5, len(word) + 1)):
                suffix = word[-i:]
                if suffix not in self.word_by_suffix:
                    self.word_by_suffix[suffix] = []
                self.word_by_suffix[suffix].append((word, hinglish))

    def _find_similar_word(self, word: str) -> str | None:
        """
        Try to find a similar word in dictionary using suffix matching.
        This handles variations like tyohaar/tyohar, dukaan/dukaanein etc.
        """
        # Try exact match first
        if word in self.common_words:
            return self.common_words[word]

        # Only use suffix matching for clear plural/oblique forms
        # Check if word ends with known plural/oblique suffixes
        known_suffixes = {
            "ें": "ein",  # dukaan -> dukaanein
            "ों": "on",  # bachcha -> bacchon
            "ीं": "iin",  # thiin
            "ों": "on",
            "एं": "ein",
        }

        for suffix, hinglish_suffix in known_suffixes.items():
            if word.endswith(suffix):
                # Get the base word by removing suffix
                base = word[: -len(suffix)]
                if base in self.common_words:
                    # Combine base form with suffix
                    return self.common_words[base] + hinglish_suffix

        return None

    def _adapt_word_form(
        self, word: str, pattern_word: str, pattern_hinglish: str
    ) -> str:
        """
        Adapt a hinglish pattern to a new word form.
        e.g., if we know 'दुकान' -> 'dukaan', we can infer 'दुकानें' -> 'dukaanein'
        """
        # Simple heuristic: if word is longer, add common plural/oblique endings
        if len(word) > len(pattern_word):
            extra = len(word) - len(pattern_word)
            if word.endswith("ें"):
                return pattern_hinglish + "ein"
            elif word.endswith("ों"):
                return pattern_hinglish + "on"
            elif word.endswith("ी"):
                return pattern_hinglish + "i"
            elif word.endswith("े"):
                return pattern_hinglish + "e"

        return pattern_hinglish

    def _try_suffix_lookup(self, word: str) -> str | None:
        """
        Try to match word by its suffix patterns.
        Helps with conjugated verbs and declined nouns.
        """
        # Try matching last 2-3 characters against known suffixes
        for length in [3, 2]:
            if len(word) >= length:
                suffix = word[-length:]
                if suffix in self.suffix_patterns:
                    # Get the base by removing suffix
                    base = word[:-length]
                    if base in self.common_words:
                        # Combine base form with suffix transliteration
                        return self.common_words[base] + self.suffix_patterns[suffix]

        return None

    def _apply_smart_schwa(self, word: str) -> str:
        """
        Apply intelligent schwa deletion based on word patterns.
        CONSERVATIVE approach - only apply safe, well-established patterns.
        """
        if len(word) <= 2:
            return word

        wl = word.lower()
        original = word

        # DON'T apply aggressive rules here - _apply_schwa_deletion already did the work
        # Only fix specific issues that slip through

        # Rule 1: Fix triple+ vowels (clearly wrong)
        # aaa -> aa, eee -> ee, etc.
        import re

        word = re.sub(r"([aeiou])\1{2,}", r"\1\1", word, flags=re.IGNORECASE)

        # Rule 2: Fix common consonant doubling issues
        # Don't double consonants unnecessarily
        # But preserve valid doubles like: mm, nn, ll, ss, tt
        word = re.sub(r"([b-df-hj-np-tv-z])\1{2,}", r"\1\1", word, flags=re.IGNORECASE)

        # Rule 3: Specific ending fixes for very common errors
        # These are only applied if the word is not in dictionary
        ending_fixes = {
            "aei": "ei",  # dukaaei -> dukaei (but we want dukaanein)
            "aee": "ee",  # gaanee -> ganee (but we want gaana)
        }

        for wrong, right in ending_fixes.items():
            if word.lower().endswith(wrong):
                # Only apply to longer words to avoid breaking short ones
                if len(word) > 5:
                    word = word[: -len(wrong)] + right

        # Rule 4: Preserve dictionary words exactly
        # Check if original form exists in dictionary (case insensitive)
        word_lower = word.lower()
        for hw, he in self.common_words.items():
            if hw.lower() == word_lower:
                return he

        return word

    def _transliterate_word(self, word: str) -> str:
        """
        Transliterate a single Hindi word to Hinglish.
        Uses dictionary lookup first, then pattern matching, then rule-based.
        """
        # Skip empty words
        if not word:
            return ""

        # Check if it's in common words dictionary
        if word in self.common_words:
            return self.common_words[word]

        # Try to find similar word pattern
        similar = self._find_similar_word(word)
        if similar:
            return similar

        # Try suffix-based lookup for known patterns
        suffix_match = self._try_suffix_lookup(word)
        if suffix_match:
            return suffix_match

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
        # Apply both old and new schwa rules for better accuracy
        final_result = self._apply_schwa_deletion(final_result)
        final_result = self._apply_smart_schwa(final_result)

        # Post-processing: fix common issues
        final_result = self._post_process(final_result)

        return final_result

    def _post_process(self, text: str) -> str:
        """
        Post-process to fix common transliteration issues.
        This is the final step to catch common errors.
        """
        import re

        original_text = text
        text_lower = text.lower()

        # Common problematic patterns and their fixes
        # Only apply to whole words or clear patterns
        replacements = {
            # Vowel issues
            "aaee": "aee",  # Error pattern
            "aee": "ae",  # Simplify
            "ooee": "ui",  # Common error
            "eeee": "ee",  # Quadruple e
            "aaaa": "aa",  # Quadruple a
            "eeee": "ee",  # Triple e fix
            "uuuu": "uu",  # Quadruple u
            # Consonant clusters that are commonly wrong
            "kshn": "kshan",  # For words like "kshan" (moment)
            "kshm": "kshm",  # Keep as is
            "tn": "tan",  # Better to have 'tan' than 'tn'
            "dn": "dan",  # Better to have 'dan' than 'dn'
            "pn": "pan",  # Better to have 'pan' than 'pn'
            "gn": "gan",  # Better to have 'gan' than 'gn'
            # English loanwords (common errors)
            "wifai": "wifi",
            "skool": "school",
            "fona": "phone",
            "mobail": "mobile",
            "intar": "inter",
            "neta": "net",
            "dileev": "deliv",
            "kaemp": "camp",
            "kemp": "camp",
            "steshn": "station",
            "stesha": "station",
            "bilding": "building",
            "beech": "beach",
            "helo": "hello",
            "hal": "haal",
            "bhaiya": "bhaiya",
            "bhaiyya": "bhaiya",
            # Common Hindi word fixes
            "tyohara": "tyohaar",
            "dukaana": "dukaan",
            "khanaa": "khana",
            "paanee": "paani",
            "vaalaa": "waala",
            "vaalee": "waali",
            "vaale": "waale",
            # Schwa deletion over-corrections
            "rahana": "rahna",  # Sometimes we want this
            "kahana": "kehna",  # Sometimes we want this
        }

        # Apply replacements conservatively
        for old, new in replacements.items():
            # Only replace if it forms a complete pattern
            # Use word boundaries for short patterns
            if len(old) <= 4:
                # For short patterns, be more careful
                text = re.sub(r"\b" + old + r"\b", new, text, flags=re.IGNORECASE)
            else:
                # For longer patterns, can be more liberal
                text = text.replace(old, new)
                # Also try case-insensitive
                if text == original_text:
                    text = re.sub(old, new, text, flags=re.IGNORECASE)

        # Fix multiple spaces
        text = re.sub(r" +", " ", text)

        # Ensure proper spacing after punctuation
        text = re.sub(r"([.!?])([^ ])", r"\1 \2", text)

        return text

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
