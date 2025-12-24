# core/api_server.py
from flask import Flask, jsonify, request
import time

app = Flask(__name__)

# --- Core Data Simulation ---
core_status = {
    "earnings": 16746,
    "tokens": 339,
    "status": "SECURED",
    "logs": []
}

# --- Helper Functions ---
def log(msg):
    core_status["logs"].append(f"{time.strftime('%H:%M:%S')} - {msg}")
    # Keep last 50 logs
    core_status["logs"] = core_status["logs"][-50:]

# --- API Endpoints ---
@app.route("/status", methods=["GET"])
def get_status():
    return jsonify(core_status)

@app.route("/simulate_earnings", methods=["POST"])
def simulate_earnings():
    import random
    earn = random.randint(50, 500)
    token = random.randint(1, 10)
    core_status["earnings"] += earn
    core_status["tokens"] += token
    log(f"🚀 Simulated: ₹{earn}, Tokens: {token}")
    return jsonify({"success": True, "earnings": core_status["earnings"], "tokens": core_status["tokens"]})

@app.route("/force_payout", methods=["POST"])
def force_payout():
    amount = 100
    if core_status["earnings"] >= amount:
        core_status["earnings"] -= amount
        log(f"💸 Forced Payout: ₹{amount} SUCCESS")
        return jsonify({"success": True, "earnings": core_status["earnings"]})
    else:
        log(f"❌ Payout Failed: Insufficient balance")
        return jsonify({"success": False, "message": "Insufficient balance"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
