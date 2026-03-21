from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'change_this_secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trading.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.before_first_request
def create_admin():
    db.create_all()
    if not User.query.filter_by(email="admin@example.com").first():
        admin = User(
            email="admin@example.com",
            password_hash=generate_password_hash("admin123", method="pbkdf2:sha256")
        )
        db.session.add(admin)
        db.session.commit()


@app.route("/")
def home():
    return redirect(url_for("dashboard"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password_hash, password):
            flash("Invalid email or password", "danger")
            return redirect(url_for("login"))
        login_user(user)
        return redirect(url_for("dashboard"))
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


@app.route("/wallet")
@login_required
def wallet():
    return render_template("wallet.html")


@app.route("/trade")
@login_required
def trade():
    return render_template("trade.html")


@app.route("/deposit")
@login_required
def deposit():
    return render_template("deposit.html")


@app.route("/withdraw", methods=["POST"])
@login_required
def withdraw():
    amount = request.form.get("amount")
    phone = request.form.get("phone")
    flash(f"Withdraw request received: {amount} to {phone}", "info")
    return redirect(url_for("wallet"))


@app.route("/terminal")
@login_required
def terminal():
    return render_template("terminal.html")


@app.route("/market")
@login_required
def market():
    return render_template("live_market.html")


@app.route("/place_order", methods=["POST"])
@login_required
def place_order():
    symbol = request.form.get("symbol")
    order_type = request.form.get("order_type")
    quantity = request.form.get("quantity")
    side = request.form.get("side")
    flash(f"{side.upper()} order placed: {quantity} {symbol} ({order_type})", "success")
    return redirect(url_for("terminal"))


@app.route("/set_mode/<mode>")
@login_required
def set_mode(mode):
    if mode not in ["real", "demo"]:
        flash("Invalid mode selected", "danger")
        return redirect(url_for("dashboard"))
    session["trade_mode"] = mode
    flash(f"Trading mode switched to {mode.upper()}", "success")
    return redirect(url_for("dashboard"))


# ---------------- SURVEY SYSTEM ---------------- #

SURVEY_CATEGORIES = [
    {
        "id": 1,
        "title": "Tech & Gadgets",
        "level": "Beginner",
        "payout": 50,
        "questions": [
            {
                "q": "How often do you upgrade your smartphone?",
                "choices": ["Every year", "Every 2 years", "Every 3+ years", "Only when it breaks"]
            },
            {
                "q": "Which OS do you prefer?",
                "choices": ["Android", "iOS", "Windows", "Linux"]
            }
        ]
    },
    {
        "id": 2,
        "title": "Finance & Investing",
        "level": "Intermediate",
        "payout": 120,
        "questions": [
            {
                "q": "How would you describe your risk tolerance?",
                "choices": ["Low", "Medium", "High", "Very high"]
            },
            {
                "q": "What do you invest in most?",
                "choices": ["Stocks", "Crypto", "Real estate", "I don't invest"]
            }
        ]
    }
]


def get_survey_balance():
    return session.get("survey_balance", 0)


def add_survey_earnings(amount):
    session["survey_balance"] = get_survey_balance() + amount


@app.route("/surveys")
@login_required
def surveys_dashboard():
    return render_template(
        "surveys/dashboard.html",
        surveys=SURVEY_CATEGORIES,
        balance=get_survey_balance()
    )


@app.route("/surveys/<int:survey_id>", methods=["GET", "POST"])
@login_required
def take_survey(survey_id):
    survey = next((s for s in SURVEY_CATEGORIES if s["id"] == survey_id), None)
    if not survey:
        flash("Survey not found", "danger")
        return redirect(url_for("surveys_dashboard"))

    if request.method == "POST":
        add_survey_earnings(survey["payout"])
        return render_template(
            "surveys/completed.html",
            survey=survey,
            balance=get_survey_balance()
        )

    return render_template(
        "surveys/take.html",
        survey=survey,
        balance=get_survey_balance()
    )
@app.route("/create-admin")
def create_admin():
    from werkzeug.security import generate_password_hash
    from your_user_model_file import User  # adjust this import to match your project

    email = "admin@example.com"
    password = "admin123"

    # Check if user already exists
    existing = User.query.filter_by(email=email).first()
    if existing:
        return "Admin already exists!"

    # Create new admin user
    hashed = generate_password_hash(password)
    new_user = User(email=email, password=hashed)
    db.session.add(new_user)
    db.session.commit()

    return "Admin user created! Email: admin@example.com Password: admin123"
@app.route("/create-admin")
def create_admin():
    from werkzeug.security import generate_password_hash

    email = "admin@example.com"
    password = "admin123"

    # Check if user already exists
    existing = User.query.filter_by(email=email).first()
    if existing:
        return "Admin already exists!"

    # Create new admin user
    hashed = generate_password_hash(password)
    new_user = User(email=email, password=hashed)
    db.session.add(new_user)
    db.session.commit()

    return "Admin user created! Email: admin@example.com Password: admin123"


if __name__ == "__main__":
    os.makedirs("templates/components", exist_ok=True)
    port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)


