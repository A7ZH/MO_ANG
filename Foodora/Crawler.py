from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Load and clean up locations, each being the representing address of a neighbourhood in Totonto.
#   Prob1: What's the minumally necessary encoding needed for data in location.csv?
#   Prob2: "Hood #" column is unecessary; removed.
#   Prob3: "Unamed: 3" column is unecessary; removed.
#   Prob4: Entries "Maple Leaf" & "Rouge" miss addresses; removed / manually fill in.
#   Prob5: Entries contain address components that are invalid to Foodora address search, e.g. Unit #
#          use err_ind=df.index[df['Repr Addr'].str.contains('error string')][0] to find the index.
#          use df['Repr Addr'][err_ind]=df['Repr Addr'][err_ind][:x]+df['Repr Addr'][err_ind][y:] to modify.
df=pd.read_csv('locations.csv', encoding='iso-8859-1').drop(columns=['Hood #'])
df=df.loc[:, ~df.columns.str.contains('^Unnamed')]
df=df.drop(df.index[df['Repr Addr'].isna()]).reset_index().drop(columns=['index'])

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

# Log the neighourhoods not serviced by Foodora; can be used for visualization.
unserviced_locations = open("unserviced_locations.txt", 'a')

for addr in df['Repr Addr'][5:]:
  print(addr)
  # Create output file with the name being the Hood Name. 
  filename = "Crawler_Output/" + df['Hood Name'][df.index[df['Repr Addr']==addr].values[0]]
  output = open(filename,'w+')
  # Navigate to "www.foodora.ca".
  driver.get("https://www.foodora.ca")
  # Wait for the address search bar to become clickable, and click it. 
  search_bar=WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH,
      "//input[@class='restaurants-search-form__input restaurants__location__input ']")))
  # Type in target address into the search bar. Sometimes the input get truncated or cleared
  #   as the webpage refreshes itself while loading, thus we make 3 attempts to type in the 
  #   target address, interleaving with 1 second of wait time.
  for i in range(3):
    search_bar.click()
    if(search_bar.get_attribute('value')==addr): pass
    else:
      while(search_bar.get_attribute('value')!=''): 
        search_bar.send_keys(Keys.ALT + Keys.RIGHT)
        search_bar.send_keys(Keys.BACKSPACE)
      search_bar.send_keys(addr) 
  # Press the "Delivery" button to jump to the listing page.
  search_bar.find_element_by_xpath("ancestor::form/descendant::button[1]").click()
  try:
    # Many neighbourhood representing addresses produce no listing results, which will be logged.
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH,
                                   "//div[@class='restaurants__not-available-message " \
                                   "restaurants__no-result-message vendor-list-empty-message']")))
    print(df['Hood Name'][df.index[df['Repr Addr']==addr][0]] + " ; " + addr, file=unserviced_locations)
    print("UNSERVICED")
  except:
    # Wait for all the listing figures in the page to become visible.
    figures = WebDriverWait(driver, 180).until(EC.presence_of_all_elements_located((By.XPATH, 
                                               "//div[@class='restaurants__list']/descendant::figure")))
    # For each figure, scrape its corresponding listing's text information and link for details page
    for f in figures:
      info1 = f.text.replace('\n', ';')
      info2 = f.find_element_by_xpath("parent::a").get_attribute('href')
      print(info1 + '\n' + info2 + '\n', file=output)
      print(info1 + '\n' + info2 + '\n')
  output.close()
  driver.delete_all_cookies()
driver.close()
