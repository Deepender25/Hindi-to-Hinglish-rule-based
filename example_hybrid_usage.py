"""
Usage Example: Hybrid Gemini-Rule Based Converter
Shows how to use the hybrid converter with Gemini API validation
"""

from hybrid_gemini_converter import HybridGeminiConverter, convert_with_gemini


def main():
    print("=" * 70)
    print("Hybrid Gemini-Rule Based Converter - Usage Examples")
    print("=" * 70)

    # Initialize converter
    # It will automatically look for GEMINI_API_KEY in .env file
    converter = HybridGeminiConverter()

    # Example 1: Basic conversion (async mode - returns instantly)
    print("\n1. Basic Conversion (Rule-based instant, Gemini validates in background):")
    print("-" * 70)

    test_texts = [
        "नमस्ते, आप कैसे हैं?",
        "मुझे हिंदी बोलना पसंद है",
        "यह एक बढ़िया दिन है",
        "मैं ठीक हूं, धन्यवाद",
        "चलो बाहर घूमने चलते हैं",
    ]

    for text in test_texts:
        result = converter.convert(text, use_gemini=True, async_mode=True)
        print(f"Hindi:    {text}")
        print(f"Hinglish: {result}")
        print()

    # Example 2: Synchronous mode (waits for Gemini)
    print("\n2. Synchronous Mode (waits for Gemini response):")
    print("-" * 70)

    text = "मैं आज बहुत खुश हूं"
    result = converter.convert(text, use_gemini=True, async_mode=False)
    print(f"Hindi:    {text}")
    print(f"Hinglish: {result}")
    print()

    # Example 3: Rule-based only (no API call)
    print("\n3. Rule-Based Only (no API call - fastest):")
    print("-" * 70)

    result = converter.convert(text, use_gemini=False)
    print(f"Hindi:    {text}")
    print(f"Hinglish: {result}")
    print()

    # Example 4: Batch conversion
    print("\n4. Batch Conversion:")
    print("-" * 70)

    batch_results = converter.convert_batch(test_texts[:3], use_gemini=False)
    for hindi, hinglish in zip(test_texts[:3], batch_results):
        print(f"{hindi} -> {hinglish}")
    print()

    # Example 5: Show statistics
    print("\n5. Conversion Statistics:")
    print("-" * 70)

    import time

    time.sleep(2)  # Wait for background tasks

    converter.show_learning_summary()

    # Example 6: Quick function
    print("\n6. Quick Convert Function:")
    print("-" * 70)

    result = convert_with_gemini("धन्यवाद")
    print(f"धन्यवाद -> {result}")


if __name__ == "__main__":
    main()
