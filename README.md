# 🧠 Binance Dynamic Trading Bot (Production Ready)

A **FastAPI-based automated Binance trading system** with:

- ✅ Dynamic configuration updates via API  
- ✅ Persistent configs in SQLite or PostgreSQL  
- ✅ Asynchronous WebSocket trading stream  
- ✅ Self-healing, reconnecting WebSocket logic  
- ✅ Graceful bot start/stop per symbol  
- ✅ Production-ready Docker deployment

---

## ⚙️ Features

| Feature | Description |
|----------|--------------|
| 🧩 **Dynamic Configuration** | Update trading thresholds, quantities, and strategies live via `/bot/start`. |
| 🔄 **Self-Healing Stream** | Auto-reconnects to Binance on disconnect or WebSocket error. |
| 💾 **Persistent Database** | Symbol configs stored in SQLite or PostgreSQL with dynamic merging. |
| 🧠 **Singleton AppState** | Centralized runtime with shared database, strategy, and active bot tracking. |
| 🔒 **JWT Cookie Auth** | Protects all bot endpoints via token authentication. |
| 🐳 **Dockerized** | Runs in a production-ready container with `docker-compose`. |
| 📡 **Live & Testnet Ready** | Switch between Binance Testnet and Live API seamlessly. |

---

### 💾 Persistent Configuration Logic

Whenever `/bot/start` is called:

- The system merges configuration in order of **priority**:

### 🧩 Key Endpoints
#### 🔹 Start or Update a Bot
`POST /bot/start`
**Request Body Example:**

```json
{
  "symbol": "BTCUSDT",
  "base": "USDT",
  "buy_threshold": 0.98,
  "buy_quantity": 0.1,
  "cooldown_seconds": 300,
  "stop_loss": 0.01,
  "take_profit": 0.02,
  "max_volatility": 0.02,
  "window": 10
}
```


## 📦 Project Structure
```binancePythonProject/
│
├── api/
│ └── routes/
│ ├── index.py # FastAPI trading endpoints
│ └── trading.py # API registration
│
├── bot/
│ ├── main.py # Entry point for dynamic bot launching
│ ├── stream.py # Self-healing WebSocket streamer
│ └── simple_bot.py # Core trading logic (buy/sell signals)
│
├── config/
│ └── env_config.py # Loads API keys & environment variables
│
├── database/
│ ├── app_state.py # Singleton app state with config merging
│ └── database.py # SQLite or Postgres manager
│
├── dtos/
│ └── index.py # Data models for API & bot parameters
│
├── utils/
│ ├── binance_api.py # Connect to Binance API / Testnet
│ ├── index.py # Helpers for DataFrame handling
│ └── auth.py # Cookie-based JWT authentication
│
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── run.py # FastAPI entrypoint
```

---

## 🔧 Installation (Local)
```
uvicorn main:app --reload
```

### 1️⃣ Clone & Setup Virtual Environment

```bash
git clone https://github.com/sunnepazzy123/binancePythonProject.git
cd binancePythonProject

python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
```
### Binance Keys
TEST_API_KEY=your_testnet_api_key
TEST_SECRET_KEY=your_testnet_secret


### Database
DATABASE_URL=sqlite:///data.db

### App Config
```
JWT_SECRET="your_super_secret_key"
ENVIRONMENT=development
PORT=8000
```
### Run (Development)
```
uvicorn run:app --reload
```
Navigate to:  
[BotTrading Swagger UI](http://localhost:8000/docs)


### Example WebSocket Logs

```text
📡 Connected to BTCUSDT price stream.
💲 BTCUSDT tick: 67125.4
❌ Stream error: Read loop closed
🔁 Reconnecting in 3s...
✅ Binance client (re)connected.
📡 Reconnected to BTCUSDT price stream.

Rendered in Markdown, it will look like:
```
### Docker Deployment
```
docker-compose build
```
### Run in Detached Mode
```
docker-compose up -d
```
### Stop the Container
```
docker-compose down
```
### View Logs
```
docker-compose logs -f
```

### Example 
```
version: '3.9'

services:
  trading-bot:
    build: .
    container_name: binance_bot
    ports:
      - "8000:8000"
    env_file:
      - .env
    restart: always
    volumes:
      - .:/app
```

### 🔒 Security

- Cookie-based JWT authentication protects all endpoints  
- Never exposes API keys in logs or responses

### 💡 Tips

- Clean DB configs using your DB manager before new payloads.  
- Use **Testnet** for development and **Live** only after full validation.  
- Logs include emoji-coded severity for readability.


### 🧾 License

MIT © 2025 DarkMind Team  
Contributions welcome — fork, improve, and submit PRs.
This version:  
- Fixes the directory tree formatting.  
- Ensures all endpoints, Docker, and WebSocket features are documented.  
- Reads cleanly on GitHub, VSCode, or any Markdown renderer.