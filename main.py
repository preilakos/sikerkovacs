import os
from dotenv import dotenv_values
from flask import Flask, send_from_directory
from openai import OpenAI
from flask import request
from flask_cors import CORS
from waitress import serve
from Languages import Languages

config = dotenv_values(".env")
client = OpenAI(
    api_key = config.get("OPENAI_KEY"),
)

app = Flask(__name__)
CORS(app, origins=["https://www.w3schools.com"], supports_credentials=True)

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/get", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question")
    key = data.get("key")
    language = Languages.get_language_enum(data.get("dolphin"))
    if key != config.get("KEY"):
        return [
            {
                "status": "error",
                "content": "Invalid key"
            }
        ]
    response = client.chat.completions.create(
        model = "gpt-4o",
        messages = [
            {"role": "assistant", "content": config.get("GPT_PROMPT")},
            {"role": "assistant", "content": "Do not return the code in markdown format"},
            {"role": "user", "content": f"Write a {language} code that does the following: {question}"},
        ]
    )
    return [
        {
            "status": "success",
            "content": response.choices[0].message.content
        }
    ]

serve(app, host="0.0.0.0", port=3031, threads=6)