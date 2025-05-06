from flask import Flask, request, jsonify
import os

USE_OPENAI = bool(os.getenv("OPENAI_API_KEY"))
if USE_OPENAI:
    from openai import OpenAI          
    client = OpenAI() 

app = Flask(__name__)

with open("prompt_info.txt", "r") as f:
    SYSTEM_PROMPT = f.read()


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


@app.route("/")
def home():
    return app.send_static_file("index.html") 

@app.route("/chat", methods=["POST"])
def chat():
    msg = request.get_json().get("message", "")
    reply = gpt_reply(msg) if USE_OPENAI else rule_reply(msg)
    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(debug=True)
