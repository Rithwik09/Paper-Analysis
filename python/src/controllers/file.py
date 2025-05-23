from fastapi import File, UploadFile
import shutil
import os
import fitz  # PyMuPDF
from pdfminer.high_level import extract_text
import nltk
import re

from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from collections import defaultdict

# Ensure necessary directories and resources
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

nltk.download("punkt")
nltk.download("stopwords")
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

def extract_questions_with_options(text):
    text = re.sub(r'\n+', '\n', text).strip()

    # pattern = re.compile(
    #     r'(?P<number>\d{1,3})[.)]\s*(?P<question>.+?)\s*(?=\(\s*[A-Da-d]\))'
    #     r'(?P<options>(\(\s*[A-Da-d]\).+?)(?=(\n\d{1,3}[.)]|$)))',
    #     re.DOTALL
    # )
    
     # Match patterns starting with Q[number]. and options (a)-(e)
    pattern = re.compile(
        r'Q\d+\.\s*(?P<question>.*?)(?=\(a\))'  # Question until (a)
        r'\(a\)\s*(?P<a>.*?)\s*'
        r'\(b\)\s*(?P<b>.*?)\s*'
        r'\(c\)\s*(?P<c>.*?)\s*'
        r'\(d\)\s*(?P<d>.*?)\s*'
        r'\(e\)\s*(?P<e>.*?)(?=(?:\nQ\d+\.|$))',  # until next Q<number>. or end
        re.DOTALL
    )

    # questions = []
    # for match in pattern.finditer(text):
    #     question_text = match.group("question").strip()
    #     raw_options = match.group("options")

    #     options = re.findall(r'\(\s*([A-Da-d])\)\s*(.*?)(?=(\(\s*[A-Da-d]\)|$))', raw_options, re.DOTALL)
    #     options_dict = {opt[0].upper(): opt[1].strip().replace("\n", " ") for opt in options}

    #     questions.append({
    #         "question": question_text,
    #         "options": options_dict
    #     })
    
    questions = []
    for match in pattern.finditer(text):
        questions.append({
            "question": match.group("question").replace("\n", " ").strip(),
            "options": {
                "A": match.group("a").strip().replace("\n", " "),
                "B": match.group("b").strip().replace("\n", " "),
                "C": match.group("c").strip().replace("\n", " "),
                "D": match.group("d").strip().replace("\n", " "),
                "E": match.group("e").strip().replace("\n", " "),
            }
        })

    return questions

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
        text = extract_text(file_path)

    if not text.strip():
        return {"error": "Unable to extract text from PDF"}

    questions_with_options = extract_questions_with_options(text)

    return {
        "filename": pdf.filename,
        "total_questions": len(questions_with_options),
        "questions": questions_with_options
    }
