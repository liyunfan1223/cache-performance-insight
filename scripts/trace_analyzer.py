from collections import defaultdict
from utils import TRACES_LIST

def run(access):
    mp = {}
    ats = {}
    ts = 0
    interval = 0
    ninterval = 0
    tot_freq = 0
    nHiF = 2048
    for i in access:
        ts += 1
        if i in mp.keys():
            mp[i] += 1
            interval += (ts - ats[i])
            ninterval += 1
            ats[i] = ts
        else:
            mp[i] = 1
            ats[i] = ts
    sort_result = sorted(mp.items(), key=lambda x: x[1], reverse=True)
    for idx, item in enumerate(sort_result):
        if (idx == nHiF):
            break
        tot_freq += item[1]
    avg_freq = len(access) / len(mp)
    avg_hiF = tot_freq / nHiF
    avg_interval = interval / ninterval

    print("average freq:", avg_freq)
    print(f"average high {nHiF} freq :", avg_hiF)
    print("average interval:", avg_interval)

def analyzer(trace_file):
    access = []
    with open(trace_file, "r") as f:
        for line in f.readlines():
            k, r, _, _ = line.strip().split()
            k = int(k)
            r = int(r)
            for i in range(k, k + r):
                access.append(i)
    run(access)

if __name__ == "__main__":
    for trace in TRACES_LIST:
        print(f"Analyzing {trace}:")
        analyzer(f"../traces/{trace}.lis")