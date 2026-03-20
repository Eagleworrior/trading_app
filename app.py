from flask import Flask, render_template, redirect, url_for, request, flash
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


# -------------------------
# USER MODEL
# -------------------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# -------------------------
# CREATE ADMIN
# -------------------------
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


# -------------------------
# ROUTES
# -------------------------
@app.route('/')
def home():
    return redirect(url_for('dashboard'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password_hash, password):
            flash("Invalid email or password", "danger")
            return redirect(url_for('login'))

        login_user(user)
        return redirect(url_for('dashboard'))

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/wallet')
@login_required
def wallet():
    return render_template('wallet.html')


@app.route('/trade')
@login_required
def trade():
    return render_template('trade.html')


# -------------------------
# DEPOSIT PAGE (DISPLAY ONLY)
# -------------------------
@app.route('/deposit')
@login_required
def deposit():
    return render_template('deposit.html')


# -------------------------
# WITHDRAW REQUEST (SIMULATION)
# -------------------------
@app.route('/withdraw', methods=['POST'])
@login_required
def withdraw():
    amount = request.form.get('amount')
    phone = request.form.get('phone')
    flash(f"Withdraw request received: {amount} to {phone}", "info")
    return redirect(url_for('wallet'))


# -------------------------
# TERMINAL & MARKET
# -------------------------
@app.route('/terminal')
@login_required
def terminal():
    return render_template('terminal.html')


@app.route('/market')
@login_required
def market():
    return render_template('live_market.html')


# -------------------------
# PLACE ORDER (SIMULATION)
# -------------------------
@app.route('/place_order', methods=['POST'])
@login_required
def place_order():
    symbol = request.form.get('symbol')
    order_type = request.form.get('order_type')
    quantity = request.form.get('quantity')
    side = request.form.get('side')

    flash(f"{side.upper()} order placed: {quantity} {symbol} ({order_type})", "success")
    return redirect(url_for('terminal'))


# -------------------------
# RUN APP
# -------------------------
from flask import session

@app.route('/set_mode/<mode>')
@login_required
def set_mode(mode):
    if mode not in ["real", "demo"]:
        flash("Invalid mode selected", "danger")
        return redirect(url_for('dashboard'))

    session['trade_mode'] = mode
    flash(f"Trading mode switched to {mode.upper()}", "success")
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    os.makedirs('templates/components', exist_ok=True)
    app.run(debug=True)

