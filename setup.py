#!/usr/bin/env python3
"""
Setup script for DocxMD Converter
"""

from pathlib import Path
from setuptools import setup, find_packages

# Read README
readme_path = Path(__file__).parent / "README_NEW.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

# Read requirements
requirements_path = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_path.exists():
    with open(requirements_path, "r", encoding="utf-8") as f:
        requirements = [
            line.strip()
            for line in f
            if line.strip() and not line.startswith("#") and not line.startswith("-")
        ]

setup(
    name="docxmd-converter",
    version="3.1.0",
    description="Интеллектуальная система конвертации и обработки документов с NLP-анализом",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="DocxMD Team",
    author_email="team@docxmd-converter.com",
    url="https://github.com/your-repo/docxmd-converter",

    # Package configuration
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.11",

    # Dependencies
    install_requires=[
        "pypandoc>=1.15",
        "python-docx>=0.8.11",
        "flask>=2.3.0",
        "flask-cors>=4.0.0",
        "pandas>=1.5.0",
        "numpy>=1.24.0",
        "regex>=2023.0.0",
    ],

    # Optional dependencies
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "isort>=5.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "nlp": [
            "nltk>=3.8.0",
            "spacy>=3.6.0",
            "scikit-learn>=1.3.0",
        ],
    },

    # Entry points
    entry_points={
        "console_scripts": [
            "docxmd-converter=docxmd_converter.cli:main",
            "docxmd-gui=docxmd_converter.gui:main",
            "docxmd-web=docxmd_converter.web_interface:main",
        ],
    },

    # Package data
    package_data={
        "docxmd_converter": [
            "../config/*.json",
            "../data/*.json",
        ],
    },

    # Metadata
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business :: Office Suites",
        "Topic :: Text Processing :: Markup",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],

    keywords="docx markdown converter nlp document-processing ai",
    project_urls={
        "Bug Reports": "https://github.com/your-repo/docxmd-converter/issues",
        "Source": "https://github.com/your-repo/docxmd-converter",
        "Documentation": "https://github.com/your-repo/docxmd-converter/wiki",
    },
)