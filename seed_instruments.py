from app import app, db
from models import Instrument

INSTRUMENTS = [
    ("BTCUSDT", "BTC", "USDT", "crypto"),
    ("ETHUSDT", "ETH", "USDT", "crypto"),
    ("BNBUSDT", "BNB", "USDT", "crypto"),
    ("SOLUSDT", "SOL", "USDT", "crypto"),

    ("EURUSD", "EUR", "USD", "forex"),
    ("GBPUSD", "GBP", "USD", "forex"),
    ("USDJPY", "USD", "JPY", "forex"),
    ("USDCHF", "USD", "CHF", "forex"),

    ("AAPL", "AAPL", "USD", "stock"),
    ("MSFT", "MSFT", "USD", "stock"),
    ("TSLA", "TSLA", "USD", "stock"),
    ("AMZN", "AMZN", "USD", "stock"),

    ("XAUUSD", "XAU", "USD", "metal"),
    ("XAGUSD", "XAG", "USD", "metal"),

    ("SPX500", "SPX", "USD", "index"),
    ("NAS100", "NAS", "USD", "index"),
]

with app.app_context():
    for symbol, base, quote, cls in INSTRUMENTS:
        existing = Instrument.query.filter_by(symbol=symbol).first()
        if not existing:
            inst = Instrument(
                symbol=symbol,
                base_asset=base,
                quote_asset=quote,
                asset_class=cls,
                active=True
            )
            db.session.add(inst)

    db.session.commit()
    print("Instruments seeded.")

