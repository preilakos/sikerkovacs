import os
from dotenv import dotenv_values
from flask import Flask, send_from_directory
from openai import OpenAI
from flask import request
from flask_cors import CORS
from waitress import serve
from Languages import Languages
from Quote import Quote



app = Flask(__name__)
CORS(app, origins=["https://www.w3schools.com"], supports_credentials=True)

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/get", methods=["POST"])
def ask():
    config = dotenv_values(".env")
    client = OpenAI(
        api_key = config.get("OPENAI_KEY"),
    )
    enabled = config.get("ENABLED") == "true"
    if (enabled == True): 
        data = request.get_json()
        if not data:
            return {"status": "error", "content": "Invalid JSON body"}, 400

        question = data.get("question")
        if not question:
            return {"status": "error", "content": "Missing parameter: question"}, 400

        key = data.get("key")
        if not key:
            return {"status": "error", "content": "Missing parameter: key"}, 400

        try:
            language = Languages().getLanguageById(int(data.get("dolphin")))
            if not language:
                return {"status": "error", "message": "Invalid language parameter: dolphin"}, 400
        except Exception as e:
            return {"status": "error", "message": str(e)}, 400
        response = client.chat.completions.create(
            model = "gpt-4o",
            messages = [
                {"role": "assistant", "content": config.get("GPT_PROMPT")},
                {"role": "assistant", "content": "Do NOT return the code in markdown format, and you MUST NOT use backticks before, or after the code."},
                {"role": "assistant", "content": "If you receive a short code snippet, you should ASSUME that you will need to fix it."},
                {"role": "user", "content": f"Write a {language} code that does the following: {question}"},
            ]
        )
        return [
            {
                "status": "success",
                "content": response.choices[0].message.content
            }
        ]
    else:
        quote = Quote.getRandomQuote()
        return {
            "status": "success",
            "content": quote.__str__() if quote else "Mindenki a maga sikere kovácsa."
        }

serve(app, host="0.0.0.0", port=3031, threads=6)