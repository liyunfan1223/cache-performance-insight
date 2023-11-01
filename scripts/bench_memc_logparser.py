example_logs = [
    "Time: 1698399081.281695 Args: threads-64 value_size-1024 memcached_mem-39 trace-webmail memc_suffix-rgc earle_stop-False threads_sync-True has_warmup-False est_item_counts-48866.700000000004",
    "runtime: 39.67s warming up: 0 average latency: 0.3256 mem: 0.1870 rdb: 0.6529 nf: 0.0000 tps: 196196.49 tps_mb: 143.70 tps_mem: 100.97 tps_rdb: 42.73 h_ratio: 70.26% t_counter: 7783160 mem:rdb:nf=5468674:2314486:0",
    "Size:39, P_size:0.1, Ideal Hit Rate:73.7223"
]

def parse(logs):
    mem = int(logs[0].split(' ')[5][14:])
    psize = float(logs[2].split(' ')[1][7:-1])
    if mem < 3:
        return 0, 0
    if psize != 0.1:
        return 0, 0
    cur = logs[1].split(' ')
    sys_hr = float(cur[23][:-1])
    ideal_hr = float(logs[2].split(' ')[4][5:])
    return ideal_hr, sys_hr


if __name__ == "__main__":
    f = open('local/log1027.txt')
    logs = []
    cur_log = []
    for idx, line in enumerate(f.readlines()):
        cur_log.append(line.strip())
        if idx % 3 == 2:
            logs.append(cur_log)
            cur_log = []

    sum = 0
    count = 0

    for log in logs:
        i, s = parse(log)
        if s == 0:
            continue
        sum += i / s - 1
        # sum += (100 - s) / (100 - i) - 1
        count += 1

    print(sum / count * 100, count)