from collections import defaultdict
from utils import TRACES_LIST

def run(access):
    mp = {}
    ats = {}
    ts = 0
    interval = 0
    ninterval = 0
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
    avg_freq = len(access) / len(mp)
    avg_interval = interval / ninterval
    print("average freq:", avg_freq)
    print("average interval:", avg_interval)

def analyzer(trace_file):
    # trace_file = "../traces/P5.lis"
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
        print(f"Analyze {trace}:")
        analyzer(f"../traces/{trace}.lis")