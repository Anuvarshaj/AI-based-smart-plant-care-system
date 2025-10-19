import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("Gemini API key not found! Please set GEMINI_API_KEY in your .env file.")
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-flash-latest")

# Specify custom template folder
app = Flask(__name__, template_folder="templetes")

def chat_with_bot(prompt):
    response = model.generate_content(prompt)
    return response.text.strip()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message")
    if user_message:
        bot_message = chat_with_bot(user_message)
        return jsonify({"response": bot_message})
    return jsonify({"response": "Please send a message."})

if __name__ == "__main__":
    app.run(debug=True, port=5500)
