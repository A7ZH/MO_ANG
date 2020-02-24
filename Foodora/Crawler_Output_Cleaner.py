import pandas as pd

facades=[]
names=[]
cuisines=[]
urls=[]
with open('Crawler_Output_Integrated.txt', 'r') as input_file: 
  line_iterator = iter(input_file)
  for triplet in zip(*[line_iterator for i in range(3)]):
    facade = triplet[0][:-1]
    facades += [facade]
    urls += [triplet[1][:-1]]
    names += [facade.split(';')[0]]
    cuisines += [facade.split('$;$;$;')[1].split(';')[0].replace(' & ', '&').replace(' ',';').replace('&', ' & ')]
df = pd.DataFrame({'Name':names, 'Cuisine':cuisines, 'URL':urls, 'Listing Info':facades},
                  columns=['Name','Cuisine','URL']) \
       .sort_values('Name') \
       .drop_duplicates() \
       .reset_index() \
       .drop(columns=['index'])
df.to_csv('Crawler_Output_Cleaned.csv', encoding='utf-8-sig', index=False)
