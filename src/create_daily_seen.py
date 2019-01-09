import argparse
import pickle
import pandas as pd

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('train_file', type=str)
    parser.add_argument('test_file', type=str)
    parser.add_argument('-o', '--output', type=str, default='daily_seen.pkl')
    return parser.parse_args()

def update_daily_seen(daily_seen, rating_file):
    df = pd.read_csv(rating_file)
    total_len = df.shape[0]
    for idx, row in df.iterrows():
        if row['userid'] not in daily_seen:
            daily_seen[row['userid']] = {}
        if row['date'] not in daily_seen[row['userid']]:
            daily_seen[row['userid']][row['date']] = {}
        if row['foodid'] not in daily_seen[row['userid']][row['date']]:
            daily_seen[row['userid']][row['date']][row['foodid']] = 0
        daily_seen[row['userid']][row['date']][row['foodid']] += 1
        if idx % 10000 == 0 or idx == total_len-1:
            print('{}: {}/{}'.format(rating_file, idx, total_len))

def main(args):
    daily_seen = {}
    update_daily_seen(daily_seen, args.train_file)
    update_daily_seen(daily_seen, args.test_file)

    with open(args.output, 'wb') as f:
        pickle.dump(daily_seen, f)

if __name__ == '__main__':
    main(get_args())
