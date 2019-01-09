import argparse
import pandas as pd
from tqdm import tqdm

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

    user_cnt = 0
    mean_ap = 0
    for idx, row in tqdm(df.iterrows(), unit='line', total=df.shape[0], postfix='processing {}'.format(args.predict_file)):
        userid = row['userid']
        foodids = [int(i) for i in row['foodid'].split()]
        if len(foodids) > args.max_count:
            foodids = foodids[:args.max_count]

        # make sure uniqueness of predictions
        assert(len(foodids) == len(set(foodids)))

        unseen_foods = seen_test[userid] - seen_train[userid]

        ap = 0
        hit = 0
        for c, food in enumerate(foodids):
            if food in unseen_foods:
                hit += 1
                ap += hit/(c+1)
        ap /= min(len(unseen_foods), args.max_count)
        mean_ap += ap
        user_cnt += 1
    mean_ap /= user_cnt
    print(mean_ap)


if __name__ == '__main__':
    main(get_args())
