"""
Usage Example: Hybrid Gemini-Rule Based Converter
Shows how to use the hybrid converter with Gemini API validation
"""

from hybrid_gemini_converter import HybridGeminiConverter, convert_with_gemini


def main():
    output = []
    output.append("=" * 70)
    output.append("Hybrid Gemini-Rule Based Converter - Usage Examples")
    output.append("=" * 70)

    # Initialize converter
    # It will automatically look for GEMINI_API_KEY in .env file
    converter = HybridGeminiConverter()

    # Example 1: Basic conversion (async mode - returns instantly)
    output.append(
        "\n1. Basic Conversion (Rule-based instant, Gemini validates in background):"
    )
    output.append("-" * 70)

    test_texts = [
        "नमस्ते, आप कैसे हैं?",
        "मुझे हिंदी बोलना पसंद है",
        "यह एक बढ़िया दिन है",
        "मैं ठीक हूं, धन्यवाद",
        "चलो बाहर घूमने चलते हैं",
    ]

    for text in test_texts:
        result = converter.convert(text, use_gemini=True, async_mode=True)
        output.append(f"Hindi:    {text}")
        output.append(f"Hinglish: {result}")
        output.append("")

    # Example 2: Synchronous mode (waits for Gemini)
    output.append("\n2. Synchronous Mode (waits for Gemini response):")
    output.append("-" * 70)

    text = "मैं आज बहुत खुश हूं"
    result = converter.convert(text, use_gemini=True, async_mode=False)
    output.append(f"Hindi:    {text}")
    output.append(f"Hinglish: {result}")
    output.append("")

    # Example 3: Rule-based only (no API call)
    output.append("\n3. Rule-Based Only (no API call - fastest):")
    output.append("-" * 70)

    result = converter.convert(text, use_gemini=False)
    output.append(f"Hindi:    {text}")
    output.append(f"Hinglish: {result}")
    output.append("")

    # Example 4: Batch conversion
    output.append("\n4. Batch Conversion:")
    output.append("-" * 70)

    batch_results = converter.convert_batch(test_texts[:3], use_gemini=False)
    for hindi, hinglish in zip(test_texts[:3], batch_results):
        output.append(f"{hindi} -> {hinglish}")
    output.append("")

    # Example 5: Show statistics
    output.append("\n5. Conversion Statistics:")
    output.append("-" * 70)

    import time

    time.sleep(3)  # Wait for background tasks

    # Get stats as string
    stats = converter.get_stats()
    output.append(f"Rule-based only: {stats['rule_based_only']}")
    output.append(f"Gemini improved: {stats['gemini_improved']}")
    output.append(f"Rule-based better: {stats['rule_based_better']}")
    output.append(f"New words learned: {stats['new_words_learned']}")
    output.append("")

    # Example 6: Quick function
    output.append("\n6. Quick Convert Function:")
    output.append("-" * 70)

    result = convert_with_gemini("धन्यवाद")
    output.append(f"धन्यवाद -> {result}")

    # Save to file
    with open("example_output.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(output))

    print("Output saved to: example_output.txt")

    # Show learning summary to console (it handles its own output)
    converter.show_learning_summary()


if __name__ == "__main__":
    main()
