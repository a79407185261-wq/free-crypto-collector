
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

rewards = [
    {"id": 1, "name": "Demo Bitcoin", "amount": 10},
    {"id": 2, "name": "Demo Ethereum", "amount": 25},
    {"id": 3, "name": "Demo Token", "amount": 50},
    {"id": 4, "name": "Demo Bonus", "amount": 100}
]

PAGE = """
<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Free Crypto Collector 2.1</title>
<style>
body {
  background:#101827;color:white;font-family:Arial;
  padding:18px;margin:0
}
.container {max-width:600px;margin:auto}
.card {
  background:#1d2b40;padding:17px;
  border-radius:14px;margin:14px 0
}
h1 {color:#62e6ad}
.balance {font-size:27px;color:#62e6ad}
button {
  background:#62e6ad;border:0;padding:12px;
  border-radius:9px;font-weight:bold;margin:4px
}
input {
  padding:12px;border-radius:8px;width:90px
}
.small {color:#aab8ca;font-size:13px}
</style>
</head>
<body>
<div class="container">
<h1>Free Crypto Collector 2.1</h1>
<p>Учебная демонстрационная панель</p>

<div class="card">
<h3>Мой виртуальный баланс</h3>
<div class="balance" id="demo">0 DEMO</div>
<div class="balance" id="usdt">0.00 USDT</div>
<p class="small">Курс симуляции: 10 DEMO = 1 USDT</p>
</div>

<div class="card">
<h2>Виртуальный обмен</h2>
<input id="exchangeAmount" type="number" min="10" step="10"
placeholder="DEMO">
<button onclick="exchange()">Обменять</button>
<p id="exchangeResult" class="small"></p>
</div>

<h2>Каталог наград</h2>
<button onclick="loadCatalog()">Обновить каталог</button>
<div id="catalog"></div>

<div class="card">
<h2>Статистика</h2>
<p>Получено наград: <b id="claims">0</b></p>
<p>Всего начислено DEMO: <b id="earned">0</b></p>
</div>

<div class="card">
<h2>История операций</h2>
<div id="history">Пока пусто</div>
<button onclick="clearHistory()">Очистить историю</button>
</div>

<p class="small" id="status">Загрузка...</p>
</div>

<script>
const KEY = "fcc21_demo_data";

function getState() {
  try {
    return JSON.parse(localStorage.getItem(KEY)) || {
      demo: 0, usdt: 0, claims: 0, earned: 0, history: []
    };
  } catch(e) {
    return {
      demo: 0, usdt: 0, claims: 0, earned: 0, history: []
    };
  }
}

let state = getState();

function save() {
  localStorage.setItem(KEY, JSON.stringify(state));
  render();
}

function render() {
  document.getElementById("demo").textContent =
    state.demo + " DEMO";
  document.getElementById("usdt").textContent =
    state.usdt.toFixed(2) + " USDT";
  document.getElementById("claims").textContent =
    state.claims;
  document.getElementById("earned").textContent =
    state.earned;

  document.getElementById("history").innerHTML =
    state.history.length
      ? state.history.map(x => "<p>" + x + "</p>").join("")
      : "Пока пусто";
}

function addHistory(message) {
  const time = new Date().toLocaleString();
  state.history.unshift(time + " — " + message);
  state.history = state.history.slice(0, 100);
}

async function loadCatalog() {
  try {
    const response = await fetch("/api/rewards");
    if (!response.ok) throw new Error("Ошибка сервера");

    const data = await response.json();

    document.getElementById("catalog").innerHTML =
      data.rewards.map(item => `
        <div class="card">
          <h3>${item.name}</h3>
          <p>Награда: ${item.amount} DEMO</p>
          <button onclick="claim(${item.id})">Получить</button>
        </div>
      `).join("");

    document.getElementById("status").textContent =
      "Каталог обновлён: " + new Date().toLocaleTimeString();
  } catch(e) {
    document.getElementById("status").textContent =
      "Не удалось загрузить каталог";
  }
}

async function claim(id) {
  const response = await fetch("/api/rewards");
  const data = await response.json();
  const item = data.rewards.find(x => x.id === id);

  if (!item) return;

  state.demo += item.amount;
  state.earned += item.amount;
  state.claims += 1;

  addHistory("Получено " + item.amount + " DEMO — " + item.name);
  save();
}

function exchange() {
  const field = document.getElementById("exchangeAmount");
  const amount = Number(field.value);
  const result = document.getElementById("exchangeResult");

  if (!Number.isInteger(amount) || amount < 10 || amount % 10 !== 0) {
    result.textContent = "Введите число от 10, кратное 10.";
    return;
  }

  if (amount > state.demo) {
    result.textContent = "Недостаточно DEMO-токенов.";
    return;
  }

  state.demo -= amount;
  const received = amount / 10;
  state.usdt += received;

  addHistory("Обмен " + amount + " DEMO на " +
    received.toFixed(2) + " виртуальных USDT");

  field.value = "";
  result.textContent = "Учебный обмен выполнен!";
  save();
}

function clearHistory() {
  if (!confirm("Очистить историю операций?")) return;
  state.history = [];
  save();
}

render();
loadCatalog();
setInterval(loadCatalog, 30000);
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(PAGE)

@app.route("/api/rewards")
def get_rewards():
    return jsonify({
        "mode": "demo",
        "rewards": rewards
    })

@app.route("/api/status")
def status():
    return jsonify({
        "status": "online",
        "version": "2.1",
        "mode": "demo"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
