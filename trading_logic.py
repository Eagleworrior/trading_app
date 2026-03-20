from models import db, Instrument, PriceTick, Order, Trade, Position, Balance, EquitySnapshot, AuditLog
from datetime import datetime

def get_last_price(instrument_id):
    tick = PriceTick.query.filter_by(instrument_id=instrument_id).order_by(PriceTick.timestamp.desc()).first()
    return tick.price if tick else None

def get_balance(user_id, currency):
    b = Balance.query.filter_by(user_id=user_id, currency=currency).first()
    if not b:
        b = Balance(user_id=user_id, currency=currency, amount=0.0)
        db.session.add(b)
        db.session.commit()
    return b

def adjust_balance(user_id, currency, delta, reason=None):
    b = get_balance(user_id, currency)
    b.amount += delta
    db.session.add(b)
    db.session.commit()
    db.session.add(AuditLog(user_id=user_id, action="balance_adjust", details=f"{delta} {currency} - {reason or ''}"))
    db.session.commit()
    return b

def place_order(user, instrument, side, order_type, qty, price=None, tp_price=None, sl_price=None, reduce_only=False):
    order = Order(
        user_id=user.id,
        instrument_id=instrument.id,
        side=side,
        type=order_type,
        qty=qty,
        price=price,
        tp_price=tp_price,
        sl_price=sl_price,
        reduce_only=reduce_only,
        status="open"
    )
    db.session.add(order)
    db.session.commit()
    if order_type == "market":
        last = get_last_price(instrument.id)
        if last:
            simulate_fill(order, last, qty)
    return order

def simulate_fill(order, fill_price, fill_qty):
    trade = Trade(order_id=order.id, user_id=order.user_id, instrument_id=order.instrument_id, qty=fill_qty, price=fill_price, side=order.side)
    db.session.add(trade)
    order.filled_qty += fill_qty
    order.status = "filled" if abs(order.filled_qty - order.qty) < 1e-9 else "partial"
    db.session.add(order)
    inst = Instrument.query.get(order.instrument_id)
    cost = fill_price * fill_qty
    if order.side == "buy":
        adjust_balance(order.user_id, inst.quote_asset, -cost, reason=f"buy {inst.symbol}")
        update_position(order.user_id, inst, fill_qty, fill_price)
    else:
        adjust_balance(order.user_id, inst.quote_asset, cost, reason=f"sell {inst.symbol}")
        update_position(order.user_id, inst, -fill_qty, fill_price)
    db.session.commit()
    return trade

def update_position(user_id, instrument, delta_qty, fill_price):
    pos = Position.query.filter_by(user_id=user_id, instrument_id=instrument.id).first()
    if not pos:
        pos = Position(user_id=user_id, instrument_id=instrument.id, qty=0.0, avg_entry_price=0.0)
        db.session.add(pos)
        db.session.flush()
    prev_qty = pos.qty
    new_qty = prev_qty + delta_qty
    if prev_qty == 0 or (prev_qty > 0 and new_qty > 0) or (prev_qty < 0 and new_qty < 0):
        if prev_qty == 0:
            pos.avg_entry_price = fill_price
        else:
            pos.avg_entry_price = ((abs(prev_qty) * pos.avg_entry_price) + (abs(delta_qty) * fill_price)) / (abs(prev_qty) + abs(delta_qty))
    else:
        if new_qty == 0:
            pos.avg_entry_price = 0.0
        else:
            pos.avg_entry_price = fill_price
    pos.qty = new_qty
    pos.updated_at = datetime.utcnow()
    db.session.add(pos)
    db.session.commit()

def evaluate_orders_on_tick(instrument_id, last_price):
    open_orders = Order.query.filter_by(instrument_id=instrument_id, status="open").all()
    for order in open_orders:
        if order.type == "limit":
            if order.side == "buy" and last_price <= order.price:
                simulate_fill(order, order.price, order.qty - order.filled_qty)
            if order.side == "sell" and last_price >= order.price:
                simulate_fill(order, order.price, order.qty - order.filled_qty)
        if order.type == "stop":
            if order.side == "buy" and last_price >= order.price:
                simulate_fill(order, last_price, order.qty - order.filled_qty)
            if order.side == "sell" and last_price <= order.price:
                simulate_fill(order, last_price, order.qty - order.filled_qty)
    positions = Position.query.filter_by(instrument_id=instrument_id).all()
    for pos in positions:
        if pos.qty == 0:
            continue
        user_orders = Order.query.filter_by(user_id=pos.user_id, instrument_id=instrument_id, status="open").all()
        for o in user_orders:
            if o.tp_price and ((pos.qty > 0 and last_price >= o.tp_price) or (pos.qty < 0 and last_price <= o.tp_price)):
                simulate_fill(o, o.tp_price, o.qty - o.filled_qty)
            if o.sl_price and ((pos.qty > 0 and last_price <= o.sl_price) or (pos.qty < 0 and last_price >= o.sl_price)):
                simulate_fill(o, o.sl_price, o.qty - o.filled_qty)

