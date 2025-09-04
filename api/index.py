import os
import random
from pathlib import Path
from typing import List, Dict, Any

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from starlette.middleware.sessions import SessionMiddleware
import pandas as pd

# -----------------------------
# Configuration
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "question_bank.xlsx"  # <-- place your Excel here
SESSION_SECRET = os.getenv("SESSION_SECRET", "change-me-please")

# -----------------------------
# App & templates
# -----------------------------
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET)

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Optionally mount a static directory if you add custom assets:
# (Not required since we use Tailwind CDN in templates)
# app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# -----------------------------
# Data loading utilities
# -----------------------------
def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Make sure the DataFrame has consistent column names regardless of the original Excel headers."""
    # If the file is strictly positional: A..J
    # A: type, B: question, C..G: options A..E, J: answer (note: H/I ignored)
    # Try by header names first; fallback to positions.
    cols = {c: str(c).strip().lower() for c in df.columns}
    lower_names = list(cols.values())

    def get_col(df, wanted: List[str], fallback_index: int):
        for i, name in enumerate(df.columns):
            low = str(name).strip().lower()
            if low in wanted:
                return name
        # fallback by position
        return df.columns[fallback_index]

    col_type = get_col(df,
                       ["question type", "type", "category", "topic", "column a"],
                       0)
    col_q = get_col(df,
                    ["question", "ques", "column b"],
                    1)
    col_a = get_col(df, ["option a", "a", "column c"], 2)
    col_b = get_col(df, ["option b", "b", "column d"], 3)
    col_c = get_col(df, ["option c", "c", "column e"], 4)
    col_d = get_col(df, ["option d", "d", "column f"], 5)
    col_e = get_col(df, ["option e", "e", "column g"], 6)
    col_ans = get_col(df, ["answer", "ans", "correct", "column j"], 9)

    renamed = df.rename(columns={
        col_type: "type",
        col_q: "question",
        col_a: "A",
        col_b: "B",
        col_c: "C",
        col_d: "D",
        col_e: "E",
        col_ans: "answer"
    }).copy()

    # Clean strings
    for c in ["type", "question", "A", "B", "C", "D", "E", "answer"]:
        if c in renamed.columns:
            renamed[c] = renamed[c].astype(str).fillna("").str.strip()

    # Drop rows without a question
    renamed = renamed[renamed["question"].str.len() > 0]
    renamed.reset_index(drop=True, inplace=True)
    return renamed

def load_bank() -> pd.DataFrame:
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Excel file not found at {DATA_FILE}.")
    df = pd.read_excel(DATA_FILE, engine="openpyxl")
    df = _normalize_columns(df)
    return df

BANK = load_bank()

def get_types() -> List[str]:
    types = sorted([t for t in BANK["type"].dropna().unique() if str(t).strip() not in ("", "nan")])
    return types

# -----------------------------
# Helper logic
# -----------------------------
def select_questions(qtype: str, n: int = 10) -> List[int]:
    subset = BANK[BANK["type"] == qtype]
    idxs = subset.index.tolist()
    random.shuffle(idxs)
    if not idxs:
        return []
    return idxs[: min(n, len(idxs))]

def evaluate(answers: Dict[str, str], question_ids: List[int]) -> Dict[str, Any]:
    results = []
    score = 0
    for qid in question_ids:
        row = BANK.loc[qid]
        # user_answer is one of "A".."E" or "" (if unanswered)
        user_choice_letter = answers.get(str(qid), "")
        correct_field = str(row["answer"]).strip()

        # We accept either the letter (A..E) or the exact text of the correct option.
        options_map = {"A": row["A"], "B": row["B"], "C": row["C"], "D": row["D"], "E": row["E"]}

        # Determine correct letter if possible
        correct_letter = None
        up = correct_field.upper().strip()
        if up in options_map:  # "A" / "B"..
            correct_letter = up
        else:
            # Try to match by text
            for k, v in options_map.items():
                if str(v).strip().lower() == correct_field.lower():
                    correct_letter = k
                    break

        # Fallback: if nothing matched, mark as unknown and don't award score
        is_correct = False
        if correct_letter:
            is_correct = (user_choice_letter == correct_letter)
            if is_correct:
                score += 1

        results.append({
            "id": qid,
            "type": row["type"],
            "question": row["question"],
            "options": options_map,
            "user_letter": user_choice_letter or "-",
            "user_text": options_map.get(user_choice_letter, "") if user_choice_letter else "",
            "correct_letter": correct_letter or "?",
            "correct_text": options_map.get(correct_letter, "") if correct_letter else str(row["answer"]),
            "is_correct": is_correct
        })
    return {"score": score, "results": results, "total": len(question_ids)}

# -----------------------------
# Routes
# -----------------------------
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "types": get_types(),
    })

@app.post("/start", response_class=HTMLResponse)
async def start_test(request: Request, qtype: str = Form(...)):
    question_ids = select_questions(qtype, n=10)
    # Save to session for "retake same test"
    request.session["last_qtype"] = qtype
    request.session["last_question_ids"] = question_ids
    return templates.TemplateResponse("quiz.html", {
        "request": request,
        "qtype": qtype,
        "questions": [(qid, BANK.loc[qid]) for qid in question_ids],
    })

@app.post("/retake", response_class=HTMLResponse)
async def retake_test(request: Request):
    last_ids = request.session.get("last_question_ids", [])
    qtype = request.session.get("last_qtype", "")
    if not last_ids:
        # If no session, send to home
        return RedirectResponse(url="/", status_code=303)
    return templates.TemplateResponse("quiz.html", {
        "request": request,
        "qtype": qtype or "Retake",
        "questions": [(qid, BANK.loc[qid]) for qid in last_ids],
    })

@app.post("/submit", response_class=HTMLResponse)
async def submit(
    request: Request,
    duration: str = Form(...),  # "mm:ss" from JS timer
):
    # Collect answers (keys are question IDs)
    form = await request.form()
    answers = {k: v for k, v in form.items() if k.isdigit()}  # only qid fields
    # Retrieve current set from session (either fresh or retake)
    question_ids = request.session.get("last_question_ids", [])
    res = evaluate(answers, question_ids)
    qtype = request.session.get("last_qtype", "")

    return templates.TemplateResponse("results.html", {
        "request": request,
        "score": res["score"],
        "total": res["total"],
        "duration": duration,
        "qtype": qtype,
        "review": res["results"],
    })

@app.get("/health")
async def health():
    return {"ok": True, "total_questions": len(BANK), "types": get_types()}
