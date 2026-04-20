"""
LLM-PromptCraft — Flask backend.

HW10 Technical Prototype. Single-user app (per assignment spec #8) that walks
a user through 5 RCTF lessons and then hands off to the quiz (Part 2).

Routes implemented here cover Part 1 (home + learning).
/quiz/<n> and /quiz/result are stubbed so Part 1 is click-through-complete;
Vishal + Yve + Eric own the real quiz routes.

Author (Part 1 UI): Shubham Prashar
"""

import json
import os
from datetime import datetime
from pathlib import Path

from flask import (
    Flask,
    abort,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)

BASE_DIR  = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "lessons.json"
QUIZ_PATH = BASE_DIR / "data" / "quiz.json"

app = Flask(__name__)


# ---------------------------------------------------------------------------
# Data layer
# ---------------------------------------------------------------------------
def load_lessons():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_quiz():
    with open(QUIZ_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


# In-memory "database" of the single active user's activity.
# Per HW10 requirement #8, we only support one user at a time.
# Tracks: page-entry timestamps, lesson 5 RCTF selections, quiz answers (later).
USER_STATE = {
    "started_at": None,
    "lesson_visits": [],   # list of {"lesson": n, "ts": iso}
    "build_prompt": {},    # key -> chosen option id from lesson 5
    "quiz_answers": [],    # filled in by Part 2
}


def record_visit(lesson_id):
    USER_STATE["lesson_visits"].append(
        {"lesson": lesson_id, "ts": datetime.utcnow().isoformat()}
    )


# ---------------------------------------------------------------------------
# Part 1 — Learning routes
# ---------------------------------------------------------------------------
@app.route("/")
def home():
    """Home screen with the Start button (HW10 requirement #3)."""
    return render_template("home.html")


@app.route("/start", methods=["POST"])
def start():
    """Records start time then redirects into lesson 1."""
    USER_STATE["started_at"]    = datetime.utcnow().isoformat()
    USER_STATE["lesson_visits"] = []
    USER_STATE["build_prompt"]  = {}
    USER_STATE["quiz_answers"]  = []
    return redirect(url_for("learn", n=1))


@app.route("/learn/<int:n>")
def learn(n):
    """Renders lesson n. Data-driven from lessons.json."""
    data = load_lessons()
    total = data["total_lessons"]
    if n < 1 or n > total:
        abort(404)

    lesson = data["lessons"][n - 1]
    record_visit(n)

    next_url = (
        url_for("learn", n=n + 1) if n < total else url_for("quiz_intro")
    )
    prev_url = url_for("learn", n=n - 1) if n > 1 else url_for("home")

    return render_template(
        "learn.html",
        lesson=lesson,
        current=n,
        total=total,
        next_url=next_url,
        prev_url=prev_url,
    )


@app.route("/api/build-prompt", methods=["POST"])
def api_build_prompt():
    """Lesson 5 posts the user's RCTF selections here so the backend can
    store them (HW10 requirement #4)."""
    payload = request.get_json(silent=True) or {}
    selections = payload.get("selections", {})
    # sanity-check the keys we expect
    allowed_keys = {"role", "context", "task", "format"}
    clean = {k: v for k, v in selections.items() if k in allowed_keys}
    USER_STATE["build_prompt"] = clean
    return jsonify({"ok": True, "stored": clean})


@app.route("/api/state")
def api_state():
    """Debug helper — teammates can hit /api/state to confirm user activity
    is being stored on the backend."""
    return jsonify(USER_STATE)


# ---------------------------------------------------------------------------
# Part 2 — Quiz routes
# /quiz        : intro page (Eric's template)
# /quiz/<n>    : question renderer + answer submission (Yve's template)
# /quiz/result : final score page (Eric's template)
# ---------------------------------------------------------------------------
@app.route("/quiz")
def quiz_intro():
    USER_STATE["quiz_answers"] = []
    return render_template("quiz_intro.html")


@app.route("/quiz/result")
def quiz_result():
    answers = USER_STATE.get("quiz_answers", [])
    score   = sum(1 for a in answers if a.get("is_correct"))
    total   = load_quiz()["total_questions"]
    return render_template("quiz_result.html", score=score, total=total,
                           answers=answers)


@app.route("/quiz/<int:n>", methods=["GET", "POST"])
def quiz_question(n):
    data  = load_quiz()
    total = data["total_questions"]
    if n < 1 or n > total:
        abort(404)

    question = data["questions"][n - 1]
    existing = next(
        (a for a in USER_STATE["quiz_answers"] if a["question"] == n), None
    )

    if request.method == "POST":
        if not existing:
            if question["type"] == "match":
                selected = {
                    lbl["id"]: request.form.get(f"match_{lbl['id']}", "")
                    for lbl in question["labels"]
                }
                is_correct = (selected == question["correct_answer"])
                stored     = json.dumps(selected)
            else:
                selected   = request.form.get("answer", "")
                is_correct = (selected == question["correct_answer"])
                stored     = selected

            USER_STATE["quiz_answers"].append({
                "question":   n,
                "selected":   stored,
                "is_correct": is_correct,
                "ts":         datetime.utcnow().isoformat(),
            })
        return redirect(url_for("quiz_question", n=n))

    # GET — build context for template
    answered    = existing is not None
    user_answer = None
    is_correct  = None
    if answered:
        raw = existing["selected"]
        if question["type"] == "match":
            try:
                user_answer = json.loads(raw)
            except (ValueError, TypeError):
                user_answer = {}
        else:
            user_answer = raw
        is_correct = existing["is_correct"]

    next_url = (
        url_for("quiz_question", n=n + 1) if n < total
        else url_for("quiz_result")
    )

    return render_template(
        "quiz.html",
        question=question,
        current=n,
        total=total,
        answered=answered,
        user_answer=user_answer,
        is_correct=is_correct,
        next_url=next_url,
    )


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # debug=True is fine — single-user prototype, local only.
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))
