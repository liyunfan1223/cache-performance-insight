example = """memcached_mem-64 memc_suffix-lru threads-16 server_thread-2
Type         Ops/sec     Hits/sec   Misses/sec    Avg. Latency     p50 Latency     p99 Latency   p99.9 Latency       KB/sec
----------------------------------------------------------------------------------------------------------------------------
Sets        85876.33          ---          ---         0.09259         0.07900         0.19900         0.31100     89636.02
Gets        85876.33     72809.28     13067.05         0.09193         0.07900         0.19900         0.30300      3088.75
Waits           0.00          ---          ---             ---             ---             ---             ---          ---
Totals     171752.67     72809.28     13067.05         0.09226         0.07900         0.19900         0.31100     92724.77

memcached_mem-64 memc_suffix-rgc threads-16 server_thread-2
Type         Ops/sec     Hits/sec   Misses/sec    Avg. Latency     p50 Latency     p99 Latency   p99.9 Latency       KB/sec
----------------------------------------------------------------------------------------------------------------------------
Sets        79453.46          ---          ---         0.10023         0.08700         0.21500         0.32700     82931.95
Gets        79453.46     67374.48     12078.98         0.10006         0.08700         0.21500         0.31900      2857.73
Waits           0.00          ---          ---             ---             ---             ---             ---          ---
Totals     158906.92     67374.48     12078.98         0.10015         0.08700         0.21500         0.31900     85789.68

memcached_mem-64 memc_suffix-lru threads-16 server_thread-4
Type         Ops/sec     Hits/sec   Misses/sec    Avg. Latency     p50 Latency     p99 Latency   p99.9 Latency       KB/sec
----------------------------------------------------------------------------------------------------------------------------
Sets       162972.37          ---          ---         0.04963         0.04700         0.15900         0.58300    170107.33
Gets       162972.37    138160.64     24811.73         0.04836         0.04700         0.15900         0.59100      5861.69
Waits           0.00          ---          ---             ---             ---             ---             ---          ---
Totals     325944.73    138160.64     24811.73         0.04899         0.04700         0.15900         0.58300    175969.03

memcached_mem-64 memc_suffix-rgc threads-16 server_thread-4
Type         Ops/sec     Hits/sec   Misses/sec    Avg. Latency     p50 Latency     p99 Latency   p99.9 Latency       KB/sec
----------------------------------------------------------------------------------------------------------------------------
Sets       140842.08          ---          ---         0.05705         0.05500         0.12700         0.27900    147008.18
Gets       140842.08    119443.30     21398.78         0.05611         0.05500         0.11900         0.27100      5065.72
Waits           0.00          ---          ---             ---             ---             ---             ---          ---
Totals     281684.16    119443.30     21398.78         0.05658         0.05500         0.11900         0.27900    152073.90

memcached_mem-64 memc_suffix-lru threads-16 server_thread-6
Type         Ops/sec     Hits/sec   Misses/sec    Avg. Latency     p50 Latency     p99 Latency   p99.9 Latency       KB/sec
----------------------------------------------------------------------------------------------------------------------------
Sets       197565.08          ---          ---         0.04125         0.03900         0.14300         0.35100    206214.52
Gets       197565.08    167523.33     30041.75         0.03954         0.03900         0.13500         0.33500      7105.90
Waits           0.00          ---          ---             ---             ---             ---             ---          ---
Totals     395130.15    167523.33     30041.75         0.04040         0.03900         0.14300         0.34300    213320.42

memcached_mem-64 memc_suffix-rgc threads-16 server_thread-6
Type         Ops/sec     Hits/sec   Misses/sec    Avg. Latency     p50 Latency     p99 Latency   p99.9 Latency       KB/sec
----------------------------------------------------------------------------------------------------------------------------
Sets       168579.48          ---          ---         0.04765         0.04700         0.13500         0.28700    175959.93
Gets       168579.48    142968.68     25610.81         0.04596         0.04700         0.12700         0.27100      6063.37
Waits           0.00          ---          ---             ---             ---             ---             ---          ---
Totals     337158.96    142968.68     25610.81         0.04681         0.04700         0.13500         0.27900    182023.30

memcached_mem-64 memc_suffix-lru threads-16 server_thread-8
Type         Ops/sec     Hits/sec   Misses/sec    Avg. Latency     p50 Latency     p99 Latency   p99.9 Latency       KB/sec
----------------------------------------------------------------------------------------------------------------------------
Sets       207746.07          ---          ---         0.03932         0.03900         0.11100         0.23900    216841.24
Gets       207746.07    176097.60     31648.47         0.03754         0.03900         0.10300         0.22300      7472.09
Waits           0.00          ---          ---             ---             ---             ---             ---          ---
Totals     415492.14    176097.60     31648.47         0.03843         0.03900         0.11100         0.23100    224313.33

memcached_mem-64 memc_suffix-rgc threads-16 server_thread-8
Type         Ops/sec     Hits/sec   Misses/sec    Avg. Latency     p50 Latency     p99 Latency   p99.9 Latency       KB/sec
----------------------------------------------------------------------------------------------------------------------------
Sets       180898.19          ---          ---         0.04535         0.04700         0.12700         0.25500    188817.96
Gets       180898.19    153422.62     27475.57         0.04317         0.03900         0.11900         0.23100      6506.44
Waits           0.00          ---          ---             ---             ---             ---             ---          ---
Totals     361796.38    153422.62     27475.57         0.04426         0.04700         0.11900         0.23900    195324.39

memcached_mem-64 memc_suffix-lru threads-16 server_thread-10
Type         Ops/sec     Hits/sec   Misses/sec    Avg. Latency     p50 Latency     p99 Latency   p99.9 Latency       KB/sec
----------------------------------------------------------------------------------------------------------------------------
Sets       207575.84          ---          ---         0.03859         0.03900         0.10300         0.24700    216663.56
Gets       207575.84    175967.49     31608.35         0.03671         0.03900         0.10300         0.20700      7465.96
Waits           0.00          ---          ---             ---             ---             ---             ---          ---
Totals     415151.69    175967.49     31608.35         0.03765         0.03900         0.10300         0.23100    224129.53

memcached_mem-64 memc_suffix-rgc threads-16 server_thread-10
Type         Ops/sec     Hits/sec   Misses/sec    Avg. Latency     p50 Latency     p99 Latency   p99.9 Latency       KB/sec
----------------------------------------------------------------------------------------------------------------------------
Sets       179727.30          ---          ---         0.04511         0.04700         0.12700         0.26300    187595.80
Gets       179727.30    152427.62     27299.68         0.04262         0.03900         0.11900         0.23100      6464.32
Waits           0.00          ---          ---             ---             ---             ---             ---          ---
Totals     359454.60    152427.62     27299.68         0.04387         0.03900         0.11900         0.24700    194060.13

memcached_mem-64 memc_suffix-lru threads-16 server_thread-12
Type         Ops/sec     Hits/sec   Misses/sec    Avg. Latency     p50 Latency     p99 Latency   p99.9 Latency       KB/sec
----------------------------------------------------------------------------------------------------------------------------
Sets       211049.92          ---          ---         0.03777         0.03900         0.10300         0.25500    220289.74
Gets       211049.92    178968.22     32081.70         0.03546         0.03100         0.09500         0.21500      7590.92
Waits           0.00          ---          ---             ---             ---             ---             ---          ---
Totals     422099.85    178968.22     32081.70         0.03662         0.03900         0.10300         0.23100    227880.65

memcached_mem-64 memc_suffix-rgc threads-16 server_thread-12
Type         Ops/sec     Hits/sec   Misses/sec    Avg. Latency     p50 Latency     p99 Latency   p99.9 Latency       KB/sec
----------------------------------------------------------------------------------------------------------------------------
Sets       182567.66          ---          ---         0.04467         0.04700         0.12700         0.26300    190560.52
Gets       182567.66    154812.97     27754.70         0.04176         0.03900         0.11900         0.22300      6566.48
Waits           0.00          ---          ---             ---             ---             ---             ---          ---
Totals     365135.33    154812.97     27754.70         0.04321         0.03900         0.11900         0.23900    197127.00"""

import matplotlib.pyplot as plt
import numpy as np

threads_list = [2, 4, 6, 8, 10, 12]
def get_data(filepath):
    f = open(filepath)
    lru_tps = []
    lru_lat = []
    rgc_tps = []
    rgc_lat = []
    for thread in threads_list:
        for policy in ['lru', 'rgc']:
            lines = []
            for _ in range(8):
                line = f.readline()
                lines.append(line)
            pre_splited = lines[6].split(' ')
            splited = []
            for item in pre_splited:
                if item != '':
                    splited.append(item)
            print(splited)
            if policy == 'lru':
                # print(splited)
                lru_tps.append(float(splited[1]) / 1e6)
                lru_lat.append(float(splited[4]))
            else:
                rgc_tps.append(float(splited[1]) / 1e6)
                rgc_lat.append(float(splited[4]))
    return lru_tps, lru_lat, rgc_tps, rgc_lat

colors = ['#c44e52', '#8172b2', '#ccb974', '#86a38d', '#4c90b0', '#55a868', '#757272', '#78cbe3']

if __name__ == "__main__":

    lru_tps, lru_lat, rgc_tps, rgc_lat = get_data('local/log1101h_memtier.txt')
    plt.style.use('seaborn-v0_8')
    fig, ax = plt.subplots(figsize=(4, 3))

    X = np.arange(len(threads_list))
    ax.bar(X + 0.3, rgc_tps, width=0.3, label='RGC', hatch='\\\\')
    ax.bar(X, lru_tps, width=0.3, label='LRU', hatch='//')
    ax.set_xticks(X + 0.15)
    ax.set_xticklabels(threads_list)
    # ax.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
    ax.set_xlabel('#Threads')
    ax.set_ylabel('Throughput (M requests/s)')
    # ax.yaxis.grid(True)
    # ax.spines['bottom'].set_visible(True)
    # ax.spines['left'].set_visible(True)
    # ax.spines['top'].set_visible(True)
    # ax.spines['right'].set_visible(True)
    ax.legend()
    plt.tight_layout()
    plt.savefig('plots/D4.6/1.eps')
    plt.savefig('plots/D4.6/1.png')

    fig, ax = plt.subplots(figsize=(4, 3))

    X = np.arange(len(threads_list))

    ax.bar(X + 0.3, rgc_lat, width=0.3, label='RGC', hatch='\\\\')
    ax.bar(X, lru_lat, width=0.3, label='LRU', hatch='//')
    ax.set_xticks(X + 0.15)
    ax.set_xticklabels(threads_list)
    ax.set_xlabel('#Threads')
    ax.set_ylabel('Average Latency (ms)')
    ax.legend()
    plt.tight_layout()
    plt.savefig('plots/D4.6/2.eps')
    plt.savefig('plots/D4.6/2.png')

    sum = 0
    count = 0
    for lru, rgc in zip(lru_tps, rgc_tps):
        sum += lru / rgc - 1
        count += 1
    print(f'tps: {sum / count * 100}%')

    sum = 0
    count = 0
    for lru, rgc in zip(lru_lat, rgc_lat):
        sum += 1 - rgc / lru
        count += 1
    print(f'lat: {sum / count * 100}%')