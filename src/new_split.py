from collections import OrderedDict
import argparse
import pickle
import pandas as pd

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--split-info', type=str, default='new_split.csv')
    parser.add_argument('train_file', type=str)
    parser.add_argument('test_file', type=str)
    parser.add_argument('output_train', type=str)
    parser.add_argument('output_test', type=str)
    return parser.parse_args()

def get_end_of_traindate_per_user(filename):
    result = {}
    with open(filename) as f:
        for line in f:
            line = line.strip()
            elem = line.split(',')
            user, date = int(elem[0]), elem[1]
            result[user] = date
    return result

def main(args):
    traindate = get_end_of_traindate_per_user(args.split_info)

    df = [pd.read_csv(args.train_file), pd.read_csv(args.test_file)]
    df = pd.concat(df)
    
    with open(args.output_train, 'w') as new_train, open(args.output_test, 'w') as new_test:
        print('date,userid,foodid', file=new_train)
        print('date,userid,foodid', file=new_test)
        total_len = df.shape[0]
        for idx, row in df.iterrows():
            if row['date'] > traindate[row['userid']]:
                select_file = new_test
            else:
                select_file = new_train

            print('{},{},{}'.format(row['date'], row['userid'], row['foodid']), file=select_file)

            if idx % 10000 == 0 or idx == total_len-1:
                print('{}/{}'.format(idx, total_len))

if __name__ == '__main__':
    main(get_args())
