from selenium import webdriver
from gmapScrp import scrapData
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Generate hex area
hex_ids = ["8838412f3dfffff"]
op = Options()
#op.add_argument('--headless')
# Setup Selenium
driver = webdriver.Chrome(options=op)
driver.get("https://www.google.com/maps")

# Start scraping only within allowed H3 hexagons
results = scrapData(driver,"Food","Sfax",hex_ids)
print(results)