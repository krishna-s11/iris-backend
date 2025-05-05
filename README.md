
# 💹 Bitcoin Trading Backend

This is a **FastAPI-based backend** for a Bitcoin trading application, featuring:

- 🔐 Authentication  
- 📊 Portfolio Management  
- 💱 Trading Operations  
- 📈 Live Price Feeds  
- ⚙️ User Preferences  
- 🚨 Alerts (Telegram/Email)  

It also integrates with **Celery** for task scheduling and background job execution.



## 🚀 Prerequisites

- Python 3.9+
- Git
- Virtual environment tool (e.g., `venv`)

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/shrey-mishra/Final_Backend.git
cd Final_Backend
```

### 2. Set Up Virtual Environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not available, install manually:

```bash
pip install fastapi uvicorn celery pydantic pydantic-settings python-dotenv
```

---

## 🔐 Configure Environment Variables

Create a `.env` file in the root directory with the following:

```env
SECRET_KEY=your-secret-key
DATABASE_URL=your-database-url
BINANCE_API_KEY=your-api-key
BINANCE_API_SECRET=your-api-secret
FERNET_KEY=your-fernet-key
BINANCE_CLIENT_ID=your-client-id
BINANCE_CLIENT_SECRET=your-client-secret
BINANCE_REDIRECT_URI=your-redirect-uri
TELEGRAM_BOT_TOKEN=your-bot-token
TELEGRAM_CHAT_ID=your-chat-id
SMTP_USERNAME=your-smtp-username
SMTP_PASSWORD=your-smtp-password
EMAIL_SENDER=your-email-sender
```

Replace placeholders with your actual credentials.

---

## 🏃 Running the Backend

### 1. Start FastAPI Server

Using Python:
```bash
python main.py
```

Or using Uvicorn directly:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Server will be accessible at:  
👉 `http://localhost:8000`

---

### 2. Start Celery Worker and Beat Scheduler

Open a new terminal and activate the environment:

```bash
celery -A app.tasks.celery worker --loglevel=info
```

Then in another terminal:

```bash
celery -A app.tasks.celery beat --loglevel=info
```

---

## 📡 API Endpoints

| Endpoint       | Description                |
|----------------|----------------------------|
| `/auth`        | Authentication routes      |
| `/portfolio`   | Portfolio management       |
| `/trading`     | Trading operations         |
| `/live`        | Live feed data             |
| `/preferences` | User preferences           |
| `/alerts`      | Alert management           |
| `/`            | Health check               |

---

## 🛠️ Development Notes

- Use `--reload` with `uvicorn` for hot-reloading during development.
- Ensure all subdirectories in `app/` (e.g., `api`, `core`) include an `__init__.py` file.

---

## 🧯 Troubleshooting

- If port `8000` isn't running:
  - Check terminal logs for errors.
  - Ensure no other process is using the port:  
    `netstat -aon | findstr :8000` (Windows)
- Make sure all environment variables are correctly defined in `.env`.

---

## 🤝 Contributing

Pull requests and issue submissions are welcome on the [GitHub repo](https://github.com/shrey-mishra/Final_Backend)!

---
