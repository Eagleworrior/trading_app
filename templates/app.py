from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, UserMixin, login_user,
    login_required, logout_user, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
import os

# ============================================================
#   EAGLEX TRADING TERMINAL — NEON EDITION
# ============================================================

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trading.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ============================================================
#   USER MODEL
# ============================================================
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

# ============================================================
#   LOGIN MANAGER
# ============================================================
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = "danger"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ============================================================
#   HOME
# ============================================================
@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect('/trade')
    return redirect('/login')

# ============================================================
#   REGISTER
# ============================================================
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        if User.query.filter_by(email=email).first():
            flash("❌ User already exists", "danger")
            return redirect(url_for("register"))

        new_user = User(
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.commit()

        flash("✅ Registration successful!", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

# ============================================================
#   LOGIN
# ============================================================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password_hash, password):
            flash("❌ Invalid email or password", "danger")
            return redirect(url_for("login"))

        login_user(user)
        flash("🎉 Login successful!", "success")
        return redirect('/trade')

    return render_template("login.html")

# ============================================================
#   LOGOUT
# ============================================================
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("👋 Logged out successfully!", "info")
    return redirect(url_for("login"))

# ============================================================
#   TRADING PAGES
# ============================================================
@app.route('/trade')
@login_required
def trade():
    return render_template("trade.html", user=current_user)

@app.route('/market')
@login_required
def market():
    return render_template("market.html", user=current_user)

@app.route('/wallet')
@login_required
def wallet():
    return render_template("wallet.html", user=current_user)

@app.route('/deposit')
@login_required
def deposit():
    return render_template("deposit.html", user=current_user)

@app.route('/history')
@login_required
def history():
    return render_template("history.html", user=current_user)

@app.route('/terminal')
@login_required
def terminal():
    return render_template("terminal.html", user=current_user)

@app.route('/instrument')
@login_required
def instrument():
    return render_template("instrument.html", user=current_user)

@app.route('/live_market')
@login_required
def live_market():
    return render_template("live_market.html", user=current_user)

# ============================================================
#   SURVEYS
# ============================================================
@app.route('/surveys/dashboard')
@login_required
def surveys_dashboard():
    return render_template("surveys/dashboard.html", user=current_user)

@app.route('/surveys/completed')
@login_required
def surveys_completed():
    return render_template("surveys/completed.html", user=current_user)

# ============================================================
#   WITHDRAWAL PAGE
# ============================================================
@app.route('/withdraw')
@login_required
def withdraw():
    return render_template("withdraw.html", user=current_user)

# ============================================================
#   NEON CONSOLE OUTPUT
# ============================================================
if __name__ == "__main__":
    print("\033[95m" + "═══════════════════════════════════════════════" + "\033[0m")
    print("\033[96m" + "        🚀 EAGLEX TRADING TERMINAL STARTING 🚀" + "\033[0m")
    print("\033[92m" + "        ✔ Status: RUNNING" + "\033[0m")
    print("\033[93m" + "        ✔ Mode: DEBUG" + "\033[0m")
    print("\033[94m" + "        ✔ Visit: http://127.0.0.1:5000" + "\033[0m")
    print("\033[91m" + "        ✔ Powered by: Norman" + "\033[0m")
    print("\033[95m" + "═══════════════════════════════════════════════" + "\033[0m")

    app.run(host="0.0.0.0", port=5000, debug=True)

