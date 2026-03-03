"""
Extended Test Suite for Hindi to Hinglish Converter
Additional 50+ test cases covering diverse domains
"""

import sys
import io
from hinglish_converter import HinglishConverter

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

# Extended test cases covering new domains
ADDITIONAL_TEST_CASES = [
    # Business & Professional
    {
        "name": "Business Meeting",
        "hindi": "आज की मीटिंग बहुत अहम है। हमें क्लाइंट को प्रेजेंटेशन दिखानी है। बजट पर चर्चा होगी। डील फाइनल करनी है।",
        "expected": "aaj ki meeting bahut aham hai. hamein client ko presentation dikhaani hai. budget par charcha hogi. deal final karni hai.",
    },
    {
        "name": "Email Writing",
        "hindi": "प्रिय सर, मैं आपको सूचित करना चाहता हूं कि रिपोर्ट तैयार है। कृप्या इसे देखें और अप्रूव करें। धन्यवाद।",
        "expected": "priya sir, main aapko soochit karna chahta hoon ki report taiyaar hai. kripya ise dekhen aur approve karen. dhanyavaad.",
    },
    {
        "name": "Job Application",
        "hindi": "मैं इस पद के लिए आवेदन करना चाहता हूं। मेरे पास पांच साल का अनुभव है। मेरी योग्यता इस जॉब के अनुकूल है।",
        "expected": "main is pad ke liye avedan karna chahta hoon. mere paas paanch saal ka anubhav hai. meri yogyata is job ke anukool hai.",
    },
    # Technology & Digital
    {
        "name": "Social Media Post",
        "hindi": "इस फोटो को लाइक और शेयर करें। मेरे चैनल को सब्सक्राइब करें। कमेंट में बताएं आपको कैसा लगा।",
        "expected": "is photo ko like aur share karen. mere channel ko subscribe karen. comment mein batayen aapko kaisa laga.",
    },
    {
        "name": "Online Shopping",
        "hindi": "यह प्रोडक्ट बहुत अच्छा है। रिव्यू पढ़कर मैंने ऑर्डर किया। कैश ऑन डिलीवरी का ऑप्शन है। रिटर्न पॉलिसी भी है।",
        "expected": "yah product bahut achha hai. review padhkar maine order kiya. cash on delivery ka option hai. return policy bhi hai.",
    },
    {
        "name": "Technical Support",
        "hindi": "मेरा कंप्यूटर स्लो हो गया है। सॉफ्टवेयर अपडेट करना है। वायरस स्कैन करें। डेटा बैकअप लें।",
        "expected": "mera computer slow ho gaya hai. software update karna hai. virus scan karen. data backup len.",
    },
    # Education & Learning
    {
        "name": "Online Class",
        "hindi": "आज ऑनलाइन क्लास में टेस्ट होगा। वीडियो कॉल जॉइन करें। म्यूट करके रखें। क्विज़ में हिस्सा लें।",
        "expected": "aaj online class mein test hoga. video call join karen. mute karke rahen. quiz mein hissa len.",
    },
    {
        "name": "Homework Help",
        "hindi": "यह मैथ का सवाल समझ नहीं आया। फॉर्मूला क्या है? स्टेप बाई स्टेप बताओ। एग्जाम के लिए तैयारी करनी है।",
        "expected": "yah math ka sawaal samajh nahi aaya. formula kya hai? step by step batao. exam ke liye taiyaari karni hai.",
    },
    {
        "name": "Library Visit",
        "hindi": "मुझे यह किताब जारी करवानी है। कार्ड दिखाएं। रिन्यूअल करवाएं। फाइन तो नहीं है ना?",
        "expected": "mujhe yah kitaab jaari karwaani hai. card dikhaayen. renewal karwaayen. fine to nahi hai na?",
    },
    # Healthcare & Medical
    {
        "name": "Pharmacy Visit",
        "hindi": "यह दवा दे दीजिए। प्रिस्क्रिप्शन देख लीजिए। जेनेरिक दवा मिलेगी क्या? किन्ने दिन की डोज है?",
        "expected": "yah dawa de dijiye. prescription dekh lijiye. generic dawa milegi kya? kitne din ki dose hai?",
    },
    {
        "name": "Medical Test",
        "hindi": "ब्लड टेस्ट करवाना है। फास्टिंग है। रिपोर्ट कब आएगी? डॉक्टर को दिखानी होगी।",
        "expected": "blood test karwaana hai. fasting hai. report kab aayegi? doctor ko dikhaani hogi.",
    },
    {
        "name": "Mental Health",
        "hindi": "मैं बहुत तनाव में हूं। नींद नहीं आती। काउंसलर से बात करनी चाहिए। मेडिटेशन करूं क्या?",
        "expected": "main bahut tanaav mein hoon. neend nahi aati. counselor se baat karni chahiye. meditation karoon kya?",
    },
    # Entertainment & Media
    {
        "name": "Watching TV",
        "hindi": "आज नया सीरियल शुरू होगा। रिमोट दो। वॉल्यूम बढ़ाओ। चैनल बदलो। रिकॉर्ड कर लो।",
        "expected": "aaj naya serial shuru hoga. remote do. volume badhaao. channel badlo. record kar lo.",
    },
    {
        "name": "Concert Experience",
        "hindi": "कल कॉन्सर्ट में गए। सिंगर ने बहुत अच्छा गाया। क्राउड बहुत था। लाइट्स बहुत सुंदर थीं। एंजॉय किया।",
        "expected": "kal concert mein gaye. singer ne bahut achha gaaya. crowd bahut tha. lights bahut sundar thiin. enjoy kiya.",
    },
    {
        "name": "Gaming Session",
        "hindi": "यह गेम बहुत मजेदार है। लेवल क्रॉस करो। कंट्रोलर दो। मल्टीप्लेयर मोड खेलेंगे।",
        "expected": "yah game bahut mazedaar hai. level cross karo. controller do. multiplayer mode khelenge.",
    },
    # Sports & Fitness
    {
        "name": "Gym Workout",
        "hindi": "आज जिम जाएंगे। वेट लिफ्टिंग करेंगे। प्रोटीन शेक पिएंगे। ट्रेनर से मदद लेंगे।",
        "expected": "aaj gym jaayenge. weight lifting karenge. protein shake piyenge. trainer se madad lenge.",
    },
    {
        "name": "Yoga Session",
        "hindi": "सुबह योग करेंगे। मेडिटेशन करेंगे। शवासन में लेटेंगे। माइंड शांत होगा।",
        "expected": "subah yog karenge. meditation karenge. shavaasan mein letenge. mind shaant hoga.",
    },
    {
        "name": "Football Match",
        "hindi": "आज मैच है। गोलकीपर तैयार है। रेफरी ने सीटी बजाई। पेनाल्टी शूटआउट होगा।",
        "expected": "aaj match hai. goalkeeper taiyaar hai. referee ne seeti bajaai. penalty shootout hoga.",
    },
    # Travel & Tourism
    {
        "name": "Airport Check-in",
        "hindi": "बोर्डिंग पास दिखाएं। पासपोर्ट चेक करें। सीट बेल्ट बांधें। फ्लाइट टेक ऑफ होगी।",
        "expected": "boarding paas dikhaayen. passport check karen. seat belt baandhen. flight take off hogi.",
    },
    {
        "name": "Hotel Stay",
        "hindi": "रूम सर्विस बुलाओ। तौलिए बदलवाएं। एसी ठीक करवाएं। चेकआउट टाइम क्या है?",
        "expected": "room service bulaao. tauliye badalwaayen. ac theek karwaayen. checkout time kya hai?",
    },
    {
        "name": "Sightseeing",
        "hindi": "आज म्यूजियम जाएंगे। गाइड हायर करेंगे। हिस्ट्री देखेंगे। फोटो खींचेंगे।",
        "expected": "aaj museum jaayenge. guide hire karenge. history dekhenge. photo kheenchenge.",
    },
    # Food & Dining
    {
        "name": "Street Food",
        "hindi": "गोलगप्पे खाएंगे। चटनी डालो। पानी पुरी लो। स्वाद बहुत अच्छा है।",
        "expected": "golgappe khaayenge. chatni daalo. paani puri lo. swaad bahut achha hai.",
    },
    {
        "name": "Fine Dining",
        "hindi": "वेटर, मेन्यू दो। स्टार्टर में क्या है? वाइन लिस्ट दिखाओ। डेजर्ट अलग से लाओ।",
        "expected": "waiter, menu do. starter mein kya hai? wine list dikhaao. dessert alag se laao.",
    },
    {
        "name": "Cooking Recipe",
        "hindi": "प्याज भूनो। मसाला डालो। दम पर रखो। गार्निश करो। सर्व करो।",
        "expected": "pyaaj bhoono. masaala daalo. dam par rakho. garnish karo. serve karo.",
    },
    # Shopping & Retail
    {
        "name": "Bargaining",
        "hindi": "भैया, दाम कम करो। सस्ता दो। फिक्स प्राइस है क्या? पैसे नहीं हैं इतने।",
        "expected": "bhaiya, daam kam karo. sasta do. fix price hai kya? paise nahi hain itne.",
    },
    {
        "name": "Return Policy",
        "hindi": "यह साइज़ छोटा है। एक्सचेंज करवाना है। बिल लाया हूं। रिफंड मिलेगा क्या?",
        "expected": "yah size chhota hai. exchange karwaana hai. bill laaya hoon. refund milega kya?",
    },
    # Relationships & Social
    {
        "name": "Wedding Invitation",
        "hindi": "मेरी शादी में जरूर आना। बरात शाम को निकलेगी। डीजे पर डांस करेंगे। डिनर रात को होगा।",
        "expected": "meri shaadi mein zaroor aana. baaraat shaam ko niklegi. dj par dance karenge. dinner raat ko hoga.",
    },
    {
        "name": "Condolence Message",
        "hindi": "दुख की घड़ी में साथ हूं। भगवान उनकी आत्मा को शांति दे। हिम्मत रखो। संवेदनाएं।",
        "expected": "dukh ki ghadi mein saath hoon. bhagwan unki aatma ko shaanti de. himmat rakho. samvedanaayen.",
    },
    {
        "name": "Congratulations",
        "hindi": "बधाई हो! सफलता मुबारक। तरक्की हो। नई जॉब की बधाई। पार्टी दो।",
        "expected": "badhaai ho! safalta mubaarak. taraqqi ho. nayi job ki badhaai. party do.",
    },
    # Emergency & Safety
    {
        "name": "Emergency Call",
        "hindi": "मदद चाहिए। एक्सीडेंट हो गया। एंबुलेंस बुलाओ। फायर ब्रिगेड को फोन करो। पुलिस बुलाओ।",
        "expected": "madad chahiye. accident ho gaya. ambulance bulaao. fire brigade ko phone karo. police bulaao.",
    },
    {
        "name": "First Aid",
        "hindi": "पट्टी बांधो। कट लगा है। खून बह रहा है। डिसइंफेक्टेंट लगाओ।",
        "expected": "patti baandho. kat laga hai. khoon bah raha hai. disinfectant lagaao.",
    },
    # Finance & Banking
    {
        "name": "Loan Application",
        "hindi": "होम लोन चाहिए। इंटरेस्ट रेट क्या है? ईएमआई कितनी होगी? डॉक्यूमेंट्स चाहिए।",
        "expected": "home loan chahiye. interest rate kya hai? emi kitni hogi? documents chahiye.",
    },
    {
        "name": "Investment Talk",
        "hindi": "शेयर मार्केट में निवेश करेंगे। म्यूचुअल फंड में डालेंगे। सिप शुरू करेंगे। रिटर्न अच्छा होगा।",
        "expected": "share market mein nivesh karenge. mutual fund mein daalenge. sip shuru karenge. return achha hoga.",
    },
    # Home & Maintenance
    {
        "name": "Plumber Visit",
        "hindi": "नल टपक रहा है। पाइप लीक है। टैंक साफ करो। मोटर ठीक करो।",
        "expected": "nal tapak raha hai. pipe leak hai. tank saaf karo. motor theek karo.",
    },
    {
        "name": "Electrician Visit",
        "hindi": "लाइट नहीं जल रही। वायरिंग खराब है। एमसीबी उड़ गई। फ्यूज बदलो।",
        "expected": "light nahi jal rahi. wiring kharaab hai. mcb ud gayi. fuse badlo.",
    },
    # Government & Legal
    {
        "name": "Document Work",
        "hindi": "आधार कार्ड अपडेट करवाना है। पैन कार्ड लिंक करना है। डिजिटल सिग्नेचर चाहिए।",
        "expected": "aadhaar card update karwaana hai. pan card link karna hai. digital signature chahiye.",
    },
    {
        "name": "Court Visit",
        "hindi": "वकील से मिलना है। केस की सुनवाई है। बेल मिल गई। जमानत हो गई।",
        "expected": "vakeel se milna hai. case ki sunvaai hai. bail mil gayi. jamaanat ho gayi.",
    },
    # Nature & Environment
    {
        "name": "Gardening",
        "hindi": "पौधे लगाएंगे। मिट्टी खोदेंगे। पानी देंगे। खाद डालेंगे। फूल खिलेंगे।",
        "expected": "paudhe lagaayenge. mitti kodenenge. paani denge. khaad daalenge. phool khilen ge.",
    },
    {
        "name": "Weather Alert",
        "hindi": "तूफान आएगा। बारिश होगी। बिजली कड़केगी। घर में रहो। सुरक्षित रहो।",
        "expected": "toofaanaayega. baarish hogi. bijli kadkegi. ghar mein raho. surakshit raho.",
    },
    # Fashion & Beauty
    {
        "name": "Shopping for Clothes",
        "hindi": "यह ड्रेस अच्छी है। फिटिंग रूम कहां है? ट्रायल करूं क्या? कलर और दिखाओ।",
        "expected": "yah dress achhi hai. fitting room kahan hai? trial karoon kya? colour aur dikhaao.",
    },
    {
        "name": "Salon Visit",
        "hindi": "हैरकट करवाना है। बियर्ड ट्रिम करो। फेशियल करवाएंगे। मसाज दो।",
        "expected": "haircut karwaana hai. beard trim karo. facial karwaayenge. masaaj do.",
    },
    # Vehicles & Transport
    {
        "name": "Car Service",
        "hindi": "ऑयल चेंज करवाना है। ब्रेक ठीक करो। टायर चेक करो। पेट्रोल भरो।",
        "expected": "oil change karwaana hai. break theek karo. tyre check karo. petrol bharo.",
    },
    {
        "name": "Traffic Police",
        "hindi": "लाइसेंस दिखाओ। हेलमेट पहनो। चालान काट दिया। सिग्नल तोड़ा है।",
        "expected": "license dikhaao. helmet pahano. chalaan kaat diya. signal toda hai.",
    },
    # Festivals & Celebrations
    {
        "name": "Holi Celebration",
        "hindi": "होली खेलेंगे। रंग लगाएंगे। गुजिया खाएंगे। भांग पिएंगे। नाचेंगे गाएंगे।",
        "expected": "holi khelenge. rang lagaayenge. gujiya khaayenge. bhaang piyenge. naachenge gaayenge.",
    },
    {
        "name": "Eid Celebration",
        "hindi": "ईद मुबारक। सेवइयां बनाएंगे। नमाज पढ़ेंगे। बकरीद पर कुर्बानी होगी।",
        "expected": "eed mubaarak. sevaiyaan banaayenge. namaaz padhenge. bakreed par qurbaani hogi.",
    },
    # Religious & Spiritual
    {
        "name": "Prayer",
        "hindi": "नमाज अदा करी। रोजा रखा। जिक्र किया। दुआ मांगी। अल्लाह से मांगा।",
        "expected": "namaaz ada kari. roza rakha. zikr kiya. dua maangi. allah se maanga.",
    },
    {
        "name": "Temple Rituals",
        "hindi": "दर्शन किए। भोग लगाया। मंत्र पढ़े। आरती उतारी। प्रसाद लिया।",
        "expected": "darshan kiye. bhog lagaaya. mantra padhe. aarti utaari. prasaad liya.",
    },
    # Humor & Jokes
    {
        "name": "Funny Conversation",
        "hindi": "क्या बात है यार। मजाक कर रहा हूं। हंसी आ रही है। लोल हो गया। रोने लगा हूं हंस हंस के।",
        "expected": "kya baat hai yaar. mazaak kar raha hoon. hansi aa rahi hai. lol ho gaya. rone laga hoon hans hans ke.",
    },
    # Short Forms & Internet Slang
    {
        "name": "Internet Slang",
        "hindi": "बीबी आओ। टीटीएल दो। बीआरबी। एलओएल। ओएमजी। डीएम करो।",
        "expected": "bb aao. ttl do. brb. lol. omg. dm karo.",
    },
    # Mixed Hindi-English
    {
        "name": "Hinglish Mixed",
        "hindi": "मीटिंग में जाऊं क्या? प्रेजेंटेशन तैयार है। बॉस खुश होंगे। प्रोमोशन मिलेगा।",
        "expected": "meeting mein jaoon kya? presentation taiyaar hai. boss khush honge. promotion milega.",
    },
]


def calculate_word_accuracy(expected: str, got: str) -> tuple:
    """Calculate word-level accuracy"""
    expected_words = expected.lower().split()
    got_words = got.lower().split()

    # Pad shorter list
    max_len = max(len(expected_words), len(got_words))
    expected_words.extend([""] * (max_len - len(expected_words)))
    got_words.extend([""] * (max_len - len(got_words)))

    matches = sum(1 for e, g in zip(expected_words, got_words) if e == g)
    accuracy = (matches / max_len) * 100 if max_len > 0 else 0

    return accuracy, matches, max_len


def run_tests():
    """Run all additional test cases"""
    converter = HinglishConverter()

    print("=" * 80)
    print("          EXTENDED HINDI TO HINGLISH - TEST SUITE")
    print(f"                   Total Test Cases: {len(ADDITIONAL_TEST_CASES)}")
    print("=" * 80)

    results = {
        "excellent": [],  # >= 90%
        "good": [],  # 75-89%
        "fair": [],  # 60-74%
        "needs_work": [],  # < 60%
    }

    total_accuracy = 0

    for i, test in enumerate(ADDITIONAL_TEST_CASES, 1):
        hindi_text = test["hindi"]
        expected = test["expected"]

        got = converter.convert(hindi_text)
        accuracy, matches, total = calculate_word_accuracy(expected, got)
        total_accuracy += accuracy

        # Categorize
        if accuracy >= 90:
            status = "🌟 EXCELLENT"
            results["excellent"].append((i, test["name"], accuracy))
        elif accuracy >= 75:
            status = "👍 GOOD"
            results["good"].append((i, test["name"], accuracy))
        elif accuracy >= 60:
            status = "😐 FAIR"
            results["fair"].append((i, test["name"], accuracy))
        else:
            status = "🔧 NEEDS WORK"
            results["needs_work"].append((i, test["name"], accuracy))

        # Print results
        print(f"\n{'─' * 80}")
        print(f"Test #{i:02d}: {test['name']}")
        print(f"{'─' * 80}")
        print(f"\n📝 HINDI TEXT:")
        print(f"   {hindi_text}")
        print(f"\n✅ EXPECTED:")
        print(f"   {expected}")
        print(f"\n🎯 GOT:")
        print(f"   {got}")
        print(f"\n{status}: {accuracy:.1f}% ({matches}/{total} words)")

    # Final summary
    overall_accuracy = total_accuracy / len(ADDITIONAL_TEST_CASES)

    print("\n" + "=" * 80)
    print("                           FINAL SUMMARY")
    print("=" * 80)
    print(f"\n📊 OVERALL ACCURACY: {overall_accuracy:.1f}%")
    print(f"\n📈 BREAKDOWN:")
    print(
        f"   🌟 EXCELLENT (≥90%):  {len(results['excellent'])}/{len(ADDITIONAL_TEST_CASES)}"
    )
    print(
        f"   👍 GOOD (75-89%):     {len(results['good'])}/{len(ADDITIONAL_TEST_CASES)}"
    )
    print(
        f"   😐 FAIR (60-74%):     {len(results['fair'])}/{len(ADDITIONAL_TEST_CASES)}"
    )
    print(
        f"   🔧 NEEDS WORK (<60%):  {len(results['needs_work'])}/{len(ADDITIONAL_TEST_CASES)}"
    )

    # List failing tests
    if results["needs_work"]:
        print(f"\n🔴 FAILING TESTS:")
        for i, name, acc in results["needs_work"]:
            print(f"   #{i:02d}: {name} - {acc:.1f}%")

    # List fair tests
    if results["fair"]:
        print(f"\n🟡 FAIR TESTS:")
        for i, name, acc in results["fair"]:
            print(f"   #{i:02d}: {name} - {acc:.1f}%")

    print("\n" + "=" * 80)

    # Overall result
    if overall_accuracy >= 80:
        print("🎉 OVERALL RESULT: PASSED (≥ 80% accuracy)")
    elif overall_accuracy >= 60:
        print("⚠️  OVERALL RESULT: FAIR (60-79% accuracy)")
    else:
        print("❌ OVERALL RESULT: FAILED (< 60% accuracy)")
    print("=" * 80)


if __name__ == "__main__":
    run_tests()
