import random
from flask import (
    Flask, render_template, redirect,
    url_for, request, flash
)
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, UserMixin, login_user,
    login_required, logout_user, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash

# ============================================================
#   EAGLEX TRADING TERMINAL + AI SURVEYS — NEON EDITION
# ============================================================

app = Flask(__name__)
app.config["SECRET_KEY"] = "super_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ============================================================
#   MODELS
# ============================================================

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    balance = db.Column(db.Float, default=0.0)  # survey earnings


class SurveyLevel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level_number = db.Column(db.Integer, nullable=False)
    reward = db.Column(db.Float, default=4.0)
    unlocked = db.Column(db.Boolean, default=False)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class SurveyQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level_id = db.Column(db.Integer, db.ForeignKey("survey_level.id"))
    question = db.Column(db.String(500))
    choice1 = db.Column(db.String(200))
    choice2 = db.Column(db.String(200))
    choice3 = db.Column(db.String(200))
    choice4 = db.Column(db.String(200))
    correct = db.Column(db.String(200))
    explanation = db.Column(db.String(500))
    answered = db.Column(db.Boolean, default=False)


class SurveyAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey("survey_question.id"))
    selected = db.Column(db.String(200))
    correct = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


# ============================================================
#   LOGIN MANAGER
# ============================================================

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "danger"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ============================================================
#   AI QUESTION + EXPLANATION ENGINE
# ============================================================

def generate_ai_question(level):
    qa_bank = [
        (
            "What does CPU stand for?",
            ["Central Processing Unit", "Computer Power Utility", "Central Power Unit", "Control Processing Utility"],
            "Central Processing Unit",
            "A CPU is the main processor that executes instructions inside a computer."
        ),
        (
            "Which company created the iPhone?",
            ["Apple", "Samsung", "Nokia", "Huawei"],
            "Apple",
            "Apple released the first iPhone in 2007, changing the smartphone industry."
        ),
        (
            "What planet is known as the Red Planet?",
            ["Mars", "Jupiter", "Venus", "Mercury"],
            "Mars",
            "Mars appears red because of iron oxide (rust) on its surface."
        ),
        (
            "What gas do plants absorb from the air?",
            ["Carbon Dioxide", "Oxygen", "Nitrogen", "Hydrogen"],
            "Carbon Dioxide",
            "Plants absorb CO₂ during photosynthesis and release oxygen."
        ),
        (
            "Which is the largest ocean on Earth?",
            ["Pacific Ocean", "Atlantic Ocean", "Indian Ocean", "Arctic Ocean"],
            "Pacific Ocean",
            "The Pacific Ocean is the largest and deepest ocean on Earth."
        ),
        (
            "What is 12 × 12?",
            ["144", "124", "112", "132"],
            "144",
            "12 multiplied by 12 equals 144."
        ),
        (
            "What is the square root of 81?",
            ["9", "8", "7", "6"],
            "9",
            "The square root of 81 is 9 because 9 × 9 = 81."
        ),
    ]

    question, choices, correct, explanation = random.choice(qa_bank)
    random.shuffle(choices)
    return question, choices, correct, explanation


# ============================================================
#   AUTH ROUTES
# ============================================================

@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("trade"))
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if User.query.filter_by(email=email).first():
            flash("❌ User already exists", "danger")
            return redirect(url_for("register"))

        user = User(
            email=email,
            password_hash=generate_password_hash(password),
            balance=0.0
        )
        db.session.add(user)
        db.session.commit()
        flash("✅ Registration successful!", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password_hash, password):
            flash("❌ Invalid email or password", "danger")
            return redirect(url_for("login"))

        login_user(user)
        flash("🎉 Login successful!", "success")
        return redirect(url_for("trade"))

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("👋 Logged out successfully!", "info")
    return redirect(url_for("login"))


# ============================================================
#   TRADING ROUTES (TEMPLATES YOU ALREADY HAVE)
# ============================================================

@app.route("/trade")
@login_required
def trade():
    return render_template("trade.html", user=current_user)


@app.route("/wallet")
@login_required
def wallet():
    return render_template("wallet.html", user=current_user)


@app.route("/deposit")
@login_required
def deposit():
    return render_template("deposit.html", user=current_user)


@app.route("/history")
@login_required
def history():
    return render_template("history.html", user=current_user)


@app.route("/terminal")
@login_required
def terminal():
    return render_template("terminal.html", user=current_user)


@app.route("/markets")
@login_required
def markets():
    return render_template("markets.html", user=current_user)


@app.route("/market_chart")
@login_required
def market_chart():
    return render_template("market_chart.html", user=current_user)


@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)


@app.route("/signals")
@login_required
def signals():
    return render_template("signals.html", user=current_user)


@app.route("/tasks")
@login_required
def tasks():
    return render_template("tasks.html", user=current_user)


# ============================================================
#   SURVEY DASHBOARD
# ============================================================

@app.route("/surveys/dashboard")
@login_required
def surveys_dashboard():
    levels = SurveyLevel.query.filter_by(user_id=current_user.id).order_by(SurveyLevel.level_number).all()

    if not any(l.level_number == 1 for l in levels):
        lvl1 = SurveyLevel(
            level_number=1,
            reward=4.0,
            unlocked=True,
            completed=False,
            user_id=current_user.id
        )
        db.session.add(lvl1)
        db.session.commit()
        levels = SurveyLevel.query.filter_by(user_id=current_user.id).order_by(SurveyLevel.level_number).all()

    return render_template("surveys/dashboard.html", user=current_user, levels=levels)


# ============================================================
#   START LEVEL (GENERATE 50 QUESTIONS)
# ============================================================

@app.route("/surveys/start/<int:level>")
@login_required
def start_level(level):
    lvl = SurveyLevel.query.filter_by(level_number=level, user_id=current_user.id).first()
    if not lvl:
        flash("Level not found.", "danger")
        return redirect(url_for("surveys_dashboard"))

    if not lvl.unlocked:
        flash("This level is locked.", "danger")
        return redirect(url_for("surveys_dashboard"))

    questions = SurveyQuestion.query.filter_by(level_id=lvl.id).all()
    if len(questions) == 0:
        for _ in range(50):
            q_text, choices, correct, explanation = generate_ai_question(level)
            q = SurveyQuestion(
                level_id=lvl.id,
                question=q_text,
                choice1=choices[0],
                choice2=choices[1],
                choice3=choices[2],
                choice4=choices[3],
                correct=correct,
                explanation=explanation
            )
            db.session.add(q)
        db.session.commit()

    return redirect(url_for("survey_question", level=level, qnum=1))


# ============================================================
#   QUESTION FLOW (ONE AT A TIME + EXPLANATION)
# ============================================================

@app.route("/surveys/<int:level>/<int:qnum>", methods=["GET", "POST"])
@login_required
def survey_question(level, qnum):
    lvl = SurveyLevel.query.filter_by(level_number=level, user_id=current_user.id).first()
    if not lvl:
        flash("Level not found.", "danger")
        return redirect(url_for("surveys_dashboard"))

    questions = SurveyQuestion.query.filter_by(level_id=lvl.id).order_by(SurveyQuestion.id).all()
    total = len(questions)

    if total == 0:
        flash("No questions found for this level.", "danger")
        return redirect(url_for("surveys_dashboard"))

    if qnum > total:
        if not lvl.completed:
            lvl.completed = True
            current_user.balance += lvl.reward
            db.session.commit()

            next_level_num = level + 1
            next_lvl = SurveyLevel.query.filter_by(
                level_number=next_level_num,
                user_id=current_user.id
            ).first()

            if not next_lvl:
                next_lvl = SurveyLevel(
                    level_number=next_level_num,
                    reward=4.0,
                    unlocked=True,
                    completed=False,
                    user_id=current_user.id
                )
                db.session.add(next_lvl)
                db.session.commit()

            flash(f"Level {level} completed! +{lvl.reward} EUR added.", "success")

        return redirect(url_for("surveys_dashboard"))

    q = questions[qnum - 1]

    if request.method == "POST":
        selected = request.form.get("choice")
        is_correct = (selected == q.correct)

        ans = SurveyAnswer(
            question_id=q.id,
            selected=selected,
            correct=is_correct,
            user_id=current_user.id
        )
        q.answered = True
        db.session.add(ans)
        db.session.commit()

        return render_template(
            "surveys/explanation.html",
            q=q,
            level=level,
            qnum=qnum,
            total=total,
            correct=is_correct,
            explanation=q.explanation
        )

    progress = int((qnum - 1) / total * 100)

    return render_template(
        "surveys/question.html",
        q=q,
        level=level,
        qnum=qnum,
        total=total,
        progress=progress
    )

# ============================================================
#   WITHDRAWAL PAGE (MIN 500 EUR)
# ============================================================

@app.route("/withdraw", methods=["GET", "POST"])
@login_required
def withdraw():
    if request.method == "POST":
        amount = float(request.form.get("amount") or 0)
        method = request.form.get("method")
        account = request.form.get("account")

        if current_user.balance < 500:
            flash("Minimum withdrawal is 500 EUR. Keep completing levels to reach it.", "danger")
            return redirect(url_for("withdraw"))

        if amount <= 0 or amount > current_user.balance:
            flash("Invalid amount.", "danger")
            return redirect(url_for("withdraw"))

        current_user.balance -= amount
        db.session.commit()
        flash("Withdrawal request submitted successfully!", "success")
        return redirect(url_for("withdraw"))

    return render_template("withdraw.html", user=current_user)


# ============================================================
#   NEON CONSOLE OUTPUT
# ============================================================

if __name__ == "__main__":
    import os

    print("\033[95m" + "═══════════════════════════════════════════════" + "\033[0m")
    print("\033[96m" + "        🚀 EAGLEX TRADING + AI SURVEYS 🚀" + "\033[0m")
    print("\033[92m" + "        ✔ Status: RUNNING" + "\033[0m")
    print("\033[93m" + "        ✔ Mode: DEBUG" + "\033[0m")
    print("\033[94m" + "        ✔ Visit: http://127.0.0.1:5000" + "\033[0m")
    print("\033[91m" + "        ✔ Minimum Withdrawal: 500 EUR" + "\033[0m")
    print("\033[95m" + "═══════════════════════════════════════════════" + "\033[0m")

    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)

