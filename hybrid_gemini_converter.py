"""
Hybrid Gemini-Rule Based Hindi-to-Hinglish Converter
Combines fast rule-based conversion with Gemini API validation
Continuously learns and improves dictionary
"""

import os
import re
import json
import threading
from typing import Optional, Tuple
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Try to import Gemini (new google-genai library)
try:
    from google import genai
    from google.genai import types

    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

# Import the rule-based converter
from hinglish_converter import HinglishConverter as RuleBasedConverter


class HybridGeminiConverter:
    """
    Hybrid converter that:
    1. Returns rule-based output instantly (fast)
    2. Calls Gemini API in background for validation
    3. Compares outputs and uses better one
    4. Learns new words and adds to dictionary
    """

    def __init__(
        self, api_key: Optional[str] = None, model_name: str = "gemini-3-flash-preview"
    ):
        """
        Initialize hybrid converter

        Args:
            api_key: Gemini API key (or set GEMINI_API_KEY in .env)
            model_name: Gemini model to use (default: gemini-3-flash-preview)
        """
        # Rule-based converter (primary)
        self.rule_converter = RuleBasedConverter()

        # Gemini setup
        self.gemini_available = False
        self.client = None
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model_name = model_name

        if GEMINI_AVAILABLE and self.api_key and self.api_key != "your_api_key_here":
            try:
                # New google-genai client initialization
                self.client = genai.Client(api_key=self.api_key)
                self.gemini_available = True
                print(f"[OK] Gemini API configured with model: {model_name}")
            except Exception as e:
                print(f"[WARN] Gemini setup failed: {e}")
                print("[INFO] Falling back to rule-based only")
        else:
            if not GEMINI_AVAILABLE:
                print(
                    "[WARN] google-genai not installed. Run: pip install google-genai"
                )
            elif not self.api_key or self.api_key == "your_api_key_here":
                print("[WARN] No Gemini API key found in .env file")
                print(
                    "       Get your API key from: https://makersuite.google.com/app/apikey"
                )
            print("[INFO] Running in rule-based only mode")

        # Learning system
        self.learned_words_file = "learned_words_gemini.json"
        self.learned_words = self._load_learned_words()

        # Background task tracking
        self._pending_tasks = []
        self._lock = threading.Lock()

        # Statistics
        self.stats = {
            "rule_based_only": 0,
            "gemini_improved": 0,
            "rule_based_better": 0,
            "new_words_learned": 0,
        }

    def _load_learned_words(self) -> dict:
        """Load learned words from file"""
        if os.path.exists(self.learned_words_file):
            try:
                with open(self.learned_words_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_learned_words(self):
        """Save learned words to file"""
        try:
            with open(self.learned_words_file, "w", encoding="utf-8") as f:
                json.dump(self.learned_words, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Warning: Could not save learned words: {e}")

    def _call_gemini(self, hindi_text: str) -> Optional[str]:
        """
        Call Gemini API for Hinglish transliteration

        Args:
            hindi_text: Hindi text in Devanagari

        Returns:
            Hinglish text or None if failed
        """
        if not self.gemini_available or not self.client:
            return None

        prompt = f"""Convert the following Hindi text to Hinglish (Hindi written in Roman/English script).
Important instructions:
- Use natural conversational Hinglish, NOT formal transliteration
- Example: 'मैं' should be 'main', NOT 'mayn'
- Example: 'हैं' should be 'hain', NOT 'hain'
- Keep it simple and natural, how people actually type in WhatsApp
- Do NOT translate, just convert script

Hindi: {hindi_text}

Hinglish:"""

        try:
            # New google-genai API
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.1,
                    max_output_tokens=256,
                ),
            )

            if response and response.text:
                # Clean up the response
                hinglish = response.text.strip()
                # Remove any quotes or extra formatting
                hinglish = re.sub(r'["\']', "", hinglish)
                return hinglish

        except Exception as e:
            print(f"Gemini API error: {e}")

        return None

    def _extract_words(self, text: str) -> list:
        """Extract Hindi words from text"""
        # Simple word extraction
        words = re.findall(r"[\u0900-\u097F]+", text)
        return words

    def _compare_outputs(
        self, hindi: str, rule_output: str, gemini_output: Optional[str]
    ) -> Tuple[str, str]:
        """
        Compare rule-based and Gemini outputs

        Returns:
            Tuple of (best_output, source)
        """
        if not gemini_output:
            return rule_output, "rule"

        # Normalize for comparison (remove spaces and punctuation)
        import string

        def normalize(text: str) -> str:
            text = text.lower().replace(" ", "")
            # Remove punctuation for comparison
            text = text.translate(str.maketrans("", "", string.punctuation))
            return text

        rule_norm = normalize(rule_output)
        gemini_norm = normalize(gemini_output)

        # Check if they're similar (ignoring punctuation)
        if rule_norm == gemini_norm:
            # Same transliteration, return rule-based (prefer original punctuation)
            return rule_output, "rule"

        # Check if Gemini output looks more natural (heuristics)
        # Prefer Gemini if it uses common Hinglish patterns
        hinglish_patterns = [
            "hai",
            "hain",
            "main",
            "mera",
            "tum",
            "aap",
            "yeh",
            "woh",
            "nahi",
            "acha",
            "bura",
            "bahut",
            "thoda",
            "kaise",
            "kyu",
            "mein",
            "ko",
            "se",
            "ka",
            "ki",
            "ke",
        ]

        rule_score = sum(1 for p in hinglish_patterns if p in rule_norm)
        gemini_score = sum(1 for p in hinglish_patterns if p in gemini_norm)

        # Also check word count similarity
        hindi_words = len(hindi.split())
        rule_words = len(rule_output.split())
        gemini_words = len(gemini_output.split())

        rule_word_diff = abs(hindi_words - rule_words)
        gemini_word_diff = abs(hindi_words - gemini_words)

        # Decide which is better
        if gemini_score >= rule_score and gemini_word_diff <= rule_word_diff + 2:
            return gemini_output, "gemini"
        else:
            return rule_output, "rule"

    def _learn_from_comparison(
        self, hindi: str, rule_output: str, gemini_output: Optional[str], chosen: str
    ):
        """Learn from comparison and update dictionary"""
        if chosen == "gemini" and gemini_output:
            # Extract words and learn
            hindi_words = self._extract_words(hindi)
            gemini_words = gemini_output.split()
            rule_words = rule_output.split()

            # Simple word-by-word learning
            if len(hindi_words) == len(gemini_words):
                for hw, gw in zip(hindi_words, gemini_words):
                    if hw not in self.rule_converter.common_words:
                        if hw not in self.learned_words:
                            self.learned_words[hw] = {
                                "hinglish": gw,
                                "confidence": 1,
                                "source": "gemini",
                            }
                            self.stats["new_words_learned"] += 1
                            print(f"[LEARNED] New word: {hw} -> {gw}")
                        else:
                            # Increase confidence
                            self.learned_words[hw]["confidence"] += 1

            self._save_learned_words()

    def convert(
        self, hindi_text: str, use_gemini: bool = True, async_mode: bool = True
    ) -> str:
        """
        Convert Hindi to Hinglish with optional Gemini validation

        Args:
            hindi_text: Hindi text in Devanagari
            use_gemini: Whether to use Gemini API for validation
            async_mode: If True, return rule-based immediately and validate in background

        Returns:
            Hinglish text
        """
        if not hindi_text or not hindi_text.strip():
            return ""

        hindi_text = hindi_text.strip()

        # Step 1: Get rule-based output (instant)
        rule_output = self.rule_converter.convert(hindi_text)

        # Step 2: If Gemini not available or disabled, return rule-based
        if not use_gemini or not self.gemini_available:
            self.stats["rule_based_only"] += 1
            return rule_output

        if async_mode:
            # Return rule-based immediately, validate in background
            self._validate_async(hindi_text, rule_output)
            return rule_output
        else:
            # Synchronous mode: wait for Gemini
            gemini_output = self._call_gemini(hindi_text)
            best_output, source = self._compare_outputs(
                hindi_text, rule_output, gemini_output
            )

            if source == "gemini":
                self.stats["gemini_improved"] += 1
                self._learn_from_comparison(
                    hindi_text, rule_output, gemini_output, source
                )
            else:
                self.stats["rule_based_better"] += 1

            return best_output

    def _validate_async(self, hindi_text: str, rule_output: str):
        """Validate in background thread"""

        def validate():
            gemini_output = self._call_gemini(hindi_text)
            if gemini_output:
                best, source = self._compare_outputs(
                    hindi_text, rule_output, gemini_output
                )
                if source == "gemini":
                    with self._lock:
                        self.stats["gemini_improved"] += 1
                    self._learn_from_comparison(
                        hindi_text, rule_output, gemini_output, source
                    )
                else:
                    with self._lock:
                        self.stats["rule_based_better"] += 1

        thread = threading.Thread(target=validate, daemon=True)
        thread.start()
        self._pending_tasks.append(thread)

    def convert_batch(self, texts: list, use_gemini: bool = True) -> list:
        """Convert multiple texts"""
        return [self.convert(text, use_gemini=use_gemini) for text in texts]

    def get_stats(self) -> dict:
        """Get conversion statistics"""
        return self.stats.copy()

    def show_learning_summary(self):
        """Show learned words summary"""
        print("\n" + "=" * 60)
        print("LEARNING SUMMARY")
        print("=" * 60)
        print(f"Total learned words: {len(self.learned_words)}")
        print(f"Rule-based only: {self.stats['rule_based_only']}")
        print(f"Gemini improved: {self.stats['gemini_improved']}")
        print(f"Rule-based better: {self.stats['rule_based_better']}")
        print(f"New words learned: {self.stats['new_words_learned']}")
        print("\nTop learned words:")
        sorted_words = sorted(
            self.learned_words.items(),
            key=lambda x: x[1].get("confidence", 0),
            reverse=True,
        )[:10]
        for word, data in sorted_words:
            print(
                f"  {word} -> {data['hinglish']} (confidence: {data.get('confidence', 1)})"
            )


# Convenience function for quick use
def convert_with_gemini(hindi_text: str, api_key: Optional[str] = None) -> str:
    """
    Quick conversion with Gemini validation

    Args:
        hindi_text: Hindi text to convert
        api_key: Optional Gemini API key

    Returns:
        Hinglish text
    """
    converter = HybridGeminiConverter(api_key=api_key)
    return converter.convert(hindi_text)


if __name__ == "__main__":
    # Demo
    output = []
    output.append("=" * 60)
    output.append("Hybrid Gemini-Rule Based Converter Demo")
    output.append("=" * 60)

    converter = HybridGeminiConverter()

    test_sentences = [
        "नमस्ते, आप कैसे हैं?",
        "मुझे हिंदी बोलना पसंद है",
        "यह एक बढ़िया दिन है",
        "चलो बाहर घूमने चलते हैं",
    ]

    output.append(
        "\nConverting... (Rule-based is instant, Gemini validates in background)\n"
    )

    for hindi in test_sentences:
        hinglish = converter.convert(hindi, use_gemini=True, async_mode=True)
        output.append(f"Hindi:    {hindi}")
        output.append(f"Hinglish: {hinglish}")
        output.append("")

    # Wait a bit for background tasks
    import time

    time.sleep(3)

    # Save output to file
    with open("hybrid_demo_output.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(output))

    print("Output saved to: hybrid_demo_output.txt")

    # Show stats
    converter.show_learning_summary()
