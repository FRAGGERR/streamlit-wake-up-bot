from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from datetime import datetime, timedelta
import os
import csv

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

# 📊 Prepare log row
log_row = {"timestamp": ist_time.strftime("%Y-%m-%d %H:%M:%S")}

# 🔁 Loop through each app
for name, url in urls.items():
    print(f"\n🚀 Opening: {url}")
    try:
        driver.get(url)

        # ⏳ Wait for "wake-up" button
        wait = WebDriverWait(driver, 20)
        button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(., 'get this app back up')]")
        ))

        button.click()
        print(f"✅ Wake-up button clicked for: {url}")
        log_row[name] = "clicked"
        time.sleep(5)

    except Exception as e:
        print(f"⚠️ Skipped or already awake: {url} — {str(e)}")
        log_row[name] = "already_awake_or_error"

# ✅ Done
driver.quit()
print("\n🎉 All apps processed.")

# 📁 CSV Logging
log_file = "wake_up_log.csv"
fieldnames = ["timestamp"] + list(urls.keys())

file_exists = os.path.isfile(log_file)
with open(log_file, mode='a', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    if not file_exists or os.stat(log_file).st_size == 0:
        writer.writeheader()

    writer.writerow(log_row)
