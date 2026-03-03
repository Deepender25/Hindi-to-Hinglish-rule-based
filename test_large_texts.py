"""
Comprehensive Test Suite for Hindi to Hinglish Converter
Tests large paragraphs with expected outputs
"""

import sys
import io
from hinglish_converter import HinglishConverter

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

# Test cases with expected outputs
TEST_CASES = [
    {
        "name": "Daily Conversation",
        "hindi": "नमस्ते दोस्तों! आज मौसम बहुत अच्छा है। चलो बाहर घूमने चलते हैं। मुझे बहुत दिनों से तुमसे मिलने का मन था।",
        "expected": "namaste doston! aaj mausam bahut achha hai. chalo baahar ghoomne chalte hain. mujhe bahut dinon se tumse milne ka man tha.",
    },
    {
        "name": "Family Scene",
        "hindi": "मेरी माँ ने आज बहुत स्वादिष्ट खाना बनाया। हम सब परिवार के साथ बैठकर खाना खाएंगे। मेरे भाई और बहन भी घर आए हैं।",
        "expected": "meri maa ne aaj bahut swaadisht khana banaaya. hum sab parivaar ke saath baithkar khana khaaenge. mere bhai aur behen bhi ghar aaye hain.",
    },
    {
        "name": "School Scene",
        "hindi": "मुझे सुबह स्कूल जाना है। मेरे सभी दोस्त वहाँ मिलेंगे। हमें पढ़ाई करनी है और फिर खेल खेलना है।",
        "expected": "mujhe subah school jaana hai. mere sabhi dost vahaan milenge. hamein padhaai karni hai aur phir khel khelna hai.",
    },
    {
        "name": "Shopping",
        "hindi": "मैं बाजार जा रहा हूं। मुझे सब्जियां और फल खरीदने हैं। क्या आपको भी कुछ चाहिए?",
        "expected": "main bazaar ja raha hoon. mujhe sabziyaan aur phal khareedne hain. kya aapko bhi kuchh chahiye?",
    },
    {
        "name": "Weather Description",
        "hindi": "आज बहुत गर्मी है। धूप बहुत तेज है। मुझे पानी पीना है। शाम को शायद बारिश होगी।",
        "expected": "aaj bahut garmi hai. dhoop bahut tez hai. mujhe paani peena hai. shaam ko shaayad baarish hogi.",
    },
    {
        "name": "Emotions",
        "hindi": "मैं आज बहुत खुश हूं। मुझे अपने दोस्तों के साथ समय बिताना पसंद है। हम हंसते हैं और मज़ा करते हैं।",
        "expected": "main aaj bahut khush hoon. mujhe apne doston ke saath samay bitaana pasand hai. hum hansate hain aur maza karte hain.",
    },
    {
        "name": "Technology",
        "hindi": "मेरा मोबाइल फोन खराब हो गया। मुझे नया फोन खरीदना है। मैं इंटरनेट से ऑर्डर करूंगा।",
        "expected": "mera mobile phone kharaab ho gaya. mujhe naya phone khareedna hai. main internet se order karunga.",
    },
    {
        "name": "Health",
        "hindi": "मुझे सिरदर्द हो रहा है। मुझे दवा लेनी होगी। कल मैं डॉक्टर से मिलूंगा।",
        "expected": "mujhe sirdard ho raha hai. mujhe dawa leni hogi. kal main doctor se milunga.",
    },
    {
        "name": "Travel",
        "hindi": "हम कल शहर जा रहे हैं। हम ट्रेन से जाएंगे। वहाँ हम अपने रिश्तेदारों से मिलेंगे।",
        "expected": "hum kal shehar ja rahe hain. hum train se jaaenge. vahaan hum apne rishtedaaron se milenge.",
    },
    {
        "name": "Food",
        "hindi": "मुझे खाना पकाना पसंद है। मैं आलू की सब्जी और दाल चावल बनाऊंगा। यह बहुत स्वादिष्ट होगा।",
        "expected": "mujhe khana pakaana pasand hai. main aaloo ki sabzi aur daal chawal banaunga. yah bahut swaadisht hoga.",
    },
    {
        "name": "Long Paragraph",
        "hindi": "कल मैं अपने दोस्तों के साथ सिनेमा गया। हमने एक नई फिल्म देखी जो बहुत अच्छी थी। फिल्म में एक लड़का और लड़की की कहानी दिखाई गई थी। उनकी दोस्ती बहुत प्यारी थी। हम सबने बहुत एंजॉय किया।",
        "expected": "kal main apne doston ke saath cinema gaya. hamne ek nayi film dekhi jo bahut achhi thi. film mein ek ladka aur ladki ki kahaani dikhaayi gayi thi. unki dostee bahut pyaari thi. hum sabne bahut enjoy kiya.",
    },
    {
        "name": "Story",
        "hindi": "एक समय की बात है। एक गांव में एक बूढ़ा आदमी रहता था। उसके पास एक बेटा और एक बेटी थी। वह बहुत गरीब था लेकिन बहुत ईमानदार था।",
        "expected": "ek samay ki baat hai. ek gaanv mein ek boodha aadmi rehta tha. uske paas ek beta aur ek beti thi. vah bahut gareeb tha lekin bahut imaandaar tha.",
    },
    {
        "name": "Questions",
        "hindi": "तुम कहाँ जा रहे हो? मैं बाजार जा रहा हूं। तुम क्या खरीदोगे? मुझे कुछ सब्जियां चाहिए।",
        "expected": "tum kahaan ja rahe ho? main bazaar ja raha hoon. tum kya khareedoge? mujhe kuchh sabziyaan chahiye.",
    },
    {
        "name": "Complex",
        "hindi": "जब मैं छोटा था तो मैं अपनी दादी के साथ रहता था। वह मुझे हर रात कहानियां सुनाती थीं। मुझे उनकी कहानियां बहुत पसंद थीं।",
        "expected": "jab main chhota tha toh main apni dadi ke saath rehta tha. vah mujhe har raat kahaaniyaan sunaati thiin. mujhe unki kahaaniyaan bahut pasand thiin.",
    },
]


def normalize_text(text):
    """Normalize text for comparison."""
    return " ".join(text.lower().split())


def calculate_accuracy(result, expected):
    """Calculate word-level accuracy."""
    result_words = normalize_text(result).split()
    expected_words = normalize_text(expected).split()

    total = max(len(result_words), len(expected_words))
    if total == 0:
        return 100.0, 100.0

    matches = sum(1 for r, e in zip(result_words, expected_words) if r == e)
    expected_set = set(expected_words)
    matches_loose = sum(1 for r in result_words if r in expected_set)

    strict_acc = (matches / total) * 100
    loose_acc = (matches_loose / total) * 100

    return strict_acc, loose_acc


def run_tests():
    """Run all test cases."""
    converter = HinglishConverter()

    print("=" * 80)
    print("HINDI TO HINGLISH - COMPREHENSIVE TEST SUITE")
    print("=" * 80)
    print(f"\nTotal test cases: {len(TEST_CASES)}")

    results = []
    total_strict_acc = 0
    total_loose_acc = 0

    for i, test in enumerate(TEST_CASES, 1):
        print(f"\n{'─' * 80}")
        print(f"Test {i}: {test['name']}")
        print(f"{'─' * 80}")

        result = converter.convert(test["hindi"])

        print(f"\nHindi: {test['hindi']}")
        print(f"Expected: {test['expected']}")
        print(f"Got:      {result}")

        strict_acc, loose_acc = calculate_accuracy(result, test["expected"])
        total_strict_acc += strict_acc
        total_loose_acc += loose_acc

        if strict_acc >= 90:
            status = "EXCELLENT"
        elif strict_acc >= 70:
            status = "GOOD"
        else:
            status = "NEEDS WORK"

        print(
            f"\nAccuracy: {strict_acc:.1f}% (strict) / {loose_acc:.1f}% (loose) - {status}"
        )

        results.append(
            {
                "name": test["name"],
                "strict_acc": strict_acc,
                "loose_acc": loose_acc,
                "status": status,
            }
        )

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    avg_strict = total_strict_acc / len(TEST_CASES)
    avg_loose = total_loose_acc / len(TEST_CASES)

    print(f"\nAverage Strict Accuracy: {avg_strict:.1f}%")
    print(f"Average Loose Accuracy: {avg_loose:.1f}%")

    excellent = sum(1 for r in results if r["status"] == "EXCELLENT")
    good = sum(1 for r in results if r["status"] == "GOOD")
    needs_work = sum(1 for r in results if r["status"] == "NEEDS WORK")

    print(f"\nBreakdown:")
    print(f"  EXCELLENT (>=90%): {excellent}/{len(TEST_CASES)}")
    print(f"  GOOD (70-89%): {good}/{len(TEST_CASES)}")
    print(f"  NEEDS WORK (<70%): {needs_work}/{len(TEST_CASES)}")

    # Cache stats
    print(f"\n{'=' * 80}")
    print("CACHE STATS")
    print(f"{'=' * 80}")
    cache_info = converter.get_cache_info()
    print(f"Hits: {cache_info.hits}")
    print(f"Misses: {cache_info.misses}")
    print(f"Size: {cache_info.currsize}/{cache_info.maxsize}")

    if cache_info.hits + cache_info.misses > 0:
        hit_rate = (cache_info.hits / (cache_info.hits + cache_info.misses)) * 100
        print(f"Hit Rate: {hit_rate:.1f}%")

    print(f"\n{'=' * 80}")

    return avg_strict, avg_loose


if __name__ == "__main__":
    avg_strict, avg_loose = run_tests()

    if avg_strict >= 80:
        print("\nOVERALL: PASSED (>= 80% accuracy)")
        sys.exit(0)
    else:
        print("\nOVERALL: NEEDS IMPROVEMENT (< 80% accuracy)")
        sys.exit(1)
