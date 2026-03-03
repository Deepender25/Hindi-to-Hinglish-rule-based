# Hindi to Hinglish Converter

A highly accurate Python project that converts Hindi text to natural conversational Hinglish (Hindi written in Roman script).

## Features

- **Natural Conversational Hinglish**: Not robotic ITRANS format, but the way people actually type Hinglish in messages
- **Extensive Word Dictionary**: 200+ common Hindi words with perfect Hinglish equivalents
- **Smart Schwa Deletion**: Automatically removes inherent 'a' vowels where Hindi speakers don't pronounce them
- **Multiple Interfaces**: Command-line, interactive, and GUI modes
- **File Processing**: Convert entire files with one command
- **Highly Customizable**: Easy to add new words and rules

## Installation

1. Clone or download this repository
2. Run the setup script:
   - Windows: `run.bat`
   - Linux/Mac: `./run.sh`

Or manually:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

### GUI Mode (Default)
```bash
python main.py
# or
run.bat        # Windows
./run.sh       # Linux/Mac
```

### Command Line

**Convert text directly:**
```bash
python main.py "नमस्ते, आप कैसे हैं?"
# Output: namaste, aap kaise hain?
```

**Interactive mode:**
```bash
python main.py -i
```

**Convert a file:**
```bash
python main.py -f input.txt -o output.txt
```

**Show help:**
```bash
python main.py --help
```

## Python API

```python
from hinglish_converter import HinglishConverter, convert

# Quick conversion
hinglish = convert("नमस्ते, आप कैसे हैं?")
print(hinglish)  # namaste, aap kaise hain?

# Advanced usage with custom settings
converter = HinglishConverter()
result = converter.convert("मैं ठीक हूं")
print(result)  # main theek hoon

# Convert file
converter.convert_file('hindi.txt', 'hinglish.txt')
```

## Examples

| Hindi | Hinglish |
|-------|----------|
| नमस्ते, आप कैसे हैं? | namaste, aap kaise hain? |
| मैं ठीक हूं, धन्यवाद! | main theek hoon, dhanyavaad! |
| मुझे हिंदी बोलना पसंद है | mujhe hindi bolna pasand hai |
| यह एक बढ़िया दिन है | yeh ek badhiya din hai |
| चलो बाहर घूमने चलते हैं | chalo bahar ghoomne chalte hain |

## How It Works

1. **Dictionary Lookup**: First checks if the word exists in the common words dictionary
2. **Character Mapping**: Converts Devanagari characters to Roman equivalents
3. **Schwa Deletion**: Applies linguistic rules to remove unnecessary 'a' sounds
4. **Post-processing**: Normalizes vowel patterns (e.g., 'ee' → 'i', 'aa' → 'a')

## Project Structure

```
.
├── hinglish_converter.py    # Core conversion engine
├── main.py                   # CLI and GUI application
├── requirements.txt          # Python dependencies
├── run.bat                   # Windows launcher
├── run.sh                    # Unix launcher
└── README.md                 # This file
```

## Customization

To add new words, edit the `common_words` dictionary in `hinglish_converter.py`:

```python
self.common_words = {
    "हिंदी": "hindi",
    "आप": "aap",
    # Add your words here
}
```

## Requirements

- Python 3.8+
- tkinter (for GUI, usually comes with Python)
- See `requirements.txt` for package dependencies

## License

This project is open source and available under the MIT License.
