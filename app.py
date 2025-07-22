from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
import requests
import os
import csv
import time

# 🔗 Streamlit app URLs
urls = {
    "clearsight": "https://clearsight.streamlit.app/",
    "incident_management": "https://incident-management-application.streamlit.app/"
}

# ⚙️ Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# 🧠 Setup ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# ⏰ Get current time in IST
ist_time = datetime.utcnow() + timedelta(hours=5, minutes=30)
log_row = {"timestamp": ist_time.strftime("%Y-%m-%d %H:%M:%S")}
messages = []

# 🔁 Loop through each app
for name, url in urls.items():
    try:
        print(f"\n🚀 Opening: {url}")
        driver.get(url)

        wait = WebDriverWait(driver, 20)
        button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(., 'get this app back up')]")
        ))

        button.click()
        print(f"✅ Wake-up button clicked for: {name}")
        log_row[name] = "clicked"
        messages.append(f"🟢 {name.replace('_', ' ').title()} was asleep and has been woken up.")
        messages.append("")

        time.sleep(5)

    except Exception as e:
        print(f"⚠️ Skipped or already awake: {name} — {str(e)}")
        log_row[name] = "already_awake_or_error"
        messages.append(f"🟡 {name.replace('_', ' ').title()} is already awake or unreachable.")
        messages.append("")

driver.quit()
print("\n🎉 All apps processed.")



# 💬 Send Telegram Message
bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
chat_id = os.environ.get("TELEGRAM_CHAT_ID")

print(f"Telegram Credentials Check:") #add this
print(f"Bot Token Present: {bool(bot_token)}")
print(f"Chat ID Present: {bool(chat_id)}") #add this

if bot_token and chat_id:
    message_text = f"📡 Streamlit Wake-Up Report ({log_row['timestamp']} IST):\n\n" + "\n".join(messages)
    telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    try:
        response = requests.post(telegram_url, data={
            "chat_id": chat_id,
            "text": message_text,
            "parse_mode": "Markdown"
        })
        print(f"📨 Telegram message sent. Status: {response.status_code}")
    except Exception as ex:
        print(f"❌ Failed to send Telegram message: {str(ex)}")

print(f"Telegram API Response: {response.status_code}") # add this
print(f"Response Text: {response.text}")  # Add this

# 📁 Write to CSV
log_file = "wake_up_log.csv"
fieldnames = ["timestamp"] + list(urls.keys())
file_exists = os.path.isfile(log_file)

with open(log_file, mode='a', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    if not file_exists or os.stat(log_file).st_size == 0:
        writer.writeheader()
    writer.writerow(log_row)
