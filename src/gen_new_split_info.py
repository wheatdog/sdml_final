from collections import OrderedDict
import argparse
import pickle
import pandas as pd

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--daily-seen', type=str, default='daily_seen.pkl')
    parser.add_argument('-n', '--novel-cnt', type=int, default=3)
    return parser.parse_args()

def main(args):
    with open(args.daily_seen, 'rb') as f:
        daily_seen = pickle.load(f)

    aggregate = {}
    for user, date_food in daily_seen.items():
        date_food = OrderedDict(date_food)

        date_range = list(date_food.keys())
        for idx in range(len(date_range)-1):
            prev_date = date_range[idx] 
            cur_date = date_range[idx+1]

            for food in date_food[prev_date]:
                if food not in date_food[cur_date]:
                    date_food[cur_date][food] = 0
                date_food[cur_date][food] += date_food[prev_date][food]
        aggregate[user] = date_food

    aggregate = OrderedDict(aggregate)
    seen_food_cnt = {}
    for user, date_food in aggregate.items():
        seen_food_cnt[user] = [len(food) for food in date_food.values()]

    for user, cnts in seen_food_cnt.items():
        total = cnts[-1]
        idx = len(cnts)-1
        for cnt in cnts[::-1]:
            if cnt + args.novel_cnt <= total:
                break
            idx -= 1

        assert(idx >= 0)
        print('{},{},foodid: [{}/{}] train_test_date: [{}/{}]'.format(
            user, list(aggregate[user].keys())[idx],
            cnts[idx], cnts[-1],
            idx+1, len(cnts)))

if __name__ == '__main__':
    main(get_args())
