import matplotlib.pyplot as plt
import matplotlib.style
import numpy as np

# print(matplotlib.style.available)
plt.style.use('seaborn-v0_8-paper')

data = {
    "P1-64M-1K-rgc" : {
        "tps": np.asarray([5923.40, 9242.99, 13881.93, 21562.43, 31944.23, 45613.91, 55233.91, 67830.90, 71433.66, 74942.23]),
        "hr": np.asarray([50.81, 50.86, 50.82, 50.83, 50.80, 50.74, 50.72, 50.76, 50.74, 50.73]),
        "avg_lat": np.asarray([0.1685, 0.2160, 0.2877, 0.3706, 0.5004, 0.7011, 1.1581, 1.8860, 3.5825, 6.8305]),
        "tpsdiskmb":np.asarray([2.13, 3.33, 5.00, 7.77, 11.51, 16.46, 19.93, 24.46, 25.77, 27.04]),
    },
    "P1-64M-1K-lru" : {
        "tps": np.asarray([4829.28, 8002.84, 11430.35, 17426.92, 25649.83, 36478.76, 46419.85, 55830.68, 63224.03, 68124.98]),
        "hr": np.asarray([37.30, 37.34, 37.36, 37.31, 37.30, 37.30, 37.29, 37.27, 37.24, 37.25]),
        "avg_lat": np.asarray([0.2067, 0.2495, 0.3495, 0.4586, 0.6233, 0.8767, 1.3781, 2.2912, 4.0478, 7.5114]),
        "tpsdiskmb":np.asarray([2.22, 3.67, 5.24, 8.00, 11.78, 16.75, 21.32, 25.65, 29.06, 31.31]),
    },
    "P1-2048M-32K-rgc" : {
        "tps": np.asarray([2723.92, 5302.09, 9367.29, 15708.33, 23832.75, 30891.24, 36095.28, 35682.09, 31385.80, 28861.54]),
        "hr": np.asarray([52.92, 52.88, 52.88, 52.87, 52.91, 52.94, 45.88, 30.18, 15.97, 7.42]),
        "avg_lat": np.asarray([0.3667, 0.3768, 0.4265, 0.5088, 0.6708, 1.0353, 1.7722, 3.5855, 8.1518, 17.7309]),
        "tpsdiskmb":np.asarray([30.06, 58.56, 103.44, 173.52, 263.01, 340.70, 457.88, 583.90, 618.13, 626.25]),
    },
    "P1-2048M-32K-lru" : {
        "tps": np.asarray([2327.97, 4413.83, 7705.66, 12903.76, 19923.48, 26451.52, 30226.97, 32376.43, 30815.46, 29108.65]),
        "hr": np.asarray([41.02, 41.03, 41.02, 41.06, 41.05, 41.03, 35.77, 23.39, 13.43, 7.14]),
        "avg_lat": np.asarray([0.4292, 0.4527, 0.5186, 0.6194, 0.8025, 1.2092, 2.1166, 3.9522, 8.3048, 17.5770]),
        "tpsdiskmb":np.asarray([32.18, 61.00, 106.53, 178.26, 275.29, 365.61, 455.02, 581.37, 625.27, 633.53]),
    },
    "OLTP-3M-8K-rgc": {
        "tps": np.asarray([2469.60, 4547.91, 8433.53, 15372.54, 26814.57, 41260.92, 52068.15, 57327.76, 60660.08, 60057.95]),
        "hr": np.asarray([29.11, 28.92, 29.02, 28.83, 29.00, 28.98, 28.96, 28.93, 28.30, 28.39]),
        "avg_lat": np.asarray([0.4047, 0.4394, 0.4739, 0.5197, 0.5960, 0.7748, 1.2250, 2.2237, 4.1548, 8.3783]),
        "tpsdiskmb": np.asarray([10.26, 18.94, 35.08, 64.10, 111.56, 171.71, 216.72, 238.72, 254.85, 251.99]),

    },
    "OLTP-3M-8K-lru": {
        "tps": np.asarray([2019.02, 3734.08, 6969.36, 12807.96, 22813.32, 35256.29, 45745.71, 50528.59, 55255.98, 54295.87]),
        "hr": np.asarray([24.98, 21.57, 19.75, 18.31, 17.26, 16.77, 16.28, 15.40, 14.46, 14.23]),
        "avg_lat": np.asarray([0.4950, 0.5353, 0.5736, 0.5221, 0.6998, 0.9039, 1.3939, 2.5186, 4.5710, 9.2977]),
        "tpsdiskmb": np.asarray([8.88, 17.16, 32.77, 61.30, 110.60, 171.94, 224.40, 250.46, 276.95, 272.88]),
    },
    "OLTP-12M-32K-rgc": {
        "tps": np.asarray([1924.57, 3404.77, 6059.67, 10746.41, 17924.77, 25316.13, 29115.68, 31817.21, 32103.98, 30813.28]),
        "hr": np.asarray([27.05, 27.03, 27.16, 27.12, 26.94, 26.65, 26.86, 26.76, 26.87, 26.60]),
        "avg_lat": np.asarray([0.5193, 0.5876, 0.6597, 0.7440, 0.8921, 1.2568, 2.1723, 3.9511, 7.9135, 16.4548]),
        "tpsdiskmb": np.asarray([32.90, 58.18, 103.45, 183.55, 306.92, 435.21, 499.12, 546.15, 550.24, 530.10])
    },
    "OLTP-12M-32K-lru": {
        "tps": np.asarray([1622.50, 2869.76, 5237.58, 9097.48, 15248.42, 21691.63, 24268.32, 26709.24, 27035.04, 26140.62]),
        "hr": np.asarray([22.39, 20.07, 17.99, 16.19, 15.55, 15.05, 14.50, 13.43, 13.18, 12.60]),
        "avg_lat": np.asarray([0.6161, 0.6966, 0.7633, 0.8789, 1.0487, 1.4730, 2.6240, 4.7327, 9.3290, 19.4476]),
        "tpsdiskmb": np.asarray([29.51, 53.76, 100.67, 178.71, 301.83, 431.88, 486.33, 541.93, 550.12, 535.50])
    },
}

threads = [2 ** k for k in range(0, 10)]

def P1():

    fig = plt.figure(figsize=(14,7))
    ax = fig.subplots(2, 2)
    ax1 = ax[0][0]
    ax1.plot(threads, data["P1-64M-1K-rgc"]["tps"], label="RGC", marker='o', linestyle='-')
    ax1.plot(threads, data["P1-64M-1K-lru"]["tps"], label="LRU", marker='s', linestyle=':')
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_xlabel("Threads")
    ax1.set_ylabel("Throughput (requests/s)", fontsize=12)
    ax1.set_xticks([1, 2, 4, 8, 16, 32, 64, 128, 256, 512])
    ax1.set_xticklabels([1, 2, 4, 8, 16, 32, 64, 128, 256, 512])
    ax1.set_yticks([2 ** i for i in range(13, 18)])
    ax1.set_yticklabels([f"$2^{{{i}}}$" for i in range(13, 18)])
    ax1.legend(loc=4)

    ax2 = ax[0][1]
    ax2.plot(threads, data["P1-64M-1K-rgc"]["hr"], label="RGC", marker='o', linestyle='-')
    ax2.plot(threads, data["P1-64M-1K-lru"]["hr"], label="LRU", marker='s', linestyle=':')
    ax2.set_xscale('log')
    # ax2.set_yscale('log')
    ax2.set_xlabel("Threads")
    ax2.set_ylabel("Hit ratio(%)", fontsize=12)
    ax2.set_xticks([1, 2, 4, 8, 16, 32, 64, 128, 256, 512])
    ax2.set_xticklabels([1, 2, 4, 8, 16, 32, 64, 128, 256, 512])
    ax2.set_ylim(10, 60)
    ax2.legend(loc=4)

    ax3 = ax[1][0]
    ax3.plot(threads, data["P1-64M-1K-rgc"]["tpsdiskmb"], label="RGC", marker='o', linestyle='-')
    ax3.plot(threads, data["P1-64M-1K-lru"]["tpsdiskmb"], label="LRU", marker='s', linestyle=':')
    ax3.set_xscale('log')
    ax3.set_yscale('log')
    ax3.set_xlabel("Threads")
    ax3.set_ylabel("Disk IO throughput (MB/s)", fontsize=12)
    ax3.set_xticks([1, 2, 4, 8, 16, 32, 64, 128, 256, 512])
    ax3.set_xticklabels([1, 2, 4, 8, 16, 32, 64, 128, 256, 512])
    ax3.set_yticks([2, 4, 8, 16, 32])
    ax3.set_yticklabels([2, 4, 8, 16, 32])
    ax3.legend(loc=4)

    ax4 = ax[1][1]
    ax4.plot(threads, data["P1-64M-1K-rgc"]["avg_lat"], label="RGC", marker='o', linestyle='-')
    ax4.plot(threads, data["P1-64M-1K-lru"]["avg_lat"], label="LRU", marker='s', linestyle=':')
    ax4.set_xscale('log')
    # ax4.set_yscale('log')
    ax4.set_xlabel("Threads")
    ax4.set_ylabel("Average latency (ms)", fontsize=12)
    ax4.set_xticks([1, 2, 4, 8, 16, 32, 64, 128, 256, 512])
    ax4.set_xticklabels([1, 2, 4, 8, 16, 32, 64, 128, 256, 512])
    ax4.legend(loc=4)

    plt.savefig("plots/4.2.2/1.png")
    plt.show()

def P2():
    fig = plt.figure(figsize=(14,7))
    ax = fig.subplots(2, 2)
    ax1 = ax[0][0]
    ax1.plot(threads, data["P1-2048M-32K-rgc"]["tps"], label="RGC", marker='o', linestyle='-')
    ax1.plot(threads, data["P1-2048M-32K-lru"]["tps"], label="LRU", marker='s', linestyle=':')
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_xlabel("Threads")
    ax1.set_ylabel("Throughput (requests/s)", fontsize=12)
    ax1.set_xticks([1, 2, 4, 8, 16, 32, 64, 128, 256, 512])
    ax1.set_xticklabels([1, 2, 4, 8, 16, 32, 64, 128, 256, 512])
    ax1.set_yticks([2 ** i for i in range(13, 17)])
    ax1.set_yticklabels([f"$2^{{{i}}}$" for i in range(13, 17)])
    ax1.legend(loc=4)

    ax2 = ax[0][1]
    ax2.plot(threads, data["P1-2048M-32K-rgc"]["hr"], label="RGC", marker='o', linestyle='-')
    ax2.plot(threads, data["P1-2048M-32K-lru"]["hr"], label="LRU", marker='s', linestyle=':')
    ax2.set_xscale('log')
    # ax2.set_yscale('log')
    ax2.set_xlabel("Threads")
    ax2.set_ylabel("Hit ratio(%)", fontsize=12)
    ax2.set_xticks([1, 2, 4, 8, 16, 32, 64])
    ax2.set_xticklabels([1, 2, 4, 8, 16, 32, 64])
    ax2.set_ylim(5, 60)
    ax2.legend(loc=4)

    ax3 = ax[1][0]
    ax3.plot(threads, data["P1-2048M-32K-rgc"]["tpsdiskmb"], label="RGC", marker='o', linestyle='-')
    ax3.plot(threads, data["P1-2048M-32K-lru"]["tpsdiskmb"], label="LRU", marker='s', linestyle=':')
    ax3.set_xscale('log')
    ax3.set_yscale('log')
    ax3.set_xlabel("Threads")
    ax3.set_ylabel("Throughput (MB/s)", fontsize=12)
    ax3.set_xticks([1, 2, 4, 8, 16, 32, 64])
    ax3.set_xticklabels([1, 2, 4, 8, 16, 32, 64])
    ax3.set_yticks([32,64,128,256,512,1024])
    ax3.set_yticklabels([32,64,128,256,512,1024])
    ax3.legend(loc=4)

    ax4 = ax[1][1]
    ax4.plot(threads, data["P1-2048M-32K-rgc"]["avg_lat"], label="RGC", marker='o', linestyle='-')
    ax4.plot(threads, data["P1-2048M-32K-lru"]["avg_lat"], label="LRU", marker='s', linestyle=':')
    ax4.set_xscale('log')
    # ax4.set_yscale('log')
    ax4.set_xlabel("Threads")
    ax4.set_ylabel("Average latency (ms)", fontsize=12)
    ax4.set_xticks([1, 2, 4, 8, 16, 32, 64])
    ax4.set_xticklabels([1, 2, 4, 8, 16, 32, 64])
    # ax4.set_yticks([0.1 * i for i in np.arange(1, 11)])
    # ax4.set_yticklabels([0.1 * i for i in np.arange(1, 11)])
    ax4.set_ylim(-1, 20)
    ax4.legend(loc=4)

    plt.savefig("plots/4.2.2/2.png")
    plt.show()

def OLTP_a():

    fig = plt.figure(figsize=(14,7))
    ax = fig.subplots(2, 2)
    ax1 = ax[0][0]
    ax1.plot(threads, data["OLTP-3M-8K-rgc"]["tps"], label="RGC", marker='o', linestyle='-')
    ax1.plot(threads, data["OLTP-3M-8K-lru"]["tps"], label="LRU", marker='s', linestyle=':')
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_xlabel("Threads")
    ax1.set_ylabel("Throughput (requests/s)", fontsize=12)
    ax1.set_xticks([1, 2, 4, 8, 16, 32, 64, 128, 256, 512])
    ax1.set_xticklabels([1, 2, 4, 8, 16, 32, 64, 128, 256, 512])
    ax1.set_yticks([2 ** i for i in range(11, 17)])
    ax1.set_yticklabels([f"$2^{{{i}}}$" for i in range(11, 17)])
    ax1.legend(loc=4)

    ax2 = ax[0][1]
    ax2.plot(threads, data["OLTP-3M-8K-rgc"]["hr"], label="RGC", marker='o', linestyle='-')
    ax2.plot(threads, data["OLTP-3M-8K-lru"]["hr"], label="LRU", marker='s', linestyle=':')
    ax2.set_xscale('log')
    # ax2.set_yscale('log')
    ax2.set_xlabel("Threads")
    ax2.set_ylabel("Hit ratio(%)", fontsize=12)
    ax2.set_xticks([1, 2, 4, 8, 16, 32, 64, 128, 256, 512])
    ax2.set_xticklabels([1, 2, 4, 8, 16, 32, 64, 128, 256, 512])
    ax2.set_ylim(10, 35)
    ax2.legend(loc=4)

    ax3 = ax[1][0]
    ax3.plot(threads, data["OLTP-3M-8K-rgc"]["tpsdiskmb"], label="RGC", marker='o', linestyle='-')
    ax3.plot(threads, data["OLTP-3M-8K-lru"]["tpsdiskmb"], label="LRU", marker='s', linestyle=':')
    ax3.set_xscale('log')
    ax3.set_yscale('log')
    ax3.set_xlabel("Threads")
    ax3.set_ylabel("Disk IO throughput (MB/s)", fontsize=12)
    ax3.set_xticks([1, 2, 4, 8, 16, 32, 64, 128, 256, 512])
    ax3.set_xticklabels([1, 2, 4, 8, 16, 32, 64, 128, 256, 512])
    ax3.set_yticks([8, 16, 32, 64, 128, 256])
    ax3.set_yticklabels([8, 16, 32, 64, 128, 256])
    ax3.legend(loc=4)

    ax4 = ax[1][1]
    ax4.plot(threads, data["OLTP-3M-8K-rgc"]["avg_lat"], label="RGC", marker='o', linestyle='-')
    ax4.plot(threads, data["OLTP-3M-8K-lru"]["avg_lat"], label="LRU", marker='s', linestyle=':')
    ax4.set_xscale('log')
    # ax4.set_yscale('log')
    ax4.set_xlabel("Threads")
    ax4.set_ylabel("Average latency (ms)", fontsize=12)
    ax4.set_xticks([1, 2, 4, 8, 16, 32, 64, 128, 256, 512])
    ax4.set_xticklabels([1, 2, 4, 8, 16, 32, 64, 128, 256, 512])
    ax4.legend(loc=4)

    plt.savefig("plots/4.2.2/3.png")
    plt.show()

def OLTP_b():
    fig = plt.figure(figsize=(14,7))
    ax = fig.subplots(2, 2)
    ax1 = ax[0][0]
    ax1.plot(threads, data["OLTP-12M-32K-rgc"]["tps"], label="RGC", marker='o', linestyle='-')
    ax1.plot(threads, data["OLTP-12M-32K-lru"]["tps"], label="LRU", marker='s', linestyle=':')
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_xlabel("Threads")
    ax1.set_ylabel("Throughput (requests/s)", fontsize=12)
    ax1.set_xticks([1, 2, 4, 8, 16, 32, 64, 128, 256, 512])
    ax1.set_xticklabels([1, 2, 4, 8, 16, 32, 64, 128, 256, 512])
    ax1.set_yticks([2 ** i for i in range(11, 16)])
    ax1.set_yticklabels([f"$2^{{{i}}}$" for i in range(11, 16)])
    ax1.legend(loc=4)

    ax2 = ax[0][1]
    ax2.plot(threads, data["OLTP-12M-32K-rgc"]["hr"], label="RGC", marker='o', linestyle='-')
    ax2.plot(threads, data["OLTP-12M-32K-lru"]["hr"], label="LRU", marker='s', linestyle=':')
    ax2.set_xscale('log')
    # ax2.set_yscale('log')
    ax2.set_xlabel("Threads")
    ax2.set_ylabel("Hit ratio(%)", fontsize=12)
    ax2.set_xticks([1, 2, 4, 8, 16, 32, 64])
    ax2.set_xticklabels([1, 2, 4, 8, 16, 32, 64])
    ax2.set_ylim(5, 35)
    ax2.legend(loc=4)

    ax3 = ax[1][0]
    ax3.plot(threads, data["OLTP-12M-32K-rgc"]["tpsdiskmb"], label="RGC", marker='o', linestyle='-')
    ax3.plot(threads, data["OLTP-12M-32K-lru"]["tpsdiskmb"], label="LRU", marker='s', linestyle=':')
    ax3.set_xscale('log')
    ax3.set_yscale('log')
    ax3.set_xlabel("Threads")
    ax3.set_ylabel("Throughput (MB/s)", fontsize=12)
    ax3.set_xticks([1, 2, 4, 8, 16, 32, 64])
    ax3.set_xticklabels([1, 2, 4, 8, 16, 32, 64])
    ax3.set_yticks([32,64,128,256,512])
    ax3.set_yticklabels([32,64,128,256,512])
    ax3.legend(loc=4)

    ax4 = ax[1][1]
    ax4.plot(threads, data["OLTP-12M-32K-rgc"]["avg_lat"], label="RGC", marker='o', linestyle='-')
    ax4.plot(threads, data["OLTP-12M-32K-lru"]["avg_lat"], label="LRU", marker='s', linestyle=':')
    ax4.set_xscale('log')
    # ax4.set_yscale('log')
    ax4.set_xlabel("Threads")
    ax4.set_ylabel("Average latency (ms)", fontsize=12)
    ax4.set_xticks([1, 2, 4, 8, 16, 32, 64])
    ax4.set_xticklabels([1, 2, 4, 8, 16, 32, 64])
    # ax4.set_yticks([0.1 * i for i in np.arange(1, 11)])
    # ax4.set_yticklabels([0.1 * i for i in np.arange(1, 11)])
    ax4.set_ylim(-1, 20)
    ax4.legend(loc=4)

    plt.savefig("plots/4.2.2/4.png")
    plt.show()

if __name__ == "__main__":
    P1()
    P2()

    OLTP_a()
    OLTP_b()