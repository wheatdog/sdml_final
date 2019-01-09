import argparse
import pandas as pd
from tqdm import tqdm
from average_precision import mapk

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('train_file', type=str)
    parser.add_argument('test_file', type=str)
    parser.add_argument('predict_file', type=str)
    parser.add_argument('-m', '--max-count', type=int, default=20)
    return parser.parse_args()

def seen_food_in(filepath):
    df = pd.read_csv(filepath)

    seen = {}
    for idx, row in tqdm(df.iterrows(), unit='line', total=df.shape[0], postfix='reading {}'.format(filepath)):
        userid = row['userid']
        foodid = row['foodid']
        if userid not in seen:
            seen[userid] = set()
        seen[userid].add(foodid)
    return seen

def main(args):
    seen_train = seen_food_in(args.train_file)
    seen_test = seen_food_in(args.test_file)

    assert(set(seen_train.keys()) == set(seen_test.keys()))

    df = pd.read_csv(args.predict_file)

    actual = []
    predicted = []
    for idx, row in tqdm(df.iterrows(), unit='line', total=df.shape[0], postfix='processing {}'.format(args.predict_file)):
        userid = row['userid']
        foodids = [int(i) for i in row['foodid'].split()]
        unseen_foods = seen_test[userid] - seen_train[userid]

        predicted.append(foodids)
        actual.append(list(unseen_foods))

    print(mapk(actual, predicted, k=20))

if __name__ == '__main__':
    main(get_args())

