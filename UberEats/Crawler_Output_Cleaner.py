import pandas as pd

def N_lines_at_a_time(all_lines, N=1):
  # Create a iterator pointing to the all_lines data in memory, line_iterator is a reference to the iterator
  #   object.
  line_iterator = iter(all_lines) 
  # [line_iterator for i in range(N)] creates N references of the same iterator object above - when next() 
  #   is invoked upon any of the N references, the "next pointer" of the very same iterator object pointing 
  #   to the data moves ahead one step - to be stored in a list.
  # *[line_iterator for i in range(N)] unpacks the list, exposing N references of the same iterator object 
  #  to the zip function.
  # zip function takes the N references of the same iterator to store them in a zip object, which itself is
  #   an iterator object that next() can be called upon.
  # When zip() zips iterables, e.g. zip([1,2], ["one", "two"]), zip object has one inner iterator per zipped 
  #   iterable, such that when next() is called upon the zip object, next() is called upon each inner 
  #   iterator. i.e. >>> a = zip([1,2], ["one", "two"])
  #                  >>> next(a)
  #                      (1, "one")
  # When zip() zips iterators, such as above, the zip object's inner iterators become the zipped iterators, 
  #   such that when next() is called upon the zip object, next() is called upon each zipped iterator. 
  return zip(*[line_iterator for i in range(N)]) 

facades=[]
names=[]
cuisines=[]
urls=[]
with open('Crawler_Output_Integrated.txt', 'r') as input_file: 
  for triplet in N_lines_at_a_time(input_file, N=3):
    # Output Test: 1. print(*triplet, sep='') 2. print(triplet[0], triplet[1], sep='')
    #              3. print(triplet[1])       4. print(triplet[1][:-1])
    facade = triplet[0][:-1]
    facades += [triplet[0][:-1]]
    urls += [triplet[1][:-1].split('?promo')[0]]
    names += [facade.split('•')[0].split(';')[-2]]
    cuisines += [','.join([c.lstrip().rstrip() for c in facade.split('•')[1:]])
                   .split(';')[0]
                   .replace(',', ';')]
data = {'Name':names, 'Cuisine':cuisines, 'URL':urls, 'Listing Info':facades} 
df = pd.DataFrame(data, columns=['Name','Cuisine','URL']) \
       .sort_values('Name') \
       .drop_duplicates() \
       .reset_index() \
       .drop(columns=['index'])
df.to_csv('Crawler_Output_Cleaned.csv', encoding='utf-8-sig', index=False)
