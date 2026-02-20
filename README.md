# Finnish PDF → English Translator (Local, MPS‑Accelerated)

This repository provides a fully local, privacy‑preserving pipeline for translating **Finnish-language PDFs** into **English text files**, supporting:

- Native text extraction (for digital PDFs)
- OCR text extraction using Tesseract (for scanned PDFs)
- Sentence segmentation
- MarianMT translation (Helsinki-NLP/opus-mt-fi-en)
- Apple Silicon **MPS GPU acceleration**
- Complete offline execution (except first-time model download)

This is ideal for research, clinical documents, historical Finnish text, student papers, or any privacy-sensitive content.

---

## 🚀 Features

- **🔍 Automatic PDF type detection**  
  Detects if a PDF contains selectable text or requires OCR.

- **📖 OCR for scanned PDFs**  
  Uses `pytesseract` + `pdfplumber`.

- **💬 Sentence-based translation**  
  Translation quality improves when we translate sentence-by-sentence.

- **⚡ MPS GPU acceleration**  
  Dramatically faster translation on Apple Silicon:  
  (M1/M2/M3/M4 chips supported)

- **🧠 Local MarianMT model**  
  No cloud calls. No data leaves your device.

---

## 🛠️ Installation

### 1. Install system dependencies

#### macOS (recommended)

```bash
brew install tesseract
brew install tesseract-lang
brew install poppler
brew install libjpeg

brew install tesseract-lang
# or specifically:
brew install tesseract --with-fin

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

```

📜 Code Overview
The main steps:
1.	is_scanned_pdf() — detect digital vs. scanned
2.	extract_text_native() — extract digital text
3.	extract_text_ocr() — run Tesseract OCR on pages
4.	split_sentences() — simple Finnish segmentation
5.	MarianTranslator — loads MarianMT + MPS device
6.	translate_batch() — batch GPU accelerated translation
7.	Writes English text file


🧩 Known Limitations
•	OCR accuracy depends on PDF quality.
•	Sentence splitter is rule based; complex Finnish grammar may need spaCy or HF tokenizers.
•	Very long PDFs may require batching or chunking beyond sentence-level translation.

