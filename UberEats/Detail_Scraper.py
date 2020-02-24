import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

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
print("==========" + str(time.time())+"========", file=output)
error = open('coordinates_error_url.txt', 'a')
print("==========" + str(time.time())+"========", file=error)
for url in df['URL']:
  driver.get(url)
  print(url)
  try:
    WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.LINK_TEXT, "More info"))).click()
    coord = WebDriverWait(driver,30).until(EC.visibility_of_element_located((By.XPATH, 
                                            "//div[@role='dialog']/figure/img"))) \
                                    .get_attribute('src') \
                                    .split('center=')[1] \
                                    .split('&zoom')[0] \
                                    .split('%2C')
    coord = (float(coord[0]), float(coord[1]))
    print(coord)
    print(coord, file=output)
  except:
    print(None)
    print(None, file=output)
    print(url, file=error)
  driver.delete_all_cookies()
driver.close()
output.close()
error.close()
