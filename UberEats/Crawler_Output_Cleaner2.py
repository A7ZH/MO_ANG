import pandas as pd
df=pd.read_csv('Crawler_Output_Cleaned.csv', encoding='utf-8-sig')
df['Coordinate'] = [c.rstrip('\n') for c in open('coordinates.txt','r').readlines()]
df = df[['Name', 'Cuisine', 'Coordinate']]
#df = df.drop(df.index[df['Coordinate']=='None']) # Manually filled in missing coordinates
df.to_csv('UberEats_Clean.csv', encoding='utf-8-sig', index=False)
