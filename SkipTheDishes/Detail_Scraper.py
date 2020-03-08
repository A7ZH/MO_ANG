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
output = open('coordinates_cuisines.txt', 'a')
for url in df['URL']:
  driver.get(url)
  print("WORKING ON: " + url)
  try:
    time.sleep(2)
    # WebDriverWait(driver, 15).until(lambda x: x.execute_script('return document.readyState')=='complete')
    WebDriverWait(driver, 30).until(lambda driver: eval(str(eval(driver.find_element_by_xpath(
         "//script[@type='application/ld+json']").get_attribute('innerHTML'))['geo']))['latitude']!=0)
    info = eval(driver.find_element_by_xpath("//script[@type='application/ld+json']") 
                      .get_attribute('innerHTML'))
    coord = (float(eval(str(info['geo']))['latitude']), float(eval(str(info['geo']))['longitude']))
    cui = info['servesCuisine'].replace(',', ';')
    print(coord, cui, sep=' | ')
    print(coord, cui, url, sep=' | ', file=output)
  except:
    print(None, None, sep='|')
    print(None, None, url, sep='|', file=output)
  driver.delete_all_cookies()
driver.close()
output.close()
