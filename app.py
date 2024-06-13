from flask import Flask, request, jsonify, render_template
import requests
import re

app = Flask(__name__)

# Custom responses for specific questions
CUSTOM_RESPONSES = {
    "what is your name": "Yan AI",
    "who is your owner": "Qazi Omar"
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['GET'])
def ask():
    question = request.args.get('question', '')
    if question:
        response = get_response(question)
        return jsonify({'answer': response})
    return jsonify({'answer': 'No question provided.'})

def get_response(question):
    try:
        # Check if the question is a math problem
        if is_math_question(question):
            return calculate(question)
        
        # Check if the question has a custom response
        if question.lower() in CUSTOM_RESPONSES:
            return CUSTOM_RESPONSES[question.lower()]
        
        # Fetch answer from Wikipedia if it's not a math question or custom response
        wiki_response = get_wikipedia_summary(question)
        if wiki_response:
            return wiki_response
        
        return "Sorry, I couldn't find an answer."
    
    except Exception as e:
        return f"Error: {str(e)}"

def is_math_question(question):
    # Check if the question contains only numbers and math operators
    return re.match(r'^[0-9+\-*/.() ]+$', question)

def calculate(question):
    try:
        # Evaluate the math expression safely
        result = eval(question)
        return str(result)
    except Exception as e:
        return f"Error in calculation: {str(e)}"

def get_wikipedia_summary(query):
    headers = {
        'User-Agent': 'YanAI/1.0 (http://yourwebsite.com; your_email@example.com)',
        'Accept': 'application/json'
    }
    search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={query}&format=json"
    response = requests.get(search_url, headers=headers)
    if response.status_code == 200:
        search_results = response.json()
        if search_results['query']['search']:
            pageid = search_results['query']['search'][0]['pageid']
            summary_url = f"https://en.wikipedia.org/w/api.php?action=query&prop=extracts&pageids={pageid}&explaintext&format=json"
            summary_response = requests.get(summary_url, headers=headers)
            if summary_response.status_code == 200:
                summary_data = summary_response.json()
                page_data = summary_data['query']['pages'][str(pageid)]
                return page_data.get('extract', 'No summary available.')
    return None

if __name__ == '__main__':
    app.run(debug=True)
