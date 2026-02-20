import argparse
import pdfplumber
import PyPDF2
import pytesseract
from PIL import Image
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import re
from tqdm import tqdm

# =========================================================
# PDF extraction (native + OCR)
# =========================================================

def is_scanned_pdf(pdf_path, min_text_chars=50):
    """
    Detect if a PDF is scanned (i.e., contains no selectable text).
    """
    reader = PyPDF2.PdfReader(pdf_path)
    total = 0
    for page in reader.pages:
        txt = page.extract_text() or ""
        total += len(txt.strip())
        if total >= min_text_chars:
            return False
    return True


def extract_text_native(pdf_path):
    """
    Extract selectable text from digital PDFs.
    """
    parts = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            txt = page.extract_text() or ""
            parts.append(txt)
    return "\n\n".join(parts)


def extract_text_ocr(pdf_path, lang="fin"):
    """
    Extract text from scanned PDFs using OCR.
    """
    out = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            pil_img = page.to_image(resolution=300).original
            if not isinstance(pil_img, Image.Image):
                pil_img = Image.fromarray(pil_img)
            txt = pytesseract.image_to_string(pil_img, lang=lang)
            out.append(txt)
    return "\n\n".join(out)


# =========================================================
# Text segmentation
# =========================================================

def split_sentences(text):
    """
    Simple rule-based Finnish sentence splitting.
    """
    sents = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s.strip() for s in sents if s.strip()]


# =========================================================
# MarianMT Translation with MPS acceleration
# =========================================================

class MarianTranslator:
    def __init__(self, model_name="Helsinki-NLP/opus-mt-fi-en"):
        print(f"Loading translation model: {model_name}")

        # Use MPS if available (Apple Silicon GPU)
        if torch.backends.mps.is_available():
            self.device = torch.device("mps")
            print("Using GPU (MPS).")
        else:
            self.device = torch.device("cpu")
            print("MPS not available — using CPU.")

        # Load tokenizer & model
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        self.model = self.model.to(self.device)

    def translate_batch(self, sentences, batch_size=8):
        """
        Translate a list of sentences in batches.
        """
        out = []
        for i in range(0, len(sentences), batch_size):
            batch = sentences[i:i + batch_size]

            enc = self.tokenizer(
                batch,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=512
            ).to(self.device)

            with torch.no_grad():
                gen = self.model.generate(**enc, max_length=512)

            decoded = self.tokenizer.batch_decode(gen, skip_special_tokens=True)
            out.extend(decoded)

        return out


# =========================================================
# Main CLI
# =========================================================

def main():
    parser = argparse.ArgumentParser(description="Translate Finnish PDF → English (local, MPS-accelerated)")
    parser.add_argument("pdf", help="Input PDF")
    parser.add_argument("--out", default="translation.txt", help="Output TXT file")
    parser.add_argument("--prefer-ocr", action="store_true", help="Force OCR even for digital PDFs")
    parser.add_argument("--batch-size", type=int, default=8, help="Batch size for translation")
    args = parser.parse_args()

    print("Extracting text from PDF...")

    if args.prefer_ocr or is_scanned_pdf(args.pdf):
        print("Using OCR...")
        text = extract_text_ocr(args.pdf, lang="fin")
    else:
        print("Using native text extraction...")
        text = extract_text_native(args.pdf)

    print("Splitting into sentences...")
    sentences = split_sentences(text)
    print(f"Found {len(sentences)} sentences.")

    print("Initializing translator...")
    translator = MarianTranslator()

    print("Translating...")
    translations = translator.translate_batch(sentences, batch_size=args.batch_size)

    print(f"Writing output → {args.out}")
    with open(args.out, "w", encoding="utf-8") as f:
        for line in translations:
            f.write(line + "\n")

    print("Done!")


if __name__ == "__main__":
    main()