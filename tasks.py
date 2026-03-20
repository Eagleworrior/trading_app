import time, random
from sqlalchemy import text
from app import create_app
from models import db, Instrument, PriceTick, EquitySnapshot, Position, Balance
from trading_logic import evaluate_orders_on_tick, get_last_price
from config import Config

app = create_app()

def snapshot_all_users():
    users = db.session.execute(text("SELECT id FROM user")).fetchall()
    for (uid,) in users:
        equity = compute_user_equity(uid)
        snap = EquitySnapshot(user_id=uid, equity=equity, currency="USD")
        db.session.add(snap)
    db.session.commit()

def compute_user_equity(user_id):
    total = 0.0
    balances = Balance.query.filter_by(user_id=user_id).all()
    for b in balances:
        if b.currency in ("USD", "USDT"):
            total += b.amount
        else:
            total += b.amount
    return total

def market_simulator_loop():
    # ⭐ THIS is the correct place for the app context
    with app.app_context():
        while True:
            instruments = Instrument.query.filter_by(active=True).all()

            for inst in instruments:
                last = PriceTick.query.filter_by(instrument_id=inst.id)\
                    .order_by(PriceTick.timestamp.desc()).first()

                base = last.price if last else (30000.0 if inst.type == "crypto" else 100.0)
                drift = 1 + random.uniform(-0.002, 0.002)
                new_price = max(0.000001, base * drift)

                tick = PriceTick(instrument_id=inst.id, price=new_price)
                db.session.add(tick)
                db.session.commit()

                evaluate_orders_on_tick(inst.id, new_price)

            snapshot_all_users()
            time.sleep(Config.SIMULATOR_TICK_SECONDS)

if __name__ == "__main__":
    market_simulator_loop()

