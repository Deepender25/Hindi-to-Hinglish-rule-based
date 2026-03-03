"""
Compare API-First vs Smart Hybrid vs Rule-Based
Test on extended test cases
"""

import sys
import io

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

from api_first_converter import APIFirstConverter
from smart_hybrid_converter import SmartHybridConverter
from hinglish_converter import HinglishConverter

# Test cases
test_cases = [
    ("Business Meeting", "आज की मीटिंग बहुत अहम है।", "aaj ki meeting bahut aham hai."),
    (
        "Email Writing",
        "प्रिय सर, मैं आपको सूचित करना चाहता हूं।",
        "priya sir, main aapko soochit karna chahta hoon.",
    ),
    (
        "Job Application",
        "मैं इस पद के लिए आवेदन करना चाहता हूं।",
        "main is pad ke liye avedan karna chahta hoon.",
    ),
    (
        "Social Media Post",
        "इस फोटो को लाइक और शेयर करें।",
        "is photo ko like aur share karen.",
    ),
    ("Online Shopping", "यह प्रोडक्ट बहुत अच्छा है।", "yah product bahut achha hai."),
    ("Technical Support", "मेरा कंप्यूटर स्लो हो गया है।", "mera computer slow ho gaya hai."),
    ("Online Class", "आज ऑनलाइन क्लास में टेस्ट होगा।", "aaj online class mein test hoga."),
    (
        "Homework Help",
        "यह मैथ का सवाल समझ नहीं आया।",
        "yah math ka sawaal samajh nahi aaya.",
    ),
    (
        "Library Visit",
        "मुझे यह किताब जारी करवानी है।",
        "mujhe yah kitaab jaari karwaani hai.",
    ),
    ("Pharmacy Visit", "यह दवा दे दीजिए।", "yah dawa de dijiye."),
]

print("=" * 100)
print("COMPARISON: API-First vs Smart Hybrid vs Rule-Based")
print("=" * 100)

# Initialize converters
print("\nInitializing converters...")
api_first = APIFirstConverter()
smart_hybrid = SmartHybridConverter()
rule_based = HinglishConverter()

# Storage for results
api_results = []
hybrid_results = []
rule_results = []

print("\n" + "=" * 100)
print("TESTING")
print("=" * 100)

for i, (name, hindi, expected) in enumerate(test_cases, 1):
    print(f"\n{i}. {name}")
    print(f"   Hindi:    {hindi}")
    print(f"   Expected: {expected}")

    # API-First
    api_result = api_first.convert(hindi, learn=False)
    api_results.append(api_result)

    # Smart Hybrid
    hybrid_result = smart_hybrid.convert(hindi, learn=False)
    hybrid_results.append(hybrid_result)

    # Rule-Based
    rule_result = rule_based.convert(hindi)
    rule_results.append(rule_result)

    print(f"   API-First:  {api_result}")
    print(f"   SmartHybrid:{hybrid_result}")
    print(f"   Rule-Based: {rule_result}")


# Calculate accuracies
def calc_accuracy(expected, got):
    exp_words = expected.lower().split()
    got_words = got.lower().split()
    matches = sum(1 for e, g in zip(exp_words, got_words) if e == g)
    return (matches / len(exp_words)) * 100 if exp_words else 0


api_acc = sum(
    calc_accuracy(exp, got) for (_, _, exp), got in zip(test_cases, api_results)
) / len(test_cases)
hybrid_acc = sum(
    calc_accuracy(exp, got) for (_, _, exp), got in zip(test_cases, hybrid_results)
) / len(test_cases)
rule_acc = sum(
    calc_accuracy(exp, got) for (_, _, exp), got in zip(test_cases, rule_results)
) / len(test_cases)

print("\n" + "=" * 100)
print("ACCURACY COMPARISON")
print("=" * 100)
print(f"API-First:    {api_acc:.1f}%")
print(f"Smart Hybrid: {hybrid_acc:.1f}%")
print(f"Rule-Based:   {rule_acc:.1f}%")
print("=" * 100)

# Show winner
winner = max(
    [(api_acc, "API-First"), (hybrid_acc, "Smart Hybrid"), (rule_acc, "Rule-Based")]
)
print(f"\n🏆 Winner: {winner[1]} with {winner[0]:.1f}% accuracy")
