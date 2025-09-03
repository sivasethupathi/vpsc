# api/index.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import random
import os

# ---- Load questions once per cold start ----
# Expect columns: Question, OptionA, OptionB, OptionC, OptionD, OptionE, Answer
# - "Answer" should be the correct option letter like A/B/C/D/E (case-insensitive),
#   or the exact text matching one of the options.
EXCEL_PATH = os.path.join(os.path.dirname(__file__), "..", "questions.xlsx")
df = pd.read_excel(EXCEL_PATH)

# Normalize columns (trim and unify)
df.columns = [c.strip() for c in df.columns]
required_cols = ["Question", "OptionA", "OptionB", "OptionC", "OptionD", "OptionE", "Answer"]
missing = [c for c in required_cols if c not in df.columns]
if missing:
    raise RuntimeError(f"Your Excel is missing required columns: {missing}")

# Build a clean list of question dicts we can sample from quickly
QUESTION_BANK = []
for i, row in df.iterrows():
    qid = str(i)  # stable ID from row index
    opts = {
        "A": str(row["OptionA"]),
        "B": str(row["OptionB"]),
        "C": str(row["OptionC"]),
        "D": str(row["OptionD"]),
        "E": str(row["OptionE"]),
    }
    # Accept either a letter or exact option text in "Answer"
    raw_ans = str(row["Answer"]).strip()
    ans_letter = None
    if raw_ans.upper() in opts.keys():
        ans_letter = raw_ans.upper()
    else:
        # find which letter matches the text
        for k, v in opts.items():
            if raw_ans.strip().lower() == v.strip().lower():
                ans_letter = k
                break
    if ans_letter is None:
        # Fallback: default to A to avoid crashing; better to clean Excel
        ans_letter = "A"
    QUESTION_BANK.append({
        "id": qid,
        "question": str(row["Question"]),
        "options": opts,
        "answer": ans_letter,  # keep server-side truth
    })

app = FastAPI()

# Same-origin (static page + API on the same Vercel domain). CORS open as a convenience.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # you can lock this down later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def pick_questions(n=10):
    n = min(n, len(QUESTION_BANK))
    return random.sample(QUESTION_BANK, n)

@app.get("/api/health")
def health():
    return {"ok": True}

@app.get("/api/start")
def start_quiz(n: int = 10):
    """
    Returns 10 random questions by default.
    Only send id/question/options; keep correct answers server-side.
    """
    selected = pick_questions(n)
    questions = []
    for q in selected:
        questions.append({
            "id": q["id"],
            "question": q["question"],
            "options": q["options"],  # {A,B,C,D,E}
        })
    # quiz_id is not strictly needed (stateless scoring), but returned for future extension
    return {"quiz_id": "stateless", "total": len(questions), "questions": questions}

class SubmitPayload(BaseModel):
    quiz_id: str
    answers: dict  # {question_id: "A"/"B"/"C"/"D"/"E"}

@app.post("/api/submit")
def submit(payload: SubmitPayload):
    id_to_q = {q["id"]: q for q in QUESTION_BANK}
    details = []
    correct_count = 0

    for qid, user_choice in payload.answers.items():
        q = id_to_q.get(str(qid))
        if not q:
            continue
        correct_letter = q["answer"]
        is_correct = user_choice.upper() == correct_letter
        if is_correct:
            correct_count += 1
        details.append({
            "id": qid,
            "question": q["question"],
            "your_answer": user_choice.upper(),
            "correct_answer": correct_letter,
            "is_correct": is_correct,
            "options": q["options"],
        })

    total = len(payload.answers)
    score = correct_count  # 1 point per correct
    wrong = total - correct_count
    return {
        "score": score,
        "total": total,
        "correct": correct_count,
        "wrong": wrong,
        "details": details
    }
