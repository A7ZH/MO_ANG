import pandas as pd
import geopy as gp

pd.read_csv("YELP-Crawl-Run-2019-12-28T103701Z.csv", encoding='iso-8859-1') \
  .drop_duplicates() \
  .to_csv("YELP_Clean.csv")
