from models.questionpaper import QuestionPaper  # your actual path
from bson import ObjectId

async def flatten_questions_from_paper(paper_id: str):
    paper = await QuestionPaper.get(ObjectId(paper_id))
    if not paper:
        return []

    all_questions = []
    for block in paper.question_blocks:
        context = block.context
        for q in block.questions:
            all_questions.append({
                "question_id": f"{paper_id}_{q.number}",  # unique if needed
                "paper_id": paper_id,
                "global_number": q.number,
                "context": context,
                "question": q.question,
                "options": q.options.dict(),
                "answer": q.answer
            })
    return all_questions
