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

# Ensure uploads directory exists
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Download necessary NLTK resources
nltk.download("punkt")
nltk.download('punkt_tab')
nltk.download("stopwords")

from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from collections import defaultdict

stop_words = set(stopwords.words("english"))

def clean_text(text):
    tokens = word_tokenize(text)
    return [word for word in tokens if word.isalpha() and word.lower() not in stop_words]

def summarize_text(text, max_sentences=5):
    sentences = sent_tokenize(text)
    word_freq = defaultdict(int)

    for word in clean_text(text):
        word_freq[word.lower()] += 1

    # Score sentences
    sentence_scores = {}
    for sent in sentences:
        for word in word_tokenize(sent.lower()):
            if word in word_freq:
                sentence_scores[sent] = sentence_scores.get(sent, 0) + word_freq[word]

    # Sort and pick top sentences
    summarized = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:max_sentences]
    return " ".join(summarized)

async def analyze_file(pdf: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, pdf.filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(pdf.file, buffer)
    except Exception as e:
        return {"error": str(e)}

    try:
        text = ""
        doc = fitz.open(file_path)
        for page in doc:
            text += page.get_text("text") + "\n"
    except Exception:
        text = ""

    if not text.strip():
        text = extract_text(file_path)

    if not text.strip():
        return {"error": "Unable to extract text from PDF"}

    summarized_text = summarize_text(text)

    return {
        "filename": pdf.filename,
        "extracted_text": summarized_text[:1000],  # First 1000 chars
    }