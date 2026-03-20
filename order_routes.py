kfrom flask import request, redirect, url_for
from flask_login import login_required, current_user
from models import db, Order

def register_order_routes(app):

    @app.route("/place_order", methods=["POST"])
    @login_required
    def place_order():
        symbol = request.form.get("symbol")
        order_type = request.form.get("order_type")
        quantity = request.form.get("quantity")

        # Basic validation
        if not symbol or not quantity:
            return redirect(url_for("dashboard"))

        try:
            qty = float(quantity)
        except ValueError:
            return redirect(url_for("dashboard"))

        # Create and save order
        new_order = Order(
            user_id=current_user.id,
            symbol=symbol,
            order_type=order_type,
            quantity=qty
        )

        db.session.add(new_order)
        db.session.commit()

        return redirect(url_for("dashboard"))

