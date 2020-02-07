import pandas as pd
from geopy import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.exc import GeocoderTimedOut

########################## PREPARING DATA IN DATAFRAME #########################################
df = pd.read_csv("YELP-Crawl-Run-2019-12-28T103701Z.csv", encoding='iso-8859-1') \
       .drop_duplicates()     # Remove duplicate entries
df = df.drop(df.index[554]) \  # Duplicate of entry 254, cuisine written in different order
       .reset_index() \        
       .drop(columns=['index']) \
       .to_csv("YELP_Clean.csv", index=False)
df_size = df.shape[0] 

########################### AD-HOC DATA CLEANING ################################################
# Remove the prefix "Located in " contained by some addresses
df['Address'] = df['Address'].apply(lambda addr: addr[11:] if addr.startswith("Located in ") else addr)
# Remove the unit number for entry 245
df['Address'] = df['Address'][245][3:]
# Replace "Double Tree by Hiton Hotel Downtown Toronto" with "108 Chestnut Street" for entry 312
df['Address'][312] = "108 Chestnut Street"
# Add the "St" suffix to "25 Lower Simcoe" for entry 327
df['Address'][327] = df['Address'][327] + " St" 
# Remove the unit number for entry 339
df['Address'][339] = df['Address'][339][8:]
# Add ", ON, Canada" to each address to support geo-coding
addresses = df['Address'].apply(lambda addr: addr + ", ON, Canada").values.tolist()

########################### GEO-CODING ADDRESS DATA #############################################
geocoder = Nominatim(user_agent='myGeocoder').geocode
delay = 1
# The delay between each calling of geocode is to prevent the denial of access to Nominatim
while True:
  try:
    geocode = RateLimiter(geocoder, min_delay_seconds=delay)
    locations0 = [geocode(addr) for addr in addresses[0  :100]]
    break
  except GeocoderTimedOut:
    sleep(30)
    delay += 1

locations1 = [geocode(addr) for addr in addresses[100:200]]
# Increase delay to 3 seconds per call 
geocode = RateLimiter(geocoder, min_delay_seconds=3)
locations2 = [geocode(addr) for addr in addresses[200:300]]
# Reduce delay back to 1 second per call
geocode = RateLimiter(geocoder, min_delay_seconds=1)
locations3 = [geocode(addr) for addr in addresses[300:400]]
locations4 = [geocode(addr) for addr in addresses[400:500]]
locations5 = [geocode(addr) for addr in addresses[500:600]]
# Increase delay to 3 seconds per call again
geocode = RateLimiter(geocoder, min_delay_seconds=4)
locations6 = [geocode(addr) for addr in addresses[600:df_size]]

########################### INTEGRATING COORDINATES DATA INTO DATAFRAME #########################
locations = locations0 + locations1 + locations2 + locations3 + locations4 + locations5 + locations6
df["Address(Full)"] = [loc.address for loc in locations]
df["Coordinate"] = [(loc.latitude, loc.longitude) for loc in locations]
col_order = ["Name", "Cuisine", "Coordiante", "Address", "Address(Full)"]
df = df[col]
df.to_csv("YELP_Final.csv", index=False)

