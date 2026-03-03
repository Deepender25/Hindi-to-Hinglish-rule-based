"""
Test API-First with truly unknown words
"""

import sys
import io

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

from api_first_converter import APIFirstConverter
from smart_hybrid_converter import SmartHybridConverter
from hinglish_converter import HinglishConverter

# Unknown/new words that aren't in dictionary
unknown_words = [
    ("जिओ", "Geo (reliance jio)"),
    ("फ्लिपकार्ट", "Flipkart"),
    ("अमेज़ॉन", "Amazon"),
    ("व्हाट्सएप", "WhatsApp"),
    ("इंस्टाग्राम", "Instagram"),
    ("यूट्यूब", "YouTube"),
    ("फेसबुक", "Facebook"),
    ("ट्विटर", "Twitter"),
    ("लिंक्डइन", "LinkedIn"),
    ("स्नैपचैट", "Snapchat"),
    ("जूम", "Zoom"),
    ("टीम्स", "Microsoft Teams"),
    ("स्काइप", "Skype"),
    ("स्लैक", "Slack"),
    ("टrello", "Trello"),
]

print("=" * 80)
print("TESTING UNKNOWN WORDS - API vs RULE-BASED")
print("=" * 80)

# Initialize converters with NO learned words
import os

for f in ["api_first_learned.json", "smart_learned_words.json"]:
    if os.path.exists(f):
        os.remove(f)

api_first = APIFirstConverter()
smart_hybrid = SmartHybridConverter()
rule_based = HinglishConverter()

print("\nConverting unknown words...\n")

for hindi, meaning in unknown_words:
    api_result = api_first.convert(hindi, learn=False)
    hybrid_result = smart_hybrid.convert(hindi, learn=False)
    rule_result = rule_based.convert(hindi)

    # Check if API was actually used
    api_used = api_result != rule_result

    print(f"{meaning}")
    print(f"  Hindi:      {hindi}")
    print(f"  API-First:  {api_result} {'✅' if api_used else '❌'}")
    print(f"  SmartHybrid:{hybrid_result}")
    print(f"  Rule-Based: {rule_result}")
    print()

print("=" * 80)
print("\nLegend:")
print("  ✅ = API gave different (potentially better) result")
print("  ❌ = API gave same result as rule-based")
print("=" * 80)
