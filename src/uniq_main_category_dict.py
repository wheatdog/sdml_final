import json
import pandas as pd

df = pd.read_csv('data/food.csv')

collect = set()

for _, row in df[['foodid', 'annotated_food_name']].iterrows():
    name_dict = json.loads(row['annotated_food_name'])
    # foodid 39
    if len(name_dict.keys()) == 0:
        continue
    found = False
    for s in name_dict.keys():
        if len(s.split('__')) == 1:
            collect.add(s)
            found = True
    if not found:
        print('ERROR: {}'.format(row['foodid']))

collect = sorted(list(collect))
for idx, elem in enumerate(collect):
    print('{},{}'.format(idx,elem))
