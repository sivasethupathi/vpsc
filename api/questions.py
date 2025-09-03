import pandas as pd
import random
import json
from http.server import BaseHTTPRequestHandler
import os

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        # Allow requests from any origin (CORS)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        try:
            # The Excel file should be in the same directory as this Python script.
            # Vercel copies files from the root into the lambda environment.
            # We assume 'questions.xlsx' is in the root of the project.
            file_path = 'questions.xlsx'
            
            # Check if file exists
            if not os.path.exists(file_path):
                 raise FileNotFoundError(f"The file '{file_path}' was not found in the deployment environment.")

            # Read the Excel file
            df = pd.read_excel(file_path)

            # Ensure required columns exist
            required_cols = ['question', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer']
            if not all(col in df.columns for col in required_cols):
                raise ValueError("Excel file is missing one of the required columns: " + ", ".join(required_cols))

            # Convert dataframe to a list of dictionaries
            all_questions = df.to_dict('records')

            # Select 10 random questions if possible, otherwise select all
            num_questions_to_select = min(10, len(all_questions))
            if len(all_questions) < 10:
                print(f"Warning: Only found {len(all_questions)} questions, less than 10.")
            
            random_questions = random.sample(all_questions, num_questions_to_select)

            # Convert the list of questions to a JSON string
            response_data = json.dumps(random_questions)
            self.wfile.write(response_data.encode('utf-8'))

        except FileNotFoundError as e:
            self.send_error(500, f"Server Configuration Error: {str(e)}")
            self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
        except Exception as e:
            self.send_error(500, f"An error occurred: {str(e)}")
            self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))

        return
