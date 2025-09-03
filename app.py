from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import pandas as pd

app = Flask(__name__, static_folder='.', static_url_path='')
# Enable CORS to allow requests, helpful for development
CORS(app)

# Path to the Excel file
EXCEL_FILE = 'questions.xlsx'

# Load all questions into memory once to avoid reading the file on every request
try:
    ALL_QUESTIONS_DF = pd.read_excel(EXCEL_FILE)
    # Create a lookup dictionary for answers based on the question text
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
    """API endpoint to get 10 random questions, without sending the answers."""
    if ALL_QUESTIONS_DF is None:
        return jsonify({"error": "Question file not found or is empty"}), 500
    
    # Select 10 random questions if more than 10 are available
    if len(ALL_QUESTIONS_DF) > 10:
        questions_sample_df = ALL_QUESTIONS_DF.sample(n=10)
    else:
        questions_sample_df = ALL_QUESTIONS_DF

    # Prepare questions for the frontend (without the answer)
    questions_for_frontend = questions_sample_df[['question', 'option1', 'option2', 'option3', 'option4']]
    
    return jsonify(questions_for_frontend.to_dict('records'))

@app.route('/api/submit', methods=['POST'])
def submit_answers():
    """
    API endpoint to check answers and return score.
    It looks up the correct answer on the server to prevent cheating.
    """
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
        
        # Look up the correct answer on the server using the question text
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
    # For local development, run this script and access http://127.0.0.1:5000
    app.run(debug=True, port=5000)

