from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from openai import OpenAI

app = Flask(__name__)
CORS(app)  # ✅ 允许跨域访问

# 使用环境变量中的 API Key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 临时额度（内存中，不持久化）
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
    theme = data.get("theme", "").strip()

    if not theme:
        return jsonify({"error": "请输入主题"})

    prompt = f"写一篇小红书爆款文案，主题是：{theme}"

    try:
        resp = client.chat.completions.create(
            model="gpt-5.3",
            messages=[{"role":"user","content":prompt}]
        )
    except Exception as e:
        return jsonify({"error": str(e)})

    quota -= 1

    return jsonify({
        "text": resp.choices[0].message.content,
        "quota": quota
    })

if __name__ == "__main__":
    # Render 会分配端口
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
