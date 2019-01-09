import argparse
import pandas as pd

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('train_rating', type=str)
    parser.add_argument('test_rating', type=str)
    return parser.parse_args()

def group_food_with_user(rating):
    df = pd.read_csv(rating)
    seen_food = {}
    for userid in df.userid.unique():
        food = set(df.loc[df['userid'] == userid].foodid.unique())
        seen_food[userid] = food
    return seen_food

def main(args):
    seen_food = group_food_with_user(args.train_rating)
    test_food = group_food_with_user(args.test_rating)

    for userid, food in test_food.items():
        if userid not in seen_food:
            print('userid {userid} is not in file {train_file}, which is very strange!!'.format(userid=userid,train_file=args.train_rating))
            exit(1)
        unseen_food = food - seen_food[userid]
        print('{}, {}, {}'.format(userid, len(unseen_food), list(unseen_food)))

if __name__ == '__main__':
    main(get_args())
