"""Interview Buddy: a local mock-interview partner for campus placements.

Runs entirely on your machine: Flask serves the page, Ollama serves Gemma.
No API keys, no cloud, nothing the interviewee says leaves the laptop.
"""
import os

import requests
from flask import Flask, jsonify, request, send_from_directory

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
MODEL = os.environ.get("OLLAMA_MODEL", "gemma3:1b")

app = Flask(__name__, static_folder="static")

ROUND_FOCUS = {
    "hr": "HR and behavioural questions (introduce yourself, strengths and weaknesses, "
    "teamwork, conflict, why this company, where do you see yourself).",
    "technical": "technical fundamentals for a fresher software role (OOP, DBMS, OS, "
    "networks, data structures, basic problem solving, questions about their own projects).",
    "mixed": "a mix of HR/behavioural and technical fundamentals, like a real campus "
    "placement panel.",
}

SYSTEM_PROMPT = """You are Interview Buddy, a patient, warm but honest mock interviewer \
helping a friend prepare for campus placement interviews.

Target role: {role}
Round: {focus}
Language: English only. Keep your English simple and clear.

Rules:
- Ask exactly ONE question at a time. Never ask two questions together.
- Questions must be realistic for a fresher. Do not repeat earlier questions.
- When feedback is requested, be specific and kind, never harsh. Praise what worked, \
name the one or two most important fixes, and show a stronger sample answer in 2-3 \
sentences using the candidate's own content where possible.
- Keep everything short. No long lectures.
"""

ANSWER_INSTRUCTION = """The candidate just answered question {n} of {total}. Reply in EXACTLY this format and nothing else:

SCORE: <whole number from 1 to 10>/10
WORKED: <one short sentence on what was good>
IMPROVE: <one or two short sentences on what to fix>
STRONGER: <a stronger version of their answer in 2-3 sentences>
{next_part}"""

NEXT_Q = "NEXT QUESTION: <question {m} of {total}, one question only>"
NO_NEXT = "(Do not ask another question. The interview is over.)"

START_INSTRUCTION = (
    "Start the interview. Greet the candidate in one short sentence, then ask "
    "question 1 of {total}. Format exactly:\n\nGREETING: <one sentence>\n"
    "NEXT QUESTION: <question 1 of {total}, one question only>"
)

FINAL_INSTRUCTION = """The interview is over. Using the whole conversation, write the final report in EXACTLY this format:

STRENGTHS: <two short bullet-style sentences>
FOCUS AREAS: <two short bullet-style sentences, the most important things to practise>
NEXT STEPS: <two concrete things to do this week>
ENCOURAGEMENT: <one warm sentence>"""


def ask_gemma(messages):
    resp = requests.post(
        f"{OLLAMA_URL}/api/chat",
        json={
            "model": MODEL,
            "messages": messages,
            "stream": False,
            "options": {"temperature": 0.7},
        },
        timeout=180,
    )
    resp.raise_for_status()
    return resp.json()["message"]["content"].strip()


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/api/health")
def health():
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=3)
        names = [m["name"] for m in r.json().get("models", [])]
        ok = any(n.startswith(MODEL.split(":")[0]) for n in names)
        return jsonify(ok=ok, model=MODEL, installed=names)
    except Exception as exc:  # Ollama not running
        return jsonify(ok=False, model=MODEL, error=str(exc))


@app.route("/api/turn", methods=["POST"])
def turn():
    data = request.get_json(force=True)
    role = (data.get("role") or "Software Engineer (fresher)").strip()[:100]
    focus = ROUND_FOCUS.get(data.get("round", "mixed"), ROUND_FOCUS["mixed"])
    total = max(3, min(int(data.get("total", 5)), 10))
    mode = data.get("mode", "start")
    history = data.get("history", [])
    n = int(data.get("n", 1))  # question number just answered

    messages = [{"role": "system", "content": SYSTEM_PROMPT.format(role=role, focus=focus)}]
    messages += [m for m in history if m.get("role") in ("user", "assistant")]

    if mode == "start":
        instruction = START_INSTRUCTION.format(total=total)
    elif mode == "answer":
        last = n >= total
        next_part = NO_NEXT if last else NEXT_Q.format(m=n + 1, total=total)
        instruction = ANSWER_INSTRUCTION.format(n=n, total=total, next_part=next_part)
    else:
        instruction = FINAL_INSTRUCTION

    messages.append({"role": "user", "content": f"[Instruction to interviewer]\n{instruction}"})

    try:
        reply = ask_gemma(messages)
    except Exception as exc:
        return jsonify(error=f"Could not reach Gemma via Ollama: {exc}"), 502
    return jsonify(reply=reply)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
