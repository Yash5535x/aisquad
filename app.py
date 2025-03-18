# app.py
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Configure Gemini - PASTE YOUR API KEY HERE

genai.configure(api_key="")  # 🔴 Replace with actual key
model = genai.GenerativeModel('gemini-1.5-pro')

FIN_AI_PROMPT = """You are Finsavvy - a personal finance expert. Your capabilities include:
1. Analyzing spending patterns and categorizing expenses
2. Creating personalized budgets based on income/expenses
3. Suggesting small investment opportunities (stocks, ETFs, crypto)
4. Generating saving strategies for financial goals
5. Providing financial habit improvement tips
6. Answering finance-related questions

Formatting Rules:
1. Language Matching: Respond in the same language as the query, primarily English
2. Response Depth:
    - Dont Use *,**,***,etc 
   - Simple queries (greetings, yes/no): 1-line response
   - Basic questions: 2-3 line summary + ► Details
   - Complex questions: Detailed steps + resources

3. Never show ► Details for:
   - Greetings
   - Simple questions
   - Yes/no answers
   - Weather greetings

4. Structure:
- Dont Use *,**,***,etc 
   <response>
   <summary>[Concise answer]</summary>
   <details>[Optional elaboration]</details>
   <resources>[Relevant schemes/links]</resources>
   </response>"""

SUGGESTED_QUESTIONS = [
    "How can I save for a vacation?",
    "What's a good budget for $5000 monthly income?",
    "Suggest low-risk investment options",
    "Help me analyze my spending habits",
    "How to build an emergency fund?",
    "Best way to pay off credit card debt?"
]

@app.route('/')
def home():
    return render_template('index.html', suggested_questions=SUGGESTED_QUESTIONS)

@app.route('/ask', methods=['POST'])
def ask_ai():
    try:
        user_message = request.json.get('message')
        chat = model.start_chat(history=[])
        response = chat.send_message(
            f"{FIN_AI_PROMPT}\nUser Query: {user_message}",
            safety_settings={'HARM_CATEGORY_HARASSMENT': 'BLOCK_NONE',
                             'HARM_CATEGORY_HATE_SPEECH': 'BLOCK_NONE',
                             'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'BLOCK_NONE',
                             'HARM_CATEGORY_DANGEROUS_CONTENT': 'BLOCK_NONE'}
        )
        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)