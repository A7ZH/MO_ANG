import pandas as pd

facades=[]
names=[]
cuisines=[]
urls=[]
with open('Crawler_Output_Integrated.txt', 'r') as input_file: 
  line_iterator = iter(input_file)
  for triplet in zip(*[line_iterator for i in range(3)]):
    facade = triplet[0][:-1]
    url = triplet[1][:-1]
    name_maybe = facade.split(';$')[0]
    name = name_maybe.split(';')[1] if(";" in name_maybe) else name_maybe
    cuisine_maybe = facade.split('$•;')[1].split(';')[0]
    cuisine = 'Unspecified' if(cuisine_maybe=='Closed' or cuisine_maybe=='Restaurants') \
                            else cuisine_maybe.replace(',', ';') \
                                              .replace('Restaurants;', '') \
                                              .replace('; Restaurants', '') \
                                              .replace('Good for Groups;', '') \
                                              .replace('; Good for Groups', '')
    facades += [facade]
    urls += [url]
    names += [name]
    cuisines += [cuisine]
df = pd.DataFrame({'Name':names, 'Cuisine':cuisines, 'URL':urls, 'Listing Info':facades},
                  columns=['Name','Cuisine','URL']) \
       .sort_values('Name') \
       .drop_duplicates(subset='URL') \
       .reset_index() \
       .drop(columns=['index'])
for ind, row in df.iterrows():
  if(row['Cuisine']=='Unspecified' or row['Cuisine']=='Restaurants'):
    if(ind>0 and row['Name']==df['Name'][ind-1] and row['Cuisine']!=df['Cuisine'][ind-1]):
      row['Cuisine'] = df['Cuisine'][ind-1]
    elif (ind<len(df)-1 and row['Name']==df['Name'][ind+1] and row['Cuisine']!=df['Cuisine'][ind+1]):
      row['Cuisine'] = df['Cuisine'][ind+1]
df.to_csv('Crawler_Output_Cleaned.csv', encoding='utf-8-sig', index=False)
