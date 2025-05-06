"""
Minimal Flask backend for “HariBot”.
If the environment variable OPENAI_API_KEY is present, it will reply with GPT-3.5;
otherwise it falls back to a tiny rule-based answer set.
"""

from flask import Flask, request, jsonify
import os

USE_OPENAI = bool(os.getenv("OPENAI_API_KEY"))
if USE_OPENAI:
    from openai import OpenAI          
    client = OpenAI() 

app = Flask(__name__)

SYSTEM_PROMPT = """
You are Hariprashad (“Hari”) Ravikumar’s personal website chatbot.
Answer ONLY questions about Hari’s background, research, and skills.
Politely refuse unrelated requests.
Facts:
- Physics PhD candidate at New Mexico State University; graduation target Spring 2026
- Research: lattice QCD, GPU-accelerated HPC, symbolic regression (PySR)
- Collaborations: LANL, NC State; tools: CHROMA, C++, Python
"""

# ---------- helpers ----------
def gpt_reply(user_msg: str) -> str:
    resp = client.chat.completions.create( 
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": SYSTEM_PROMPT},
                  {"role": "user", "content": user_msg}],
        max_tokens=300,
    )
    return resp.choices[0].message.content.strip()


def rule_reply(user_msg: str) -> str:
    kb = {
        "name": "I'm Hariprashad Ravikumar — you can call me Hari.",
        "graduation": "I expect to finish my PhD in Spring 2026.",
        "research": "I work on lattice QCD calculations and GPU-accelerated simulations.",
    }
    for key, ans in kb.items():
        if key in user_msg.lower():
            return ans
    return "Sorry, I only answer questions about Hari’s background and work."

# ---------- routes ----------
@app.route("/")
def home():
    return app.send_static_file("index.html")  # serve simple page

@app.route("/chat", methods=["POST"])
def chat():
    msg = request.get_json().get("message", "")
    reply = gpt_reply(msg) if USE_OPENAI else rule_reply(msg)
    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(debug=True)
