from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import dateparser

# Setup Chrome
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

# Configure search
search_bar_input = "Kawasaki Z750"
money_min = "3500"
money_max = "4200"

print("[1/9] Opening OLX...")
driver.get("https://www.olx.ro/")
time.sleep(1)

# Accept Cookies
print("[2/9] Accepting Cookies...")
try:
    accept_cookies = driver.find_element(By.ID, "onetrust-accept-btn-handler")
    accept_cookies.click()
    time.sleep(1)
except:
    print("   -> No cookie popup found.")

# Search for an item
print(f"[3/9] Searching for {search_bar_input}...")
search_bar = driver.find_element(By.ID, "search")
search_bar.clear()
search_bar.send_keys(search_bar_input + Keys.ENTER)
time.sleep(2)

# Set Currency
print("[4/9] Setting currency to euro...")
try:
    currency_select = driver.find_element(By.CSS_SELECTOR, "[data-testid='currency-item']")
    currency_select.click()
    time.sleep(2)
except:
    print("   -> Currency selector not found, continuing...")

# Set price range
print(f"[5/9] Setting price range (min: {money_min}, max: {money_max})...")
money_range_min = driver.find_element(By.NAME, "range-from-input")
money_range_min.clear()
money_range_min.send_keys(money_min + Keys.ENTER)
time.sleep(2)

money_range_max = driver.find_element(By.NAME, "range-to-input")
money_range_max.clear()
money_range_max.send_keys(money_max + Keys.ENTER)
time.sleep(2)

# Wait for ads
WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.css-1sw7q4x"))
)

# Collect ads across pages
print("[6/9] Collecting all ad links...")
all_links = []
page = 1

while True:
    display_page = 8 + page / 10
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
        time.sleep(2)
        page += 1
    except:
        break

# Remove duplicates
final_links = list(dict.fromkeys(all_links))

# Extract details
ads_with_date = []
for i, link in enumerate(final_links, 1):
    print(f"   -> Opening ad {i}/{len(final_links)}...")
    driver.get(link)

    # Posted date
    try:
        date_elem = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='ad-posted-at']"))
        )
        posted_date = date_elem.text.strip()
    except:
        posted_date = "N/A"

    ads_with_date.append({
        "link": link,
        "date": posted_date
    })

# Parse and sort by date
for ad in ads_with_date:
    ad["parsed_date"] = dateparser.parse(ad["date"], languages=["ro"]) or dateparser.parse("1 Jan 1900")

ads_sorted = sorted(
    ads_with_date,
    key=lambda x: x["parsed_date"],
    reverse=True
)

print(f"[9/9] Done! Found {len(final_links)} unique ads sorted by date:\n")
for ad in ads_sorted:
    print(f"{ad['date']}: {ad['link']}")

driver.quit()
