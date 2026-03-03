"""
Hindi to Hinglish Converter - Main Application
Supports both CLI and GUI interfaces
"""

import sys
import io

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

import argparse
from pathlib import Path

try:
    from hinglish_converter import HinglishConverter, convert
except ImportError:
    from .hinglish_converter import HinglishConverter, convert


def run_cli():
    """Run the command-line interface"""
    parser = argparse.ArgumentParser(
        description="Convert Hindi text to natural conversational Hinglish",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "नमस्ते, आप कैसे हैं?"
  %(prog)s -f input.txt -o output.txt
  %(prog)s -i                           # Interactive mode
        """,
    )

    parser.add_argument("text", nargs="?", help="Hindi text to convert")

    parser.add_argument("-f", "--file", help="Input file containing Hindi text")

    parser.add_argument("-o", "--output", help="Output file to save Hinglish text")

    parser.add_argument(
        "-i", "--interactive", action="store_true", help="Run in interactive mode"
    )

    parser.add_argument("-g", "--gui", action="store_true", help="Launch GUI interface")

    args = parser.parse_args()

    converter = HinglishConverter()

    # Launch GUI if requested
    if args.gui:
        run_gui()
        return

    # Interactive mode
    if args.interactive or (not args.text and not args.file):
        print("=" * 60)
        print("   Hindi to Hinglish Converter - Interactive Mode")
        print("=" * 60)
        print("Enter Hindi text (or 'quit' to exit):")
        print("-" * 60)

        while True:
            try:
                hindi_text = input("\nHindi > ").strip()

                if hindi_text.lower() in ("quit", "exit", "q", "बंद"):
                    print("Goodbye!")
                    break

                if hindi_text:
                    hinglish = converter.convert(hindi_text)
                    print(f"Hinglish> {hinglish}")

            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")

        return

    # File mode
    if args.file:
        if not Path(args.file).exists():
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            sys.exit(1)

        try:
            with open(args.file, "r", encoding="utf-8") as f:
                hindi_text = f.read()

            hinglish = converter.convert(hindi_text)

            if args.output:
                with open(args.output, "w", encoding="utf-8") as f:
                    f.write(hinglish)
                print(f"Output saved to: {args.output}")
            else:
                print(hinglish)

        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

        return

    # Direct text conversion
    if args.text:
        hinglish = converter.convert(args.text)
        print(hinglish)
        return


def run_gui():
    """Run the GUI interface using tkinter"""
    try:
        import tkinter as tk
        from tkinter import ttk, scrolledtext, filedialog, messagebox
    except ImportError:
        print("Error: tkinter is not available. Please install python-tk package.")
        sys.exit(1)

    class HinglishGUI:
        def __init__(self, root):
            self.root = root
            self.root.title("Hindi to Hinglish Converter")
            self.root.geometry("900x700")
            self.root.minsize(700, 500)

            # Configure style
            self.style = ttk.Style()
            self.style.configure("Header.TLabel", font=("Helvetica", 16, "bold"))
            self.style.configure("SubHeader.TLabel", font=("Helvetica", 12))
            self.style.configure("Convert.TButton", font=("Helvetica", 11, "bold"))

            self.converter = HinglishConverter()
            self.setup_ui()

        def setup_ui(self):
            # Main container with padding
            main_frame = ttk.Frame(self.root, padding="20")
            main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

            # Configure grid weights
            self.root.columnconfigure(0, weight=1)
            self.root.rowconfigure(0, weight=1)
            main_frame.columnconfigure(0, weight=1)
            main_frame.rowconfigure(2, weight=1)
            main_frame.rowconfigure(4, weight=1)

            # Header
            header = ttk.Label(
                main_frame, text="Hindi to Hinglish Converter", style="Header.TLabel"
            )
            header.grid(row=0, column=0, pady=(0, 10))

            # Subheader
            subheader = ttk.Label(
                main_frame,
                text="Enter Hindi text below and click Convert",
                style="SubHeader.TLabel",
            )
            subheader.grid(row=1, column=0, pady=(0, 10))

            # Input section
            input_frame = ttk.LabelFrame(main_frame, text="Hindi Input", padding="10")
            input_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
            input_frame.columnconfigure(0, weight=1)
            input_frame.rowconfigure(0, weight=1)

            self.input_text = scrolledtext.ScrolledText(
                input_frame,
                wrap=tk.WORD,
                font=("Mangal", 14),
                height=8,
                padx=10,
                pady=10,
            )
            self.input_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

            # Button frame
            button_frame = ttk.Frame(main_frame)
            button_frame.grid(row=3, column=0, pady=10)

            # Convert button
            convert_btn = ttk.Button(
                button_frame,
                text="Convert to Hinglish",
                command=self.convert_text,
                style="Convert.TButton",
            )
            convert_btn.pack(side=tk.LEFT, padx=5)

            # Clear button
            clear_btn = ttk.Button(button_frame, text="Clear", command=self.clear_text)
            clear_btn.pack(side=tk.LEFT, padx=5)

            # Load file button
            load_btn = ttk.Button(
                button_frame, text="Load File", command=self.load_file
            )
            load_btn.pack(side=tk.LEFT, padx=5)

            # Save button
            save_btn = ttk.Button(
                button_frame, text="Save Result", command=self.save_result
            )
            save_btn.pack(side=tk.LEFT, padx=5)

            # Output section
            output_frame = ttk.LabelFrame(
                main_frame, text="Hinglish Output", padding="10"
            )
            output_frame.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
            output_frame.columnconfigure(0, weight=1)
            output_frame.rowconfigure(0, weight=1)

            self.output_text = scrolledtext.ScrolledText(
                output_frame,
                wrap=tk.WORD,
                font=("Consolas", 14),
                height=8,
                padx=10,
                pady=10,
                state=tk.DISABLED,
            )
            self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

            # Status bar
            self.status_var = tk.StringVar()
            self.status_var.set("Ready")
            status_bar = ttk.Label(
                main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W
            )
            status_bar.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=(10, 0))

            # Bind keyboard shortcuts
            self.root.bind("<Control-Return>", lambda e: self.convert_text())
            self.root.bind("<Control-l>", lambda e: self.clear_text())
            self.root.bind("<Control-o>", lambda e: self.load_file())
            self.root.bind("<Control-s>", lambda e: self.save_result())

        def convert_text(self):
            """Convert input text to Hinglish"""
            hindi_text = self.input_text.get("1.0", tk.END).strip()

            if not hindi_text:
                messagebox.showwarning(
                    "Empty Input", "Please enter some Hindi text to convert."
                )
                return

            try:
                hinglish = self.converter.convert(hindi_text)

                self.output_text.config(state=tk.NORMAL)
                self.output_text.delete("1.0", tk.END)
                self.output_text.insert("1.0", hinglish)
                self.output_text.config(state=tk.DISABLED)

                word_count = len(hindi_text.split())
                char_count = len(hindi_text)
                self.status_var.set(
                    f"Converted {word_count} words, {char_count} characters"
                )

            except Exception as e:
                messagebox.showerror(
                    "Conversion Error", f"Error during conversion: {str(e)}"
                )

        def clear_text(self):
            """Clear both input and output"""
            self.input_text.delete("1.0", tk.END)
            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete("1.0", tk.END)
            self.output_text.config(state=tk.DISABLED)
            self.status_var.set("Ready")

        def load_file(self):
            """Load Hindi text from file"""
            file_path = filedialog.askopenfilename(
                title="Select Hindi Text File",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            )

            if file_path:
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    self.input_text.delete("1.0", tk.END)
                    self.input_text.insert("1.0", content)
                    self.status_var.set(f"Loaded: {file_path}")

                except Exception as e:
                    messagebox.showerror("Load Error", f"Error loading file: {str(e)}")

        def save_result(self):
            """Save Hinglish output to file"""
            hinglish = self.output_text.get("1.0", tk.END).strip()

            if not hinglish:
                messagebox.showwarning(
                    "Empty Output", "No output to save. Convert some text first."
                )
                return

            file_path = filedialog.asksaveasfilename(
                title="Save Hinglish Text",
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            )

            if file_path:
                try:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(hinglish)
                    self.status_var.set(f"Saved to: {file_path}")
                    messagebox.showinfo("Success", f"File saved successfully!")

                except Exception as e:
                    messagebox.showerror("Save Error", f"Error saving file: {str(e)}")

    # Create and run GUI
    root = tk.Tk()
    app = HinglishGUI(root)

    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")

    root.mainloop()


def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        run_cli()
    else:
        # No arguments - launch GUI
        print("Launching GUI... Use --help for CLI options")
        run_gui()


if __name__ == "__main__":
    main()
