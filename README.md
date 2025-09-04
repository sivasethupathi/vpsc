# Bank Promotion Mock Test (FastAPI on Vercel)

A lightweight mock test platform powered by **FastAPI** and **Jinja2**.  
Reads an Excel question bank and serves **10 random questions** by **Question Type** (Column A).

## Excel Format

- **Column A**: Question Type  
- **Column B**: Question  
- **Columns C–G**: Options A–E  
- **Column J**: Correct Answer (either the **letter** `A`..`E` or the **exact option text**)

> Place your file at: `data/question_bank.xlsx`.

## Quick Start

1. Create this repo on GitHub with the structure in this project.
2. Put your Excel into `data/question_bank.xlsx`.
3. Connect the repo to **Vercel** and deploy.
4. (Optional) Set `SESSION_SECRET` in Vercel Project → Settings → Environment Variables.

## Local Development

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Run locally
uvicorn api.index:app --reload --port 8000
# Open http://127.0.0.1:8000
