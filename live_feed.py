import json
import websocket
from flask_socketio import SocketIO

socketio = SocketIO()

def start_binance_stream():
    ws = websocket.WebSocketApp(
        "wss://stream.binance.com:9443/ws/btcusdt@trade",
        on_message=on_message
    )
    ws.run_forever()

def on_message(ws, message):
    data = json.loads(message)
    price = float(data["p"])
    socketio.emit("price_update", {"price": price})

