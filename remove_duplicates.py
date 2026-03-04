import re

with open(
    r"C:\Users\yadav\OneDrive\Desktop\projects\Hindi-to-Hinglish\try with kilo\hinglish_converter.py",
    "r",
    encoding="utf-8",
) as f:
    content = f.read()

# Words with duplicates (Hindi words)
duplicates = [
    "स्कूल",
    "कॉलेज",
    "होटल",
    "मोबाइल",
    "फोन",
    "इंटरनेट",
    "व्हाट्सएप",
    "फेसबुक",
    "इंस्टाग्राम",
    "ट्विटर",
    "गूगल",
    "यूट्यूब",
    "एप्लिकेशन",
    "वेबसाइट",
    "पासवर्ड",
    "बैंक",
    "कैश",
    "चेक",
    "ऑर्डर",
    "डिलीवरी",
    "डिस्काउंट",
    "ऑफर",
    "सेल",
    "प्रीमियम",
    "नीड",
    "वांट",
    "लाइक",
    "एंजॉय",
]

total_removed = 0

# For each duplicate word, keep only the first occurrence
for word in duplicates:
    # Find all occurrences with pattern
    pattern = f'            "{word}": "[a-z]+",\n'
    matches = list(re.finditer(pattern, content))
    if len(matches) > 1:
        # Remove all but the first occurrence
        for match in reversed(matches[1:]):  # Reverse to maintain positions
            content = content[: match.start()] + content[match.end() :]
        total_removed += len(matches) - 1

with open(
    r"C:\Users\yadav\OneDrive\Desktop\projects\Hindi-to-Hinglish\try with kilo\hinglish_converter.py",
    "w",
    encoding="utf-8",
) as f:
    f.write(content)

print(f"Removed {total_removed} duplicate entries")
print("All duplicates removed successfully!")
