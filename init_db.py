# init_db.py
# Script to initialize the trading_app database with style ✨

from app import app, db

def init_database():
    with app.app_context():
        db.create_all()
        print("\033[95m" + "═══════════════════════════════════════════════" + "\033[0m")
        print("\033[96m" + "   🚀 TradeApp Database Initialization 🚀" + "\033[0m")
        print("\033[92m" + "   ✅ trading.db created successfully!" + "\033[0m")
        print("\033[93m" + "   📂 Location: ./trading_app/trading.db" + "\033[0m")
        print("\033[94m" + "   🎉 You can now register and log in 🎉" + "\033[0m")
        print("\033[95m" + "═══════════════════════════════════════════════" + "\033[0m")

if __name__ == "__main__":
    init_database()

