import pandas as pd
facades=[]
names=[]
urls=[]
with open('Crawler_Output_Integrated.txt', 'r') as input_file: 
  line_iterator = iter(input_file)
  for triplet in zip(*[line_iterator for i in range(3)]):
    facade = triplet[0][:-1]
    url = triplet[1][:-1]
    name = facade.split(';')[0]
    facades += [facade]
    urls += [url]
    names += [name]
df = pd.DataFrame({'Name':names, 'URL':urls, 'Listing Info':facades}, columns=['Name','Cuisine','URL']) \
       .sort_values('Name') \
       .drop_duplicates(subset='URL') \
       .reset_index() \
       .drop(columns=['index']) \
       .to_csv('Crawler_Output_Cleaned.csv', encoding='utf-8-sig', index=False)
