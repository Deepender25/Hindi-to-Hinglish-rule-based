"""
Setup file for Hindi-to-Hinglish Converter
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="hindi-to-hinglish",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A highly accurate Hindi to Hinglish (Roman Hindi) converter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/hindi-to-hinglish",
    py_modules=["hinglish_converter"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "indic-transliteration>=2.3.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "hindi-to-hinglish=hinglish_converter:main",
        ],
    },
)
