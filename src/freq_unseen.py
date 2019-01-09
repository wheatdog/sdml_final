from collections import OrderedDict
import sys

result = {}

with open(sys.argv[1]) as f:
    for line in f:
        line = line.strip()
        line = line.split(',')
        userid, unseen_cnt = line[0].strip(), int(line[1].strip())
        if unseen_cnt not in result:
            result[unseen_cnt] = 0
        result[unseen_cnt] += 1

a = OrderedDict(sorted(result.items()))
for k, v in a.items():
    print(k, v)
