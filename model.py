from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# ===========================
# USER MODEL
# ===========================
class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    real_balance = db.Column(db.Float, default=0.0)
    demo_balance = db.Column(db.Float, default=10000.0)

    def __repr__(self):
        return f"<User {self.email}>"


# ===========================
# INSTRUMENT MODEL
# ===========================
class Instrument(db.Model):
    __tablename__ = "instrument"

    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    asset_class = db.Column(db.String(50), nullable=True)  # <— THIS MUST EXIST

    def __repr__(self):
        return f"<Instrument {self.symbol}>"


# ===========================
# ORDER MODEL
# ===========================
class Order(db.Model):
    __tablename__ = "order"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    symbol = db.Column(db.String(20), nullable=False)
    side = db.Column(db.String(10), nullable=False)
    order_type = db.Column(db.String(10), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=True)
    account_type = db.Column(db.String(10), nullable=False)

    user = db.relationship("User", backref="orders")

    def __repr__(self):
        return f"<Order {self.side} {self.symbol}>"

