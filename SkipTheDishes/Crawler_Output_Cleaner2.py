import pandas as pd
df=pd.read_csv('Crawler_Output_Cleaned.csv', encoding='utf-8-sig')
with open('coordinates_cuisines.txt', 'r') as input_file:
  coordinates=[]
  cuisines=[]
  for i in iter(input_file):
    coordinates += [i.split('|')[0].rstrip().lstrip()]
    cui = i.split('|')[1].rstrip().lstrip()
    cui = "Unspecified" if cui=='' else cui
    cuisines += [cui]
df['Coordinate'] = pd.DataFrame({'Coordinate' : coordinates})
df['Cuisine'] = pd.DataFrame({'Cuisine' : cuisines})
for ind, row in df.iterrows():
  if(row['Cuisine']=='Unspecified' or row['Cuisine']=='Restaurants'):
    if(ind>0 and row['Name']==df['Name'][ind-1] and row['Cuisine']!=df['Cuisine'][ind-1]):
      row['Cuisine'] = df['Cuisine'][ind-1]
    elif (ind<len(df)-1 and row['Name']==df['Name'][ind+1] and row['Cuisine']!=df['Cuisine'][ind+1]):
      row['Cuisine'] = df['Cuisine'][ind+1]
df[['Name', 'Cuisine', 'Coordinate']].to_csv('SkipTheDishes_Clean.csv', encoding='utf-8-sig', index=False)
