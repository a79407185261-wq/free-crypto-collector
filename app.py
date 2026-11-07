
from flask import Flask, jsonify, render_template_string, request
from datetime import datetime

app = Flask(__name__)

balance = 0.0
history = []

rewards = [
    {"id": 1, "name": "Demo Bitcoin", "amount": 0.25},
    {"id": 2, "name": "Demo Ethereum", "amount": 0.40},
    {"id": 3, "name": "Demo Token", "amount": 0.15},
    {"id": 4, "name": "Demo Bonus", "amount": 0.50}
]

PAGE = """
<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Free Crypto Collector 2.0</title>
<style>
body {
  margin: 0; padding: 20px;
  background: #101827; color: white;
  font-family: Arial, sans-serif;
}
.container { max-width: 600px; margin: auto; }
.card {
  background: #1d2b40; padding: 18px;
  border-radius: 14px; margin: 14px 0;
}
h1 { color: #62e6ad; }
.balance { font-size: 32px; color: #62e6ad; }
button {
  background: #62e6ad; border: 0;
  padding: 12px 18px; border-radius: 9px;
  font-weight: bold; cursor: pointer;
}
.small { color: #aab8ca; font-size: 13px; }
</style>
</head>
<body>
<div class="container">
<h1>Free Crypto Collector 2.0</h1>
<p>Учебная демонстрационная панель</p>

<div class="card">
  <h3>Виртуальный баланс</h3>
  <div class="balance" id="balance">0.00 USDT</div>
  <p class="small">Только условные единицы</p>
</div>

<h2>Каталог наград</h2>
<div id="catalog"></div>

<div class="card">
<h2>История начислений</h2>
<div id="history">Пока пусто</div>
</div>

<p class="small" id="status">Обновление каталога...</p>
</div>

<script>
async function refresh() {
  try {
    const r = await fetch('/api/data');
    const data = await r.json();

    document.getElementById('balance').textContent =
      data.balance.toFixed(2) + ' USDT';

    document.getElementById('catalog').innerHTML =
      data.rewards.map(item => `
        <div class="card">
          <h3>${item.name}</h3>
          <p>Условная награда: ${item.amount.toFixed(2)} USDT</p>
          <button onclick="claim(${item.id})">Получить</button>
        </div>
      `).join('');

    document.getElementById('history').innerHTML =
      data.history.length
        ? data.history.map(x => `<p>${x}</p>`).join('')
        : 'Пока пусто';

    document.getElementById('status').textContent =
      'Каталог обновлён: ' + new Date().toLocaleTimeString();
  } catch (e) {
    document.getElementById('status').textContent =
      'Не удалось обновить данные';
  }
}

async function claim(id) {
  const r = await fetch('/api/claim', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({id: id})
  });
  const data = await r.json();
  alert(data.message);
  refresh();
}

refresh();
setInterval(refresh, 15000);
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(PAGE)

@app.route("/api/data")
def data():
    return jsonify({
        "status": "online",
        "mode": "demo",
        "balance": balance,
        "rewards": rewards,
        "history": history
    })

@app.route("/api/claim", methods=["POST"])
def claim():
    global balance

    item = request.get_json(silent=True) or {}
    reward_id = item.get("id")

    reward = next(
        (r for r in rewards if r["id"] == reward_id),
        None
    )

    if reward is None:
        return jsonify({"message": "Награда не найдена"}), 404

    balance = round(balance + reward["amount"], 2)

    history.insert(
        0,
        f'{datetime.now().strftime("%H:%M:%S")} — '
        f'{reward["name"]}: +{reward["amount"]:.2f} USDT'
    )

    return jsonify({
        "message": "Демо-награда начислена!",
        "balance": balance
    })

@app.route("/api/status")
def status():
    return jsonify({
        "status": "online",
        "mode": "demo",
        "virtual_balance": balance
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
