import numpy as np
import scipy.sparse as sparse
import pandas as pd
import random

from sklearn import metrics

def make_train(rating, percent=0.2):
    test_set = rating.copy()
    test_set[test_set != 0] = 1
    training_set = rating.copy()
    nonzeros = training_set.nonzero()
    nonzeros = list(zip(nonzeros[0], nonzeros[1]))
    num_samples = int(np.ceil(percent*len(nonzeros)))
    samples = random.sample(nonzeros, num_samples)
    ids = list(zip(*samples))
    training_set[ids[0], ids[1]] = 0
    training_set.eliminate_zeros()

    return training_set, test_set, list(set(ids[1]))

def main():
    random.seed(0)

    df = pd.read_csv('data/rating_train.csv')
    df['cnt'] = 1
    df = df[['userid', 'foodid', 'cnt']]
    df = df.groupby(['userid', 'foodid']).sum().reset_index()

    foods = list(np.sort(df.foodid.unique()))
    users = list(np.sort(df.userid.unique()))

    type_user = pd.api.types.CategoricalDtype(users, ordered=True)
    type_food = pd.api.types.CategoricalDtype(foods, ordered=True)

    i2u = dict(enumerate(df.userid.astype(type_user).cat.categories))
    i2f = dict(enumerate(df.foodid.astype(type_food).cat.categories))

    rows = df.foodid.astype(type_food).cat.codes
    cols = df.userid.astype(type_user).cat.codes

    item_user = sparse.csr_matrix((list(df.cnt), (rows, cols)), shape=(len(foods), len(users)))

    training_set, test_set, user_alter = make_train(item_user)

    user_item = item_user.T.tocsr()

    pop_items = np.array(test_set.sum(axis=1)).reshape(-1)
    np.savetxt('t.npy', pop_items)
    with open('result.csv', 'w') as f:
        print('userid,foodid', file=f)
        for user in list(set(cols)):
            item_used = user_item[user].nonzero()[1].tolist()
            pred = pop_items.copy()
            pred[item_used] = -1
            item = (-pred).argsort()[:20]
            print('{},{}'.format(i2u[user], ' '.join([str(i2f[elem]) for elem in item])), file=f)

if __name__ == '__main__':
    main()

