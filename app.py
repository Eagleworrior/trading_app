# app.py
# TradeApp — Neon Edition ✨

from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, UserMixin, login_user,
    login_required, logout_user, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
import os

# ---------------------------------------------------
# APP CONFIGURATION
# ---------------------------------------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_secret_key_change_this'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trading.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Fix session issues (important!)
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = "danger"


# ---------------------------------------------------
# USER MODEL
# ---------------------------------------------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ---------------------------------------------------
# ROUTES
# ---------------------------------------------------

@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


# ---------------- REGISTER ---------------- #
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        if User.query.filter_by(email=email).first():
            flash("❌ User already exists!", "danger")
            return redirect(url_for("register"))

        new_user = User(
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.commit()

        flash("✅ Registration successful! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


# ---------------- LOGIN ---------------- #
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
        return redirect(url_for("dashboard"))

    return render_template("login.html")


# ---------------- LOGOUT ---------------- #
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("👋 Logged out successfully!", "info")
    return redirect(url_for("login"))


# ---------------- DASHBOARD ---------------- #
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)


# ---------------- ADMIN CREATION ---------------- #
@app.route('/create-admin')
def create_admin():
    existing = User.query.filter_by(email="admin@tradeapp.com").first()
    if existing:
        return "Admin already exists!"

    admin = User(
        email="admin@tradeapp.com",
        password_hash=generate_password_hash("admin123")
    )
    db.session.add(admin)
    db.session.commit()

    return "Admin created successfully!"


# ---------------------------------------------------
# RUN APP
# ---------------------------------------------------
if __name__ == "__main__":
    print("\033[95m" + "═══════════════════════════════════════════════" + "\033[0m")
    print("\033[96m" + "        🚀 TradeApp Neon Server Starting 🚀" + "\033[0m")
    print("\033[92m" + "        ✔ Debug Mode: ON" + "\033[0m")
    print("\033[94m" + "        ✔ Visit: http://127.0.0.1:5000" + "\033[0m")
    print("\033[95m" + "═══════════════════════════════════════════════" + "\033[0m")

    os.makedirs("templates", exist_ok=True)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

