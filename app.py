from flask import Flask, render_template, request, redirect, session
from questions import get_questions_for_level

app = Flask(__name__)
app.secret_key = "secret123"

# MAIN DASHBOARD (your main app home)
@app.route("/")
def home():
    return render_template("index.html")  # your main dashboard template

@app.route("/surveys")
def surveys_home():
    return redirect("/surveys/level/1")

@app.route("/surveys/level/<int:level>", methods=["GET"])
def start_survey(level):
    unlocked = session.get("unlocked_level", 1)
    if level > unlocked:
        return "This level is locked. Complete previous levels first."

    session["questions"] = get_questions_for_level(level)
    session["current_level"] = level
    return redirect(f"/surveys/level/{level}/question/0")

@app.route("/surveys/level/<int:level>/question/<int:index>", methods=["GET", "POST"])
def survey_question(level, index):
    questions = session.get("questions", [])

    if index >= len(questions):
        return redirect(f"/surveys/level/{level}/complete")

    question_text, options = questions[index]

    if request.method == "POST":
        return redirect(f"/surveys/level/{level}/question/{index+1}")

    return render_template(
        "question.html",
        level=level,
        index=index,
        question=question_text,
        options=options
    )

@app.route("/surveys/level/<int:level>/complete")
def survey_complete(level):
    session.pop("questions", None)
    next_level = level + 1
    session["unlocked_level"] = next_level
    return render_template("complete.html", level=level, next_level=next_level)

if __name__ == "__main__":
    app.run(debug=True)

