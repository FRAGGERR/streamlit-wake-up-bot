<h1 align="center">Streamlit Auto Wake and Status Reporter via Telegram</h1>

![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/FRAGGERR/streamlit-wake-up-bot/wakeup.yml?label=CI%2FCD&logo=github&style=flat-square)
![Repo Size](https://img.shields.io/github/repo-size/fraggerr/streamlit-wake-up-bot?style=flat-square)
![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&style=flat-square)
![Selenium](https://img.shields.io/badge/Selenium-Automation-green?logo=selenium&style=flat-square)
![Telegram Bot](https://img.shields.io/badge/Telegram-Bot%20Enabled-0088cc?logo=telegram&logoColor=white&style=flat-square)
![License](https://img.shields.io/github/license/fraggerr/streamlit-wake-up-bot?style=flat-square)
![Last Commit](https://img.shields.io/github/last-commit/fraggerr/streamlit-wake-up-bot?style=flat-square)


A GitHub Actions-powered bot to automatically wake up your free Streamlit apps using Selenium, and send you real-time status reports via Telegram.

This project is ideal for keeping your Streamlit apps responsive and minimizing cold-start delays caused by inactivity on the free tier.

---

## Features

- ⏰ Automatically runs every 12 hours (or manually) via GitHub Actions.
- 🌐 Opens and checks Streamlit app URLs using a headless browser (Selenium).
- 🔘 Detects and clicks the “wake up” button if the app is sleeping.
- ✅ Differentiates between **already awake**, **just woken up**, and **unreachable** states.
- 💬 Sends a summary to Telegram with the wake-up status of each app.
- 📊 App status is logged with a timestamp in a local CSV file (`wake_up_log.csv`).

---

## 🛠️ Requirements

- Python 3.10
- `selenium`, `webdriver_manager`, `requests`

Install dependencies:

```bash
pip install -r requirements.txt
```

## How It Works
```mermaid
graph TD
    A[GitHub Actions Scheduler] -->|Triggers every 12 hours| B[Run Wake-Up Script]
    B --> C{Visit Streamlit App}
    C -->|App sleeping| D[Click Wake-Up Button]
    C -->|App awake| E[Skip wake-up]
    D --> F[Record Success]
    E --> G[Record Status]
    F --> H[Send Telegram Report]
    G --> H
    H --> I[Update Log File]
    I --> J[Commit to Repository]
```
# 🔐 Environment Variables

Set these environment variables (in GitHub Secrets or `.env` file):

| Variable Name        | Description                          |
|----------------------|--------------------------------------|
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot API token          |
| `TELEGRAM_CHAT_ID`   | Your personal or group chat ID       |

---

# 🧾 CSV Log Output

Each run appends a new row to `wake_up_log.csv`:

| timestamp           | clearsight    | incident_management   |
|---------------------|---------------|------------------------|
| 2025-07-22 00:00:00 | clicked       | already_awake          |

---

# 📬 Telegram Message Format

### Example Message Sent:
```txt
📡 Streamlit Wake-Up Report (2025-07-22 00:00:00 IST):

🟢 Clearsight was asleep and has been woken up.

🟡 Incident Management is already awake.

🔴 Incident Management could not be reached. Error: TimeoutException
```
