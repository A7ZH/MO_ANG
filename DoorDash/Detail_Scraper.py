import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load data. 
df = pd.read_csv('Crawler_Output_Cleaned.csv', encoding='utf-8-sig')

# Add options for the Chrome browser.
options=webdriver.ChromeOptions()
options.binary_location='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
options.add_argument('--headless')
options.add_argument('--window-size=1920,1080')
options.add_argument('--diable-extensions')
options.add_argument('--diable-gpu')
options.add_argument('--incognito')
# Run the Chrome browser.
driver=webdriver.Chrome(chrome_options=options)

output = open('coordinates.txt', 'a')
for url in df['URL']:
  driver.get(url)
  print(url)
  try:
    addr = WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH, 
        "//*[contains(text(), 'Delivered from')]/following-sibling::span[3]"))).text
    driver.get("https://www.google.ca/maps")
    search_bar = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.XPATH,
        "//input[@aria-label='Search Google Maps']"))) 
    search_bar.send_keys(addr + Keys.RETURN)
    WebDriverWait(driver, 30).until(EC.url_changes("https://www.google.ca/maps"))
    coord = driver.current_url.split('/@')[1].split('z/')[0].split(',')
    coord = (float(coord[0]), float(coord[1]))
    print(coord, addr, sep=' | ')
    print(coord, addr, url, sep=' | ', file=output)
  except:
    print(None, addr, sep='|')
    print(None, addr, url, sep='|', file=output)
  driver.delete_all_cookies()
driver.close()
output.close()
error.close()
