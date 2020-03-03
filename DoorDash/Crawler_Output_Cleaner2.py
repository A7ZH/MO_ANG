import pandas as pd
df=pd.read_csv('Crawler_Output_Cleaned.csv', encoding='utf-8-sig')
df['Coordinate'] = [c.rstrip('\n').split(' | ')[0] if (not 'None' in c) else 'None' for c in open('coordinates.txt','r').readlines()]
df = df[['Name', 'Cuisine', 'Coordinate']]
df = df.drop(df.index[df['Coordinate']=='None']) \
       .reset_index() \
       .drop(columns=['index'])
df.to_csv('DoorDash_Clean.csv', encoding='utf-8-sig', index=False)
