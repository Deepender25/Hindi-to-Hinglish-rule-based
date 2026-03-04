"""
New Test Entities - Comprehensive test suite for edge cases and improvements
"""

import sys

sys.path.insert(
    0, r"C:\Users\yadav\OneDrive\Desktop\projects\Hindi-to-Hinglish\try with kilo"
)

from hinglish_converter import HinglishConverter


def run_tests():
    converter = HinglishConverter()

    # Define new test entities covering various categories
    test_entities = [
        # Edge Cases - Single Characters and Short Words
        {
            "name": "Single Character Words",
            "hindi": "आ ई ऊ ए ओ अं अः",
            "expected": "aa ee oo e o an ah",
        },
        {"name": "Two Character Words", "hindi": "क ख ग घ", "expected": "k kh g gh"},
        # Complex Compound Words (Sandhi)
        {
            "name": "Compound Words - Sandhi",
            "hindi": "पढ़ाई लिखाई खानापानी रहनसहन",
            "expected": "padhaai likhaai khaanapaani rahansahan",
        },
        {
            "name": "Complex Compounds",
            "hindi": "चलचित्र लघुचित्र महानगर प्रधानमंत्री",
            "expected": "chalchitra laghuchitra mahanagar pradhanmantri",
        },
        # Different Verb Tenses
        {
            "name": "Present Tense Verbs",
            "hindi": "खाता है पीती है सोते हैं",
            "expected": "khata hai piti hai sote hain",
        },
        {
            "name": "Past Tense Verbs",
            "hindi": "खाया था पीया था सोया था",
            "expected": "khaya tha piya tha soya tha",
        },
        {
            "name": "Future Tense Verbs",
            "hindi": "खाऊंगा पीऊंगी सोएंगे",
            "expected": "khaaoonga peehoongi soenge",
        },
        {
            "name": "Continuous Tense",
            "hindi": "खा रहा है पी रही है सो रहे हैं",
            "expected": "kha raha hai pi rahi hai so rahe hain",
        },
        # Complex Sentences with Multiple Clauses
        {
            "name": "Complex Sentence 1",
            "hindi": "जब मैं स्कूल गया तो मुझे पता चला कि छुट्टी है।",
            "expected": "jab main school gaya to mujhe pata chala ki chhutti hai.",
        },
        {
            "name": "Complex Sentence 2",
            "hindi": "अगर तुम मेरे साथ आओगे तो हम मिलकर काम करेंगे।",
            "expected": "agar tum mere saath aaoge to hum milkar kaam karenge.",
        },
        # Questions and Interrogatives
        {
            "name": "WH Questions",
            "hindi": "कौन आया? कब आएगा? कहाँ गया? क्यों रोया?",
            "expected": "kaun aaya? kab aaega? kahan gaya? kyun roya?",
        },
        {
            "name": "Yes/No Questions",
            "hindi": "क्या तुम आओगे? क्या यह सच है?",
            "expected": "kya tum aaoge? kya yeh sach hai?",
        },
        # Numbers and Counting
        {
            "name": "Numbers",
            "hindi": "एक दो तीन चार पाँच",
            "expected": "ek do teen chaar paanch",
        },
        {
            "name": "Ordinal Numbers",
            "hindi": "पहला दूसरा तीसरा",
            "expected": "pehla doosra teesra",
        },
        # Honorifics and Respect Levels
        {
            "name": "Respectful Speech",
            "hindi": "आप कैसे हैं? वे कहाँ गए?",
            "expected": "aap kaise hain? ve kahan gaye?",
        },
        {
            "name": "Familiar Speech",
            "hindi": "तुम कैसे हो? वह कहाँ गया?",
            "expected": "tum kaise ho? vah kahan gaya?",
        },
        # Modern/Digital Terms
        {
            "name": "Social Media Terms",
            "hindi": "वीडियो वायरल हो गया। लाइक शेयर सब्सक्राइब करें।",
            "expected": "video viral ho gaya. like share subscribe karein.",
        },
        {
            "name": "Tech Terms",
            "hindi": "वाईफाई पासवर्ड डालो। ब्लूटूथ चालू करो।",
            "expected": "wifi password daalo. bluetooth chaalu karo.",
        },
        # Food and Cuisine
        {
            "name": "Indian Food Items",
            "hindi": "समोसा कचौड़ी जलेबी रसगुल्ला",
            "expected": "samosa kachauri jalebi rasgulla",
        },
        {
            "name": "Cooking Terms",
            "hindi": "भूनना तलना पकाना काटना",
            "expected": "bhuunna talna pakaana kaatna",
        },
        # Emotions and Expressions
        {
            "name": "Complex Emotions",
            "hindi": "मैं हैरान हूँ। वह निराश था। हम उत्साहित हैं।",
            "expected": "main hairaan hoon. vah niraash tha. hum utsaahit hain.",
        },
        # Negations
        {
            "name": "Negation Forms",
            "hindi": "नहीं जाऊंगा मत करो बिना सोचे",
            "expected": "nahin jaoonga mat karo bina soche",
        },
        # Postpositions
        {
            "name": "Postpositions",
            "hindi": "घर में स्कूल से दोस्त के साथ",
            "expected": "ghar mein school se dost ke saath",
        },
        # Pronouns in All Forms
        {
            "name": "Pronouns All Forms",
            "hindi": "मैं मेरा मुझे तू तेरा तुझे तुम तुम्हारा",
            "expected": "main mera mujhe tu tera tujhe tum tumhara",
        },
        # Adjectives in All Genders
        {
            "name": "Adjectives Masculine/Feminine",
            "hindi": "बड़ा बड़ी बड़े छोटा छोटी छोटे",
            "expected": "bada badi bade chhota chhoti chhote",
        },
        # Common Phrases and Idioms
        {
            "name": "Common Phrases",
            "hindi": "धीरे धीरे धीरज रखो आराम से",
            "expected": "dheere dheere dhiraj rakho aaram se",
        },
        {
            "name": "Idiomatic Expressions",
            "hindi": "दिल से शुक्रिया मुंह फेर लेना हाथ धोना",
            "expected": "dil se shukriya munh pher lena haath dhona",
        },
        # Half Consonants (Chained Consonants)
        {
            "name": "Half Consonants",
            "hindi": "प्रस्थान प्रयास क्रिया ग्राम",
            "expected": "prasthaan prayas kriya graam",
        },
        # Words with Nukta (ड़ ढ़ फ़ ज़)
        {
            "name": "Words with Nukta",
            "hindi": "पेड़ घड़ी अफ़सर ज़मीन",
            "expected": "ped gharhi afsar zameen",
        },
        # Long Complex Sentences
        {
            "name": "Long Sentence 1",
            "hindi": "मेरे छोटे भाई ने कल स्कूल में एक नई कहानी सुनाई जो बहुत मजेदार थी।",
            "expected": "mere chhote bhai ne kal school mein ek nai kahaani sunaai jo bahut mazedaar thi.",
        },
        {
            "name": "Long Sentence 2",
            "hindi": "जब हम दिल्ली घूमने गए तो हमने लाल किला, इंडिया गेट और कुतुब मीनार देखा।",
            "expected": "jab hum dilli ghoomne gaye to hamne laal qila, india gate aur qutub minaar dekha.",
        },
        # Edge Cases with Punctuation
        {
            "name": "Punctuation Test",
            "hindi": "नमस्ते! आप कैसे हैं? मैं ठीक हूं...",
            "expected": "namaste! aap kaise hain? main theek hoon...",
        },
        # Names and Places
        {
            "name": "Indian Names",
            "hindi": "राम श्याम सीता गीता",
            "expected": "ram shyam sita geeta",
        },
        {
            "name": "Place Names",
            "hindi": "मुंबई दिल्ली कोलकाता चेन्नई",
            "expected": "mumbai dilli kolkata chennai",
        },
        # Religious and Cultural Terms
        {
            "name": "Religious Terms",
            "hindi": "मंदिर मस्जिद गुरुद्वारा चर्च",
            "expected": "mandir masjid gurudwara church",
        },
        # Transportation
        {
            "name": "Transport Modes",
            "hindi": "साइकिल मोटरसाइकिल स्कूटर कार बस",
            "expected": "cycle motorcycle scooter car bus",
        },
        # Body Parts
        {
            "name": "Body Parts",
            "hindi": "सिर आँख नाक कान हाथ पैर",
            "expected": "sir aankh naak kaan haath pair",
        },
        # Colors
        {
            "name": "Colors",
            "hindi": "लाल हरा नीला पीला काला सफेद",
            "expected": "laal hara neela peela kaala safed",
        },
        # Time Expressions
        {
            "name": "Time Expressions",
            "hindi": "आज कल सुबह शाम रात दिन",
            "expected": "aaj kal subah shaam raat din",
        },
        # Professional Titles
        {
            "name": "Professional Titles",
            "hindi": "डॉक्टर इंजीनियर वकील शिक्षक",
            "expected": "doctor engineer vakeel shikshak",
        },
        # Relationship Terms
        {
            "name": "Extended Family",
            "hindi": "चाचा ताऊ मामा फुआ मौसी",
            "expected": "chacha tau mama phua mausi",
        },
        # Adverbs and Modifiers
        {
            "name": "Adverbs",
            "hindi": "धीरे तेज जल्दी धीरे से",
            "expected": "dheere tej jaldi dheere se",
        },
        # Conditional Sentences
        {
            "name": "Conditional Sentences",
            "hindi": "अगर वर्षा हुई तो मैं नहीं जाऊंगा।",
            "expected": "agar varsha hui to main nahin jaoonga.",
        },
        # Passive Voice
        {
            "name": "Passive Voice",
            "hindi": "खाना बनाया गया। पत्र लिखा गया।",
            "expected": "khana banaya gaya. patra likha gaya.",
        },
        # Imperative/Commands
        {
            "name": "Commands",
            "hindi": "आओ! जाओ! देखो! सुनो! रुको!",
            "expected": "aao! jao! dekho! suno! ruko!",
        },
    ]

    # Run tests
    results = []
    output_lines = []
    output_lines.append("=" * 80)
    output_lines.append("NEW TEST ENTITIES - COMPREHENSIVE TEST SUITE")
    output_lines.append("=" * 80)
    output_lines.append("")

    for i, test in enumerate(test_entities, 1):
        hindi = test["hindi"]
        expected = test["expected"]
        result = converter.convert(hindi)

        # Calculate word-level accuracy
        expected_words = expected.split()
        result_words = result.split()

        if len(expected_words) > 0:
            matches = sum(1 for e, r in zip(expected_words, result_words) if e == r)
            total = max(len(expected_words), len(result_words))
            accuracy = (matches / total) * 100
        else:
            accuracy = 100 if result == expected else 0

        status = "PASS" if accuracy >= 80 else "FAIL"

        results.append(
            {
                "num": i,
                "name": test["name"],
                "accuracy": accuracy,
                "status": status,
                "hindi": hindi,
                "expected": expected,
                "got": result,
            }
        )

        # Print result
        output_lines.append(f"Test #{i:02d}: {test['name']}")
        output_lines.append(f"Accuracy: {accuracy:.1f}% - {status}")

        if accuracy < 100:
            output_lines.append(f"Expected: {expected}")
            output_lines.append(f"Got:      {result}")
        output_lines.append("")

    # Print summary
    output_lines.append("=" * 80)
    output_lines.append("SUMMARY")
    output_lines.append("=" * 80)

    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = len(results) - passed
    avg_accuracy = sum(r["accuracy"] for r in results) / len(results)

    output_lines.append(f"Total Tests: {len(results)}")
    output_lines.append(f"Passed (≥80%): {passed}")
    output_lines.append(f"Failed (<80%): {failed}")
    output_lines.append(f"Average Accuracy: {avg_accuracy:.1f}%")
    output_lines.append("")

    # List failed tests
    if failed > 0:
        output_lines.append("FAILED TESTS:")
        for r in results:
            if r["status"] == "FAIL":
                output_lines.append(
                    f"  #{r['num']:02d}: {r['name']} ({r['accuracy']:.1f}%)"
                )
                output_lines.append(f"      Hindi: {r['hindi']}")
                output_lines.append(f"      Expected: {r['expected']}")
                output_lines.append(f"      Got:      {r['got']}")
                output_lines.append("")

    # Save output to file
    with open("test_new_entities_results.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))

    # Print summary only (ASCII)
    print("=" * 80)
    print("NEW TEST ENTITIES - SUMMARY")
    print("=" * 80)
    print(f"Total Tests: {len(results)}")
    print(f"Passed (>=80%): {passed}")
    print(f"Failed (<80%): {failed}")
    print(f"Average Accuracy: {avg_accuracy:.1f}%")
    print()
    print("Full results saved to: test_new_entities_results.txt")

    return results


if __name__ == "__main__":
    results = run_tests()
