from setuptools import setup, find_packages
from pathlib import Path

# Minimal setup.py for a single-file CLI tool

setup(
    name="finnish-pdf-translator",
    version="0.1.0",
    description="Translate Finnish PDFs to English locally with OCR and MarianMT, with optional MPS (Apple Silicon) acceleration.",
    long_description=open("README.md", "r", encoding="utf-8").read() if Path("README.md").exists() else "",
    long_description_content_type="text/markdown",
    author="Mithilesh Prakash",
    python_requires=">=3.9",
    packages=find_packages(exclude=("tests", "examples")),
    py_modules=["translate_mypdf"],
    install_requires=[
        "pdfplumber>=0.11.0",
        "PyPDF2>=3.0.0",
        "pytesseract>=0.3.10",
        "pillow>=10.0.0",
        "transformers>=4.40.0",
        "torch",
        "accelerate>=0.27.0",
        "tqdm>=4.66.0",
    ],
    entry_points={
        "console_scripts": [
            "fi-pdf2en=translate_mypdf:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    include_package_data=True,
)
