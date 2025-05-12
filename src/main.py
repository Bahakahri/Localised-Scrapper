from selenium import webdriver
from gmapScrp import scrapData
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd

# Hexes IDs

hex_ids = ["88384c5817fffff","88384c581bfffff","88384c5811fffff","88384c5815fffff","88384c5819fffff","88384c581dfffff","88384c583bfffff","88384c58e7fffff","88384c58e3fffff","88384c58adfffff","88384c58a1fffff","88384c58a9fffff","88384c58e5fffff","88384c58ebfffff","88384c58e9fffff","88384c58edfffff","88384c5813fffff","88384c58e1fffff","88384c5833fffff","88384c59d1fffff","88384c59d9fffff","88384c588dfffff","88384c59dbfffff"]
op = Options()
op.add_argument('--headless')
driver = webdriver.Chrome(options=op)
driver.get("https://www.google.com/maps")

# Start scraping only within allowed H3 hexagons
results = scrapData(driver,"Food","Sfax",hex_ids)
df = pd.DataFrame(results)
df.to_csv(r'C:\Users\Mega Pc\Localised Scrapper\data\SfaxPrio1.csv')
print(results)