import json
import argparse
import pandas as pd

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--rating-file', type=str, default='data/rating_train.csv')
    parser.add_argument('-f', '--food-file', type=str, default='data/food.csv')
    parser.add_argument('label_file', type=str)
    return parser.parse_args()

def get_name2id_map(filename):
    mapping = {}
    with open(filename) as f:
        for line in f:
            line = line.strip()
            line = line.split(',')
            mapping[line[1]] = line[0]

    return mapping

def get_id2ids_map(n2id, food_file):
    mapping = {}

    df = pd.read_csv(food_file)
    df = df[['foodid', 'annotated_food_name']]

    for _, row in df.iterrows():
        name_dict = json.loads(row['annotated_food_name'])
        id_list = []
        # foodid 39
        if len(name_dict.keys()) == 0:
            id_list.append(len(n2id))
        for s in name_dict.keys():
            if s in n2id:
                id_list.append(n2id[s])
        mapping[row['foodid']] = sorted(id_list)

    return mapping

def get_rating_list(filename):
    rating = []
    with open(filename) as f:
        f.readline()
        for line in f:
            line = line.strip()
            line = line.split(',')
            rating.append({'date': line[0], 'user': int(line[1]), 'food': int(line[2])})
    return rating


def main(args):
    n2id = get_name2id_map(args.label_file)
    i2is = get_id2ids_map(n2id, args.food_file)
    rating = get_rating_list(args.rating_file)


    print('date,userid,foodid')
    for line in rating:
        date, user, food = line['date'], line['user'], line['food']
        new_ids = i2is[food]
        for idx in new_ids:
            print(','.join([str(elem) for elem in [date, user, idx]]))


if __name__ == '__main__':
    main(get_args())
