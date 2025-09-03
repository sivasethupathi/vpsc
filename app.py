from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import pandas as pd

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

EXCEL_FILE = 'questions.xlsx'

try:
    ALL_QUESTIONS_DF = pd.read_excel(EXCEL_FILE)
    ANSWER_LOOKUP = ALL_QUESTIONS_DF.set_index('question')['answer'].to_dict()
except FileNotFoundError:
    ALL_QUESTIONS_DF = None
    ANSWER_LOOKUP = {}


@app.route('/')
def serve_index():
    """Serves the main HTML file."""
    return send_from_directory('.', 'index.html')

@app.route('/api/questions', methods=['GET'])
def get_questions():
    """API endpoint to get 10 random questions, including option5."""
    if ALL_QUESTIONS_DF is None:
        return jsonify({"error": "Question file not found or is empty"}), 500
    
    if len(ALL_QUESTIONS_DF) > 10:
        questions_sample_df = ALL_QUESTIONS_DF.sample(n=10)
    else:
        questions_sample_df = ALL_QUESTIONS_DF

    # Define the columns to send to the frontend, now including option5
    frontend_columns = ['question', 'option1', 'option2', 'option3', 'option4', 'option5']
    
    # Ensure all columns exist, filling missing ones with None
    for col in frontend_columns:
        if col not in questions_sample_df.columns:
            questions_sample_df[col] = None

    questions_for_frontend = questions_sample_df[frontend_columns]
    
    # Convert NaN to None for proper JSON serialization
    questions_for_frontend = questions_for_frontend.where(pd.notnull(questions_for_frontend), None)
    
    return jsonify(questions_for_frontend.to_dict('records'))

@app.route('/api/submit', methods=['POST'])
def submit_answers():
    """API endpoint to check answers and return score."""
    data = request.json
    user_answers = data.get('answers', [])
    questions_from_client = data.get('questions', [])
    
    if not questions_from_client:
        return jsonify({"error": "No questions provided for validation"}), 400

    score = 0
    summary = []
    
    for i, question_data in enumerate(questions_from_client):
        question_text = question_data.get('question')
        user_ans = user_answers[i] if i < len(user_answers) else None
        
        correct_answer = ANSWER_LOOKUP.get(question_text)
        
        is_correct = (str(user_ans) == str(correct_answer))
        if is_correct:
            score += 1
        
        summary.append({
            "question": question_text,
            "user_answer": user_ans,
            "correct_answer": correct_answer,
            "correct": is_correct
        })

    return jsonify({"score": score, "summary": summary})

if __name__ == '__main__':
    app.run(debug=True, port=5000)

