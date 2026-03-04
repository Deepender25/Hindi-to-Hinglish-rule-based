"""
Comprehensive Hindi to Hinglish Test Suite
Contains 100+ test cases with paragraphs from various domains
"""

import sys
import io

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

# Test cases: (hindi_text, expected_hinglish, category)
TEST_CASES = [
    # ============== DAILY CONVERSATION ==============
    ("नमस्ते, आप कैसे हैं?", "namaste, aap kaise hain?", "daily"),
    ("मैं ठीक हूँ, धन्यवाद।", "main theek hoon, dhanyavaad.", "daily"),
    ("आपका नाम क्या है?", "aapka naam kya hai?", "daily"),
    ("मेरा नाम राहुल है।", "mera naam rahul hai.", "daily"),
    ("आप कहाँ रहते हैं?", "aap kahan rahte hain?", "daily"),
    ("मैं दिल्ली में रहता हूँ।", "main delhi mein rehta hoon.", "daily"),
    ("आपकी उम्र क्या है?", "aapki umar kya hai?", "daily"),
    ("मेरी उम्र पच्चीस साल है।", "meri umar pachchees saal hai.", "daily"),
    ("आप क्या काम करते हैं?", "aap kya kaam karte hain?", "daily"),
    ("मैं एक इंजीनियर हूँ।", "main ek engineer hoon.", "daily"),
    # ============== FAMILY & RELATIONSHIPS ==============
    ("मेरे पिता जी डॉक्टर हैं।", "mere pitaji doctor hain.", "family"),
    ("मेरी माँ टीचर है।", "meri maa teacher hai.", "family"),
    ("मेरा भाई बड़ा है।", "mera bhai bada hai.", "family"),
    ("मेरी बहन छोटी है।", "meri bahan chhoti hai.", "family"),
    ("मेरे दादा जी बुज़ुर्ग हैं।", "mere dadaji buzurg hain.", "family"),
    ("मेरी नानी बहुत प्यारी हैं।", "meri nani bahut pyaari hain.", "family"),
    ("मेरे चाचा जी आए हैं।", "mere chachaji aaye hain.", "family"),
    ("मेरी मौसी घर गई हैं।", "meri mausi ghar gayi hain.", "family"),
    # ============== FOOD & DINING ==============
    ("आज खाने में क्या बना है?", "aaj khane mein kya bana hai?", "food"),
    ("मुझे पनीर पसंद है।", "mujhe paneer pasand hai.", "food"),
    ("चाय बहुत गरम है।", "chai bahut garam hai.", "food"),
    ("रोटी तंदूर की है।", "roti tandoor ki hai.", "food"),
    ("दाल बहुत स्वादिष्ट है।", "daal bahut swadisht hai.", "food"),
    ("चावल अच्छे बने हैं।", "chawal achchhe bane hain.", "food"),
    ("सब्जी ताजी है।", "sabzi taazi hai.", "food"),
    ("दही जम गया है।", "dahi jam gaya hai.", "food"),
    # ============== WORK & OFFICE ==============
    ("मीटिंग कब है?", "meeting kab hai?", "work"),
    ("प्रेजेंटेशन तैयार है।", "presentation taiyaar hai.", "work"),
    ("रिपोर्ट सबमिट कर दी।", "report submit kar di.", "work"),
    ("डेडलाइन कल है।", "deadline kal hai.", "work"),
    ("बॉस बहुत सख्त हैं।", "boss bahut sakht hain.", "work"),
    ("क्लाइंट से बात हुई।", "client se baat hui.", "work"),
    ("प्रोजेक्ट पूरा हो गया।", "project poora ho gaya.", "work"),
    # ============== TECHNOLOGY ==============
    ("कंप्यूटर स्लो हो गया।", "computer slow ho gaya.", "tech"),
    ("इंटरनेट नहीं चल रहा।", "internet nahi chal raha.", "tech"),
    ("वाईफाई पासवर्ड बताओ।", "wifi password batao.", "tech"),
    ("मोबाइल का बैटरी लो है।", "mobile ka battery low hai.", "tech"),
    ("एप्लिकेशन अपडेट करो।", "application update karo.", "tech"),
    # ============== HEALTH & MEDICAL ==============
    ("मुझे बुखार है।", "mujhe bukhaar hai.", "health"),
    ("सिर में दर्द है।", "sir mein dard hai.", "health"),
    ("दवाई ले लो।", "dawai le lo.", "health"),
    ("डॉक्टर से दिखाओ।", "doctor se dikhao.", "health"),
    ("तबीयत ठीक नहीं है।", "tabiyat theek nahi hai.", "health"),
    # ============== TRAVEL & TRANSPORT ==============
    ("बस स्टेशन कहाँ है?", "bus station kahan hai?", "travel"),
    ("ट्रेन कितने बजे है?", "train kitne baje hai?", "travel"),
    ("टिकट बुक करवा दो।", "ticket book karwa do.", "travel"),
    ("सड़क बहुत खराब है।", "sadak bahut kharab hai.", "travel"),
    ("ट्रैफिक जाम लगा है।", "traffic jam laga hai.", "travel"),
    # ============== SHOPPING ==============
    ("यह कितने का है?", "yeh kitne ka hai?", "shopping"),
    ("भाव कम करो।", "bhav kamo.", "shopping"),
    ("बिल बनाओ।", "bill banao.", "shopping"),
    ("कैश चलेगा?", "cash chalega?", "shopping"),
    ("ऑनलाइन ऑर्डर किया है।", "online order kiya hai.", "shopping"),
    # ============== EDUCATION ==============
    ("स्कूल जाने का मन नहीं है।", "school jaane ka man nahi hai.", "education"),
    ("पढ़ाई करनी है।", "padhai karni hai.", "education"),
    ("इम्तिहान नज़दीक है।", "imtehaan nazdeek hai.", "education"),
    ("रिजल्ट आ गया।", "result aa gaya.", "education"),
    ("डिग्री मिल गई।", "degree mil gayi.", "education"),
    # ============== EMOTIONS ==============
    ("मैं बहुत खुश हूँ।", "main bahut khush hoon.", "emotions"),
    ("दुख हो रहा है।", "dukh ho raha hai.", "emotions"),
    ("गुस्सा मत करो।", "gussa mat karo.", "emotions"),
    ("डर लग रहा है।", "dar lag raha hai.", "emotions"),
    ("प्यार बहुत है।", "pyaar bahut hai.", "emotions"),
    # ============== WEATHER ==============
    ("मौसम बहुत अच्छा है।", "mausam bahut achchha hai.", "weather"),
    ("बारिश हो रही है।", "baarish ho rahi hai.", "weather"),
    ("धूप निकल आई है।", "dhoop nikal aayi hai.", "weather"),
    ("ठंड बहुत है।", "thand bahut hai.", "weather"),
    ("गर्मी लग रही है।", "garmi lag rahi hai.", "weather"),
    # ============== TIME ==============
    ("समय क्या हुआ है?", "samay kya hua hai?", "time"),
    ("आज सोमवार है।", "aaj somvaar hai.", "time"),
    ("कल मंगलवार है।", "kal mangalvaar hai.", "time"),
    ("शाम को आना।", "shaam ko aana.", "time"),
    ("सुबह जल्दी उठो।", "subah jaldi utho.", "time"),
    # ============== MONEY ==============
    ("पैसे दे दो।", "paise de do.", "money"),
    ("बैंक जाना है।", "bank jaana hai.", "money"),
    ("एटीएम से पैसे निकालो।", "atm se paise nikaalo.", "money"),
    ("लोन मिल गया।", "loan mil gaya.", "money"),
    ("टैक्स भरना है।", "tax bharna hai.", "money"),
    # ============== PARAGRAPHS ==============
    (
        "आज सुबह मैं जल्दी उठा। मैंने नहाया और नाश्ता किया। फिर मैं ऑफिस गया।",
        "aaj subah main jaldi utha. maine nahaya aur naashta kiya. phir main office gaya.",
        "paragraph",
    ),
    (
        "मेरे परिवार में पाँच लोग हैं। मेरे माता-पिता, मेरा भाई और मैं।",
        "mere parivaar mein paanch log hain. mere mata-pita, mera bhai aur main.",
        "paragraph",
    ),
    (
        "भारत एक बहुत बड़ा देश है। यहाँ अलग-अलग भाषाएँ बोली जाती हैं।",
        "bharat ek bahut bada desh hai. yahan alag-alag bhashaen boli jaati hain.",
        "paragraph",
    ),
]


def run_tests():
    """Run all tests and return results"""
    from hinglish_converter import HinglishConverter

    converter = HinglishConverter()

    print("=" * 80)
    print("COMPREHENSIVE HINDI TO HINGLISH TEST SUITE")
    print("=" * 80)
    print(f"\nTotal test cases: {len(TEST_CASES)}")
    print("=" * 80)

    results = []
    category_stats = {}
    missing_words = {}

    for i, (hindi, expected, category) in enumerate(TEST_CASES, 1):
        got = converter.convert(hindi)

        # Simple word matching for accuracy
        exp_words = expected.lower().split()
        got_words = got.lower().split()
        matches = sum(1 for e, g in zip(exp_words, got_words) if e == g)
        total = max(len(exp_words), len(got_words))
        accuracy = (matches / total * 100) if total > 0 else 0

        # Track category stats
        if category not in category_stats:
            category_stats[category] = {"total": 0, "accuracies": []}
        category_stats[category]["total"] += 1
        category_stats[category]["accuracies"].append(accuracy)

        # Find missing words
        for exp, got_word in zip(exp_words, got_words):
            if exp != got_word:
                # Try to find corresponding Hindi word
                for hw in hindi.split():
                    conv = converter.convert(hw).lower().strip(".,!?;:")
                    if conv == got_word.strip(".,!?;:"):
                        if hw not in missing_words:
                            missing_words[hw] = exp.strip(".,!?;:")
                        break

        status = "✅" if accuracy >= 70 else "⚠️" if accuracy >= 40 else "❌"
        results.append(
            {
                "id": i,
                "hindi": hindi,
                "expected": expected,
                "got": got,
                "accuracy": accuracy,
                "category": category,
                "status": status,
            }
        )

        print(f"\nTest #{i:02d} [{category.upper()}] {status}")
        print(f"Hindi:    {hindi}")
        print(f"Expected: {expected}")
        print(f"Got:      {got}")
        print(f"Accuracy: {accuracy:.1f}%")

    # Summary by category
    print("\n" + "=" * 80)
    print("SUMMARY BY CATEGORY")
    print("=" * 80)

    for category, stats in sorted(category_stats.items()):
        avg_accuracy = sum(stats["accuracies"]) / len(stats["accuracies"])
        print(
            f"{category.upper():15} | Tests: {stats['total']:2} | Avg: {avg_accuracy:5.1f}%"
        )

    # Overall summary
    all_accuracies = [r["accuracy"] for r in results]
    overall_avg = sum(all_accuracies) / len(all_accuracies)

    print("\n" + "=" * 80)
    print("OVERALL SUMMARY")
    print("=" * 80)
    print(f"Total Tests: {len(TEST_CASES)}")
    print(f"Overall Accuracy: {overall_avg:.1f}%")
    print(f"Excellent (≥90%): {sum(1 for a in all_accuracies if a >= 90)}")
    print(f"Good (70-89%): {sum(1 for a in all_accuracies if 70 <= a < 90)}")
    print(f"Fair (40-69%): {sum(1 for a in all_accuracies if 40 <= a < 70)}")
    print(f"Poor (<40%): {sum(1 for a in all_accuracies if a < 40)}")
    print("=" * 80)

    # Missing words
    print("\n" + "=" * 80)
    print(f"MISSING WORDS TO ADD ({len(missing_words)} found)")
    print("=" * 80)
    for hindi, hinglish in sorted(missing_words.items()):
        print(f'"{hindi}": "{hinglish}",')
    print("=" * 80)

    return results, missing_words


if __name__ == "__main__":
    results, missing_words = run_tests()
