import numpy as np
import scipy.sparse as sparse
import pandas as pd
import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('train_file', type=str)
    return parser.parse_args()

def main(args):
    df = pd.read_csv(args.train_file)
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
    user_item = item_user.T.tocsr()

    implicit_table = item_user.copy()
    implicit_table[implicit_table != 0] = 1
    pop_items = np.array(implicit_table.sum(axis=1)).reshape(-1)

    print('userid,foodid')
    for user in list(set(cols)):
        item_used = user_item[user].nonzero()[1].tolist()
        pred = pop_items.copy()
        pred[item_used] = -1
        item = (-pred).argsort()[:20]
        print('{},{}'.format(i2u[user], ' '.join([str(i2f[elem]) for elem in item])))

if __name__ == '__main__':
    main(get_args())
