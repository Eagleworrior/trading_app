from app_backup import app, db
from models import Instrument

with app.app_context():
    db.drop_all()
    db.create_all()

    # Add default instruments
    btc = Instrument(symbol="BTCUSDT", name="Bitcoin / Tether", asset_class="crypto")
    eth = Instrument(symbol="ETHUSDT", name="Ethereum / Tether", asset_class="crypto")
    eurusd = Instrument(symbol="EURUSD", name="Euro / US Dollar", asset_class="forex")

    db.session.add_all([btc, eth, eurusd])
    db.session.commit()

    print("Database initialized successfully!")

