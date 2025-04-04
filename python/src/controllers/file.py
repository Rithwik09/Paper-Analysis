# from fastapi import  File, UploadFile
# import shutil
# import  os  

# UPLOAD_FOLDER = "uploads"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# async def analyze_file(pdf: UploadFile = File(...)):
#     file_path = os.path.join(UPLOAD_FOLDER, pdf.filename)
#     try:
#         with open(file_path, "wb") as buffer:
#             shutil.copyfileobj(pdf.file, buffer)
#         return {"message": "File uploaded successfully", "filename" : pdf.filename }
#     except Exception as e:
#         return {"error": str(e)}

from fastapi import File, UploadFile
import shutil
import os
import fitz  # PyMuPDF
from pdfminer.high_level import extract_text
import nltk
from transformers import pipeline

# Ensure uploads directory exists
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Download necessary NLTK resources
nltk.download("punkt")
nltk.download("stopwords")

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

stop_words = set(stopwords.words("english"))

# # Optional: Load Hugging Face transformer model for text summarization
ls


# Use a smaller model instead of facebook/bart-large-cnn
text_cleaner = pipeline("text2text-generation", model="sshleifer/distilbart-cnn-12-6")

async def analyze_file(pdf: UploadFile = File(...)):
    """Uploads a PDF, extracts text using PyMuPDF & PDFMiner, and cleans it using NLP."""
    file_path = os.path.join(UPLOAD_FOLDER, pdf.filename)

    # Save the file
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(pdf.file, buffer)
    except Exception as e:
        return {"error": str(e)}

    # Extract text using PyMuPDF
    try:
        text = ""
        doc = fitz.open(file_path)
        for page in doc:
            text += page.get_text("text") + "\n"
    except Exception:
        text = ""

    # If PyMuPDF fails, use PDFMiner
    if not text.strip():
        text = extract_text(file_path)

    if not text.strip():
        return {"error": "Unable to extract text from PDF"}

    # Clean text using NLTK
    def clean_text(text):
        tokens = word_tokenize(text)
        cleaned_words = [word for word in tokens if word.isalpha() and word.lower() not in stop_words]
        return " ".join(cleaned_words)

    cleaned_text = clean_text(text)

    # (Optional) Further summarize using Hugging Face model
    summarized_text = text_cleaner(cleaned_text, max_length=300, min_length=50, do_sample=False)[0]["summary_text"]

    return {
        "filename": pdf.filename,
        "extracted_text": summarized_text[:1000],  # Preview first 1000 chars
    }