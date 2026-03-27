from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from openai import OpenAI

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

quota = 5

@app.route("/")
def home():
    return "API is running"

@app.route("/generate", methods=["POST"])
def generate():
    global quota

    if quota <= 0:
        return jsonify({"error": "额度用完了"})

    data = request.json
    theme = data.get("theme", "")

    prompt = f"写一篇小红书爆款文案，主题是：{theme}"

    resp = client.chat.completions.create(
        model="gpt-5.3",
        messages=[{"role":"user","content":prompt}]
    )

    quota -= 1

    return jsonify({
        "text": resp.choices[0].message.content,
        "quota": quota
    })

app.run(host="0.0.0.0", port=10000)
