from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>Free Crypto Collector 2.0</h1>
    <h2>Сервер работает!</h2>
    <p>Учебный демонстрационный режим.</p>
    """

@app.route("/api/status")
def status():
    return jsonify({
        "status": "online",
        "mode": "demo",
        "virtual_balance": 0
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
