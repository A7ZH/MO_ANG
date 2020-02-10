import pandas as pd
df = pd.read_csv('UberEats_Clean.csv', encoding='utf-8-sig')
cuisines = []
for c in df['Cuisine']:
  cuisines += c.split(';')

cuisine_df = pd.DataFrame({'Cuisine':cuisines}, columns=['Cuisine']) \
               .sort_values('Cuisine') \
               .drop_duplicates() \
               .reset_index() \
               .drop(columns=['index'])

output = open('Cuisine_List.txt', 'w+')
for c in cuisine_df['Cuisine']:
  print(c, file=output)

