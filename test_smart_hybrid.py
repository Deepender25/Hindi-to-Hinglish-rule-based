"""
Test Smart Hybrid Converter on Extended Test Cases
"""

import sys
import io
from smart_hybrid_converter import SmartHybridConverter

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

# Create converter
converter = SmartHybridConverter()

# Test cases from extended test suite (first 20)
test_cases = [
    ("Business Meeting", "आज की मीटिंग बहुत अहम है।", "aaj ki meeting bahut aham hai."),
    (
        "Email Writing",
        "प्रिय सर, मैं आपको सूचित करना चाहता हूं।",
        "priya sir, main aapko soochit karna chahta hoon.",
    ),
    (
        "Social Media Post",
        "इस फोटो को लाइक और शेयर करें।",
        "is photo ko like aur share karen.",
    ),
    ("Online Shopping", "यह प्रोडक्ट बहुत अच्छा है।", "yah product bahut achha hai."),
    ("Technical Support", "मेरा कंप्यूटर स्लो हो गया है।", "mera computer slow ho gaya hai."),
]

print("=" * 80)
print("SMART HYBRID CONVERTER - EXTENDED TEST")
print("=" * 80)

total_accuracy = 0

for name, hindi, expected in test_cases:
    result = converter.convert(hindi)

    # Simple word-level accuracy
    expected_words = expected.lower().split()
    result_words = result.lower().split()

    matches = sum(1 for e, r in zip(expected_words, result_words) if e == r)
    accuracy = (matches / len(expected_words)) * 100 if expected_words else 0
    total_accuracy += accuracy

    print(f"\n{name}:")
    print(f"  Expected: {expected}")
    print(f"  Got:      {result}")
    print(f"  Accuracy: {accuracy:.1f}%")

print("\n" + "=" * 80)
print(f"Average Accuracy: {total_accuracy / len(test_cases):.1f}%")
print("=" * 80)

converter.show_learning_summary()
converter._save_learned_words()
