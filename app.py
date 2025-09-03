import pandas as pd
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os

# Initialize the Flask application
app = Flask(__name__)
# Enable Cross-Origin Resource Sharing to allow the frontend to communicate with this backend
CORS(app)

# --- Data Loading ---
# Load the questions from the Excel file into a pandas DataFrame.
# This is done once when the server starts to avoid reloading the file on every request.
try:
    # The file 'questions.xlsx' should be in the same directory as this script.
    QUESTIONS_FILE = 'questions.xlsx'
    df = pd.read_excel(QUESTIONS_FILE)
    # Convert dataframe to a list of dictionaries for easier processing
    questions_data = df.to_dict('records')
except FileNotFoundError:
    print(f"Error: The file '{QUESTIONS_FILE}' was not found. Please make sure it exists.")
    # Create a dummy DataFrame if the file doesn't exist to prevent crashing on startup.
    questions_data = []

# --- API Routes ---

@app.route('/')
def serve_index():
    """
    Serves the main HTML file of the application.
    This allows us to host both frontend and backend from the same place.
    """
    return send_from_directory('.', 'index.html')

@app.route('/get_questions', methods=['GET'])
def get_questions():
    """
    This endpoint selects 10 random questions from the loaded data and returns them.
    It carefully excludes the 'CorrectAnswer' column to prevent cheating.
    """
    if not questions_data:
        return jsonify({"error": "Questions file not found or is empty."}), 500
        
    # Use pandas DataFrame sampling to get 10 random questions
    random_questions_df = df.sample(n=10)
    
    # Define the columns we want to send to the user (all except the correct answer)
    columns_to_send = ['Question', 'OptionA', 'OptionB', 'OptionC', 'OptionD', 'OptionE']
    
    # Create a new DataFrame with only the desired columns
    questions_for_user = random_questions_df[columns_to_send]
    
    # Convert the result to a list of dictionaries and return as JSON
    return jsonify(questions_for_user.to_dict('records'))

@app.route('/submit_test', methods=['POST'])
def submit_test():
    """
    This endpoint receives the user's answers, calculates the score,
    and generates a summary of correct and incorrect answers.
    """
    if not questions_data:
        return jsonify({"error": "Questions file not found or is empty."}), 500
        
    user_answers = request.json
    score = 0
    summary = []

    # Iterate through each answer submitted by the user
    for answer in user_answers:
        question_text = answer.get('Question')
        selected_answer_key = answer.get('selected_answer') # e.g., 'A', 'B', 'C'

        # Find the full question data in our original DataFrame using the question text as a key
        # We set the index to 'Question' for easy lookup with .loc
        question_details = df.set_index('Question').loc[question_text]
        correct_answer_key = question_details['CorrectAnswer']
        
        # Check if the user's answer is correct
        if selected_answer_key == correct_answer_key:
            score += 1
            status = 'Correct'
        else:
            status = 'Incorrect'
            
        # Get the full text of the correct answer for the summary
        correct_answer_value = question_details[f'Option{correct_answer_key}']

        # Add the details to our summary list
        summary.append({
            'question': question_text,
            'selected_answer': selected_answer_key,
            'correct_answer_key': correct_answer_key,
            'correct_answer_value': correct_answer_value,
            'status': status
        })

    # Return the final score and the detailed summary as JSON
    return jsonify({
        'score': score,
        'summary': summary
    })


# --- Main Execution ---
if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    # Run the app. 'host="0.0.0.0"' makes it accessible from your network.
    app.run(host='0.0.0.0', port=port, debug=True)
