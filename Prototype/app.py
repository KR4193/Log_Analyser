from flask import Flask, render_template, request, redirect, url_for
import json
import re
import sqlite3

app = Flask(__name__)

# Read the file content
with open('C:/Users/kr4193/Desktop/Log_error_reporter/Prototype/output_context.txt', 'r', encoding='utf-8') as file:
     # Replace HTML entities with actual characters
     file_content = file.read().strip()
json_like_content = file_content.replace('&quot;', '"').replace('&#x27;', "'")

# Split the content based on closing braces followed by opening braces
json_objects = []
start = 0
brace_level = 0
for i, char in enumerate(json_like_content):
    if char == '{':
        if brace_level == 0:
            start = i
        brace_level += 1
    elif char == '}':
        brace_level -= 1
        if brace_level == 0:
            json_objects.append(json_like_content[start:i+1])

# Parse each JSON object
data_list = [json.loads(obj) for obj in json_objects]

@app.route("/")
def generate_html():
    return render_template("index.html", data=data_list)

@app.route('/submit', methods=['POST'])
def submit():
    # Handle form submission
    form_data = []
    for i in range(1,len(request.form)):  # Assuming each row has 8 inputs
        test_suite = request.form.get(f'test_suite-{i}')
        if not test_suite:
            break
        test_case = request.form.get(f'test_case-{i}')
        test_description = request.form.get(f'test_description-{i}')
        classification = request.form.get(f'classification-{i}')
        reasoning = request.form.get(f'reasoning-{i}')
        correct = 'yes' if request.form.get(f'correct-{i}') == "on" else 'no'
        issue = "" if not  request.form.get(f'issue-{i}') else request.form.get(f'issue-{i}')
        reason = request.form.get(f'reason-{i}')
        form_data.append({
            'test_suite': test_suite,
            'test_case': test_case,
            'test_description': test_description,
            'classification': classification,
            'reasoning': reasoning,
            'correct': correct,
            'issue': issue,
            'reason': reason
        })
        # print(f'Row {i}: Test Suite={test_suite}, Test Case={test_case}, Test Description={test_description}, Classification={classification}, Reasoning={reasoning}, Correct={correct}, Issue={issue}, Reason={reason}')
    
    # Save form data to JSON file
    with open('C:/Users/kr4193/Desktop/Log_error_reporter/Prototype/form_data.json', 'w', encoding='utf-8') as json_file:
        json.dump(form_data, json_file, ensure_ascii=False, indent=4)
    # Connect to the database (or create it if it doesn't exist)
    conn = sqlite3.connect('C:/Users/kr4193/Desktop/Log_error_reporter/Prototype/form_data.db')
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS form_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        test_suite TEXT,
        test_case TEXT,
        test_description TEXT,
        classification TEXT,
        reasoning TEXT,
        correct TEXT,
        issue TEXT,
        reason TEXT
    )
    ''')

    # Insert form data into the database
    for entry in form_data:
        cursor.execute('''
        INSERT INTO form_data (test_suite, test_case, test_description, classification, reasoning, correct, issue, reason)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (entry['test_suite'], entry['test_case'], entry['test_description'], entry['classification'], entry['reasoning'], entry['correct'], entry['issue'], entry['reason']))

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()
    
    return redirect(url_for('generate_html'))

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)