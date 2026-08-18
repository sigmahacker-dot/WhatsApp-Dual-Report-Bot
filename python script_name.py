# ============================================================
# WhatsApp Mass Report Bot - 100% FREE (No API Key)
# Targets: Channel + Number simultaneously
# Sources: 4 free temp-number websites (scraped)
# Run: python lisa_free_dual.py
# ============================================================

import os
import time
import json
import random
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# ---------- CONFIG ----------
SESSION_DIR = "sessions"
os.makedirs(SESSION_DIR, exist_ok=True)

# ---------- FREE TEMP NUMBER SOURCES (Scraped) ----------
def get_number_free_source1():
    """Source 1: receivesms.me (US numbers)"""
    try:
        url = "https://receivesms.me/api/get-numbers?country=US"
        res = requests.get(url, timeout=15)
        if res.status_code == 200:
            data = res.json()
            if data and len(data) > 0:
                return {'number': data[0].get('number'), 'source': 'receivesms'}
    except:
        pass
    return None

def get_number_free_source2():
    """Source 2: temp-number.org (UK numbers)"""
    try:
        url = "https://temp-number.org/api/numbers/UK"
        res = requests.get(url, timeout=15)
        if res.status_code == 200:
            data = res.json()
            if data and len(data) > 0:
                return {'number': data[0].get('number'), 'source': 'temp-number'}
    except:
        pass
    return None

def get_number_free_source3():
    """Source 3: free-sms-receive.com (scraped)"""
    try:
        url = "https://free-sms-receive.com/numbers"
        res = requests.get(url, timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')
        number = soup.find('div', class_='number')
        if number:
            return {'number': number.text.strip(), 'source': 'free-sms'}
    except:
        pass
    return None

def get_number_free_source4():
    """Source 4: receive-sms-online.info (scraped)"""
    try:
        url = "https://receive-sms-online.info/numbers"
        res = requests.get(url, timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')
        number = soup.find('div', class_='phone-number')
        if number:
            return {'number': number.text.strip(), 'source': 'receive-sms'}
    except:
        pass
    return None

# ---------- FREE OTP FETCH (Scraped) ----------
def get_otp_free(number):
    """Try all sources to fetch OTP for the number"""
    sources = [
        f"https://receivesms.me/api/get-messages?number={number}",
        f"https://temp-number.org/api/messages/{number}",
        f"https://free-sms-receive.com/messages/{number}",
        f"https://receive-sms-online.info/messages/{number}"
    ]
    for url in sources:
        try:
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                data = res.json()
                if data and isinstance(data, list):
                    for msg in data:
                        if 'code' in msg or 'otp' in msg:
                            return msg.get('code') or msg.get('otp')
        except:
            continue
    return None

# ---------- BROWSER SETUP ----------
def setup_driver():
    opts = Options()
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1280,720")
    if 'TERMUX_VERSION' in os.environ:
        opts.binary_location = "/data/data/com.termux/files/usr/bin/chromium"
        opts.add_argument("--headless")
    return webdriver.Chrome(options=opts)

# ---------- WHATSAPP LOGIN ----------
def login_whatsapp(number, otp):
    driver = setup_driver()
    driver.get("https://web.whatsapp.com")
    try:
        phone = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Phone number']"))
        )
        phone.send_keys(number)
        driver.find_element(By.XPATH, "//button[contains(text(), 'Next')]").click()
        
        otp_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter code']"))
        )
        otp_field.send_keys(otp)
        driver.find_element(By.XPATH, "//button[contains(text(), 'Next')]").click()
        
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "main")))
        print(f"✅ Logged in as {number}")
        return driver
    except Exception as e:
        print(f"❌ Login failed: {e}")
        driver.quit()
        return None

# ---------- REPORT SENDER (CHANNEL + NUMBER) ----------
def send_reports(driver, channel_target, number_target):
    """Send report to both channel and number"""
    reports_sent = 0
    
    # Report Channel (if provided)
    if channel_target:
        try:
            driver.get(f"https://web.whatsapp.com/send?phone={channel_target}")
            time.sleep(5)
            menu = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Menu']"))
            )
            menu.click()
            time.sleep(1)
            report = driver.find_element(By.XPATH, "//div[contains(text(), 'Report')]")
            report.click()
            time.sleep(1)
            confirm = driver.find_element(By.XPATH, "//button[contains(text(), 'Report')]")
            confirm.click()
            print(f"📨 Report sent to CHANNEL: {channel_target}")
            reports_sent += 1
        except Exception as e:
            print(f"❌ Channel report failed: {e}")
    
    # Report Number (if provided)
    if number_target:
        try:
            driver.get(f"https://web.whatsapp.com/send?phone={number_target}")
            time.sleep(5)
            menu = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Menu']"))
            )
            menu.click()
            time.sleep(1)
            report = driver.find_element(By.XPATH, "//div[contains(text(), 'Report')]")
            report.click()
            time.sleep(1)
            confirm = driver.find_element(By.XPATH, "//button[contains(text(), 'Report')]")
            confirm.click()
            print(f"📨 Report sent to NUMBER: {number_target}")
            reports_sent += 1
        except Exception as e:
            print(f"❌ Number report failed: {e}")
    
    return reports_sent

# ---------- MAIN LOOP ----------
def start(channel_target=None, number_target=None, count=20):
    if not channel_target and not number_target:
        print("❌ At least one target required!")
        return
    
    sources = [
        get_number_free_source1,
        get_number_free_source2,
        get_number_free_source3,
        get_number_free_source4
    ]
    
    successful = 0
    for i in range(count):
        print(f"\n🔁 Attempt {i+1}/{count}")
        
        # Try each source until we get a number
        num_data = None
        for src in sources:
            num_data = src()
            if num_data:
                print(f"📱 Got number from {num_data['source']}: {num_data['number']}")
                break
        
        if not num_data:
            print("❌ No free numbers available, retrying...")
            time.sleep(30)
            continue
        
        # Get OTP
        otp = get_otp_free(num_data['number'])
        if not otp:
            print("❌ No OTP found, trying next number...")
            continue
        print(f"🔑 OTP: {otp}")
        
        # Login and send reports
        driver = login_whatsapp(num_data['number'], otp)
        if driver:
            sent = send_reports(driver, channel_target, number_target)
            if sent > 0:
                successful += 1
            driver.quit()
        
        # Random delay to avoid detection
        delay = random.randint(60, 180)
        print(f"⏳ Waiting {delay}s before next...")
        time.sleep(delay)
    
    print(f"\n✅ Done! Successful reports: {successful}/{count}")

# ---------- RUN ----------
if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════╗
    ║   WhatsApp Dual-Report Bot - 100% FREE          ║
    ║   Targets: CHANNEL + NUMBER simultaneously      ║
    ║   No API keys, no payment, scraped numbers      ║
    ╚══════════════════════════════════════════════════╝
    """)
    
    channel = input("Enter CHANNEL number (or leave empty): ").strip()
    number = input("Enter INDIVIDUAL number (or leave empty): ").strip()
    count = int(input("How many reports to send? "))
    
    start(channel if channel else None, number if number else None, count)
