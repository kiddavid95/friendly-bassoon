<<<<<<< HEAD
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import time
import dateparser

# ----------------------
# Selenium setup
# ----------------------
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service(executable_path="chromedriver.exe")

# ----------------------
# Search configuration
# ----------------------
search_bar_input = "Kawasaki Z750"
money_min = "3001"
money_max = "4200"

# ----------------------
# Step 1-6: Search & pagination
# ----------------------

# site settings
driver = webdriver.Chrome(service=service, options=options)
print("[1/10] Opening OLX...")
driver.get("https://www.olx.ro/")
time.sleep(1)

# cookies
print("[2/10] Accepting Cookies...")
driver.find_element(By.ID, "onetrust-accept-btn-handler").click()

# search bar
print(f"[3/10] Searching for '{search_bar_input}'...")
search_bar = driver.find_element(By.ID, "search")
search_bar.clear()
search_bar.send_keys(search_bar_input + Keys.ENTER)
time.sleep(3)

# currency
print("[4/10] Setting currency to Euro...")
driver.find_element(By.CSS_SELECTOR, "[data-testid='currency-item']").click()
time.sleep(3)

# price range
print(f"[5/10] Setting price range (min: {money_min}, max: {money_max})...")
money_range_min = driver.find_element(By.NAME, "range-from-input")
money_range_min.clear()
money_range_min.send_keys(money_min + Keys.ENTER)
time.sleep(2)
money_range_max = driver.find_element(By.NAME, "range-to-input")
money_range_max.clear()
money_range_max.send_keys(money_max + Keys.ENTER)
time.sleep(2)

WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.css-1sw7q4x"))
)

# ad collecting
print("[6/10] Collecting all ad links...")
all_links = []
page = 1
while True:
    display_page = 7 + page / 10
    print(f"[{display_page:.1f}/9] Parsing page {page}...")
    soup = BeautifulSoup(driver.page_source, "html.parser")
    ads = soup.select("div.css-1sw7q4x a")
    for ad in ads:
        href = ad.get("href")
        if href:
            if href.startswith("/"):
                href = "https://www.olx.ro" + href
            all_links.append(href)
    try:
        next_page = driver.find_element(By.CSS_SELECTOR, "a[data-testid='pagination-forward']")
        next_url = next_page.get_attribute("href")
        if not next_url:
            break
        driver.get(next_url)
        time.sleep(3)
        page += 1
    except:
        break

# duplicates removal
final_links = list(dict.fromkeys(all_links))
print(f"[8/10] Found {len(final_links)} unique ads.")

# ----------------------
# Step 7: Fetch posted dates using Selenium
# ----------------------
def fetch_ad_date(link):
    ad_driver = webdriver.Chrome(service=service, options=options)
    try:
        ad_driver.get(link)
        try:
            date_elem = WebDriverWait(ad_driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='ad-posted-at']"))
            )
            posted_date = date_elem.text.strip()
        except:
            posted_date = "N/A"
    finally:
        ad_driver.quit()
    return {"link": link, "date": posted_date}

# fetching post data
print("[9/10] Fetching posted dates for all ads...")
ads_with_date = []
with ThreadPoolExecutor(max_workers=5) as executor:
    ads_with_date = list(executor.map(fetch_ad_date, final_links))

# ----------------------
# Step 8: Parse dates & sort
# ----------------------

for ad in ads_with_date:
    ad["parsed_date"] = dateparser.parse(ad["date"], languages=["ro"]) or dateparser.parse("1 Jan 1900")

ads_sorted = sorted(
    ads_with_date,
    key=lambda x: x["parsed_date"],
    reverse=True
)

# ----------------------
# Step 9: Print results
# ----------------------

print(f"[10/10] Done! Found {len(final_links)} unique ads sorted by newest date:")
for ad in ads_sorted:
    print(f"{ad['date']}: {ad['link']}")
=======
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import time
import dateparser

# ----------------------
# Selenium setup
# ----------------------
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service(executable_path="chromedriver.exe")

# ----------------------
# Search configuration
# ----------------------
search_bar_input = "Kawasaki Z750"
money_min = "3001"
money_max = "4200"

# ----------------------
# Step 1-6: Search & pagination
# ----------------------

# site settings
driver = webdriver.Chrome(service=service, options=options)
print("[1/10] Opening OLX...")
driver.get("https://www.olx.ro/")
time.sleep(1)

# cookies
print("[2/10] Accepting Cookies...")
driver.find_element(By.ID, "onetrust-accept-btn-handler").click()

# search bar
print(f"[3/10] Searching for '{search_bar_input}'...")
search_bar = driver.find_element(By.ID, "search")
search_bar.clear()
search_bar.send_keys(search_bar_input + Keys.ENTER)
time.sleep(3)

# currency
print("[4/10] Setting currency to Euro...")
driver.find_element(By.CSS_SELECTOR, "[data-testid='currency-item']").click()
time.sleep(3)

# price range
print(f"[5/10] Setting price range (min: {money_min}, max: {money_max})...")
money_range_min = driver.find_element(By.NAME, "range-from-input")
money_range_min.clear()
money_range_min.send_keys(money_min + Keys.ENTER)
time.sleep(2)
money_range_max = driver.find_element(By.NAME, "range-to-input")
money_range_max.clear()
money_range_max.send_keys(money_max + Keys.ENTER)
time.sleep(2)

WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.css-1sw7q4x"))
)

# ad collecting
print("[6/10] Collecting all ad links...")
all_links = []
page = 1
while True:
    display_page = 7 + page / 10
    print(f"[{display_page:.1f}/9] Parsing page {page}...")
    soup = BeautifulSoup(driver.page_source, "html.parser")
    ads = soup.select("div.css-1sw7q4x a")
    for ad in ads:
        href = ad.get("href")
        if href:
            if href.startswith("/"):
                href = "https://www.olx.ro" + href
            all_links.append(href)
    try:
        next_page = driver.find_element(By.CSS_SELECTOR, "a[data-testid='pagination-forward']")
        next_url = next_page.get_attribute("href")
        if not next_url:
            break
        driver.get(next_url)
        time.sleep(3)
        page += 1
    except:
        break

# duplicates removal
final_links = list(dict.fromkeys(all_links))
print(f"[8/10] Found {len(final_links)} unique ads.")

# ----------------------
# Step 7: Fetch posted dates using Selenium
# ----------------------
def fetch_ad_date(link):
    ad_driver = webdriver.Chrome(service=service, options=options)
    try:
        ad_driver.get(link)
        try:
            date_elem = WebDriverWait(ad_driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='ad-posted-at']"))
            )
            posted_date = date_elem.text.strip()
        except:
            posted_date = "N/A"
    finally:
        ad_driver.quit()
    return {"link": link, "date": posted_date}

# fetching post data
print("[9/10] Fetching posted dates for all ads...")
ads_with_date = []
with ThreadPoolExecutor(max_workers=5) as executor:
    ads_with_date = list(executor.map(fetch_ad_date, final_links))

# ----------------------
# Step 8: Parse dates & sort
# ----------------------

for ad in ads_with_date:
    ad["parsed_date"] = dateparser.parse(ad["date"], languages=["ro"]) or dateparser.parse("1 Jan 1900")

ads_sorted = sorted(
    ads_with_date,
    key=lambda x: x["parsed_date"],
    reverse=True
)

# ----------------------
# Step 9: Print results
# ----------------------

print(f"[10/10] Done! Found {len(final_links)} unique ads sorted by newest date:")
for ad in ads_sorted:
    print(f"{ad['date']}: {ad['link']}")
>>>>>>> cb12965 (add olx scraper with CI workflow)
