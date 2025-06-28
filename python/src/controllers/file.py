from fastapi import File, UploadFile, Request
import shutil, os, fitz, re
import os
import fitz  # PyMuPDF
from pdfminer.high_level import extract_text
import nltk
import re
from collections import defaultdict

from models.questionpaper import QuestionPaper, QuestionBlockSchema, QuestionSchema, OptionSchema
from models.vector_metadata import QuestionVectorMetadata

# Setup

nltk.download("punkt")
nltk.download("stopwords")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# --------- Text Utilities ---------
def extract_directions(text):
    """
    Extract direction/context paragraphs like 'Directions (x-y): ...' and map them to question numbers.
    """
    pattern = re.compile(r'Directions\s*\((\d+)-(\d+)\):\s*(.*?)(?=Directions\s*\(|Q\d+\.)', re.DOTALL)
    direction_map = {}
    # for match in pattern.finditer(text):
    #     start = int(match.group(1))
    #     end = int(match.group(2))
    #     context = match.group(3).strip().replace("\n", " ")
    #     for q_num in range(start, end + 1):
    #         direction_map[q_num] = context
    # return direction_map
    for match in pattern.finditer(text):
        for q_num in range(int(match.group(1)), int(match.group(2)) + 1):
            direction_map[q_num] = match.group(3).strip().replace("\n", " ")
    return direction_map

def extract_questions_with_options(text):
    """
    Extract questions in format: Q1. <question> (a) <opt> (b) <opt> ...
    """
    pattern = re.compile(
        r'Q(?P<num>\d+)\.\s*(?P<question>.*?)(?=\(a\))'
        r'\(a\)\s*(?P<a>.*?)\s*'
        r'\(b\)\s*(?P<b>.*?)\s*'
        r'\(c\)\s*(?P<c>.*?)\s*'
        r'\(d\)\s*(?P<d>.*?)\s*'
        r'\(e\)\s*(?P<e>.*?)(?=(?:\nQ\d+\.|Directions\s*\(|$))',
        re.DOTALL
    )

    questions = []
    for match in pattern.finditer(text):
        q_num = int(match.group("num"))
        questions.append({
            # "number": q_num,
            "number": int(match.group("num")),
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

def extract_answer_keys(text):
    """
    Extract answer keys in format: S32. Ans.(b)
    """
    # pattern = re.compile(r'S(\d+)\.\s*Ans\.\((?P<ans>[a-eA-E])\)', re.IGNORECASE)
    # answers = {}
    # for match in pattern.finditer(text):
    #     q_num = int(match.group(1))
    #     ans = match.group("ans").upper()
    #     answers[q_num] = ans
    # return answers
    pattern = re.compile(r'S(\d+)\.\s*Ans\.\((?P<ans>[a-eA-E])\)', re.IGNORECASE)
    return {int(m.group(1)): m.group("ans").upper() for m in pattern.finditer(text)}

# --------- Main FastAPI Analysis Function ---------
# async def analyze_file(pdf: UploadFile = File(...)):
async def analyze_file(request: Request, pdf: UploadFile):
    print("Analyzing file:", pdf.filename)
    file_path = os.path.join(UPLOAD_FOLDER, pdf.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(pdf.file, buffer)

    try:
    #     text = ""
    #     doc = fitz.open(file_path)
    #     for page in doc:
    #         text += page.get_text("text") + "\n"
    # except Exception:
    #     text = extract_text(file_path)
        text = "".join([page.get_text("text") for page in fitz.open(file_path)])
    except Exception:
        text = extract_text(file_path)

    if not text.strip():
        return {"error": "Unable to extract text from PDF"}

    # Step 1: Extract everything
    direction_map = extract_directions(text)
    questions = extract_questions_with_options(text)
    # answer_keys = extract_answer_keys(text)
    answers = extract_answer_keys(text)
    # Step 2: Merge answers
    for q in questions:
        # q_num = q["number"]
        # q["answer"] = answer_keys.get(q_num)
        q["answer"] = answers.get(q["number"])
    # Step 3: Group questions by context or standalone
    grouped_blocks = defaultdict(list)
    for q in questions:
        context = direction_map.get(q["number"])
        group_key = context if context else f"standalone-{q['number']}"
        grouped_blocks[group_key].append(q)

    # Step 4: Format final output
    output_blocks = []
    for key, qlist in grouped_blocks.items():
        block = {"questions": qlist}
        if not key.startswith("standalone-"):
            block["context"] = key
        output_blocks.append(block)

    # return {
    #     "filename": pdf.filename,
    #     "total_questions": len(questions),
    #     "question_blocks": output_blocks
    # }
    document = {
        "originalFilename": pdf.filename,
        "backendFilename": os.path.basename(file_path),
        "total_questions": len(questions),
        "question_blocks": output_blocks,
    }

    result = await request.app.mongodb["questionpapers"].insert_one(document)

    return {
        "message": "File processed and saved to MongoDB",
        "inserted_id": str(result.inserted_id),
        "total_questions": len(questions),
    }

