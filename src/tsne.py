import pandas as pd
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

df = pd.read_csv('data/food.csv')

interest_cols = ['foodid', 'calories', 'fat', 'carbs', 'sodium', 'potassium', 'fiber', 'sugar', 'protein', 'calcium', 'iron']
df = df[interest_cols]
for key in interest_cols[1:]:
    df[key] = pd.to_numeric(df[key], errors='coerce').fillna(0.0)

data = df.values[:, 1:]
data_max = data.max(axis=0)

# Hack about divided by zero
data_max[data_max == 0] = 1

# min max normalization
data = data/data_max

print(data.shape)

title = 'Food-nutrient t-SNE perlexity={perplexity} n_iter={n_iter}'

for perplexity in [5, 30 , 50]:
    for n_iter in [2500, 5000]:
        args = {
                'verbose': True, 
                'n_iter': n_iter,
                'perplexity': perplexity,
               }
        print(title.format(**args))

        data_embedded = TSNE(**args).fit_transform(data)
        plt.title(title.format(**args))
        plt.scatter(data_embedded[:,0], data_embedded[:, 1])
        plt.savefig('food-nutrient-p{perplexity}-n{n_iter}.png'.format(**args))
        plt.clf()
