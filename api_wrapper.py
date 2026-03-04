"""
Simple API wrapper for Hindi-to-Hinglish Converter
Easy integration for other projects
"""

from hinglish_converter import HinglishConverter

# Global converter instance (singleton)
_converter = None


def get_converter():
    """Get or create the global converter instance"""
    global _converter
    if _converter is None:
        _converter = HinglishConverter()
    return _converter


def convert(text: str) -> str:
    """
    Convert Hindi text to Hinglish

    Args:
        text: Hindi text in Devanagari script

    Returns:
        Hinglish text in Roman script

    Example:
        >>> convert("नमस्ते")
        'namaste'
    """
    return get_converter().convert(text)


def convert_batch(texts: list) -> list:
    """
    Convert multiple Hindi texts to Hinglish

    Args:
        texts: List of Hindi strings

    Returns:
        List of Hinglish strings
    """
    converter = get_converter()
    return [converter.convert(text) for text in texts]


def convert_file(input_path: str, output_path: str):
    """
    Convert a file containing Hindi text

    Args:
        input_path: Path to input file with Hindi text
        output_path: Path to output file for Hinglish text
    """
    get_converter().convert_file(input_path, output_path)


# Convenience function for quick conversion
def to_hinglish(text: str) -> str:
    """Alias for convert() - quick conversion"""
    return convert(text)


if __name__ == "__main__":
    # Demo
    print(convert("नमस्ते, आप कैसे हैं?"))
    print(convert("मुझे हिंदी बोलना पसंद है"))
