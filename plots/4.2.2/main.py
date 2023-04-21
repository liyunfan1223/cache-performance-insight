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
        "tpsdiskmb":np.asarray([30.06, 58.56, 103.44, 173.52, 263.01, 340.07, 457.88, 583.90, 518.13, 626.25]),
    },
    "P1-2048M-32K-lru" : {
        "tps": np.asarray([2327.97, 4413.83, 7705.66, 12903.76, 19923.48, 26451.52, 30226.97, 32376.43, 30815.46, 29108.65]),
        "hr": np.asarray([41.02, 41.03, 41.02, 41.06, 41.05, 41.03, 35.77, 23.39, 13.43, 7.14]),
        "avg_lat": np.asarray([0.4292, 0.4527, 0.5186, 0.6194, 0.8025, 1.2092, 2.1166, 3.9522, 8.3048, 17.5770]),
        "tpsdiskmb":np.asarray([32.18, 61.00, 106.53, 178.26, 275.29, 365.61, 455.02, 581.37, 625.27, 633.53]),
    },
}

threads = [2 ** k for k in range(0, 10)]

def P1():

    fig = plt.figure(figsize=(14,7))
    ax = fig.subplots(2, 2)
    ax1 = ax[0][0]
    ax1.plot(threads, data["P1-64M-1K-rgc"]["tps"], label="RGC", marker='o', linestyle='dashed')
    ax1.plot(threads, data["P1-64M-1K-lru"]["tps"], label="LRU", marker='s', linestyle=':')
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_xlabel("Threads", fontsize=12)
    ax1.set_ylabel("Throughput (requests/s)", fontsize=12)
    ax1.set_xticks([1, 2, 4, 8, 16, 32, 64, 128, 256, 512])
    ax1.set_xticklabels([1, 2, 4, 8, 16, 32, 64, 128, 256, 512])
    ax1.set_yticks([2 ** i for i in range(13, 18)])
    ax1.set_yticklabels([f"$2^{{{i}}}$" for i in range(13, 18)])
    ax1.legend(loc=4)

    ax2 = ax[0][1]
    ax2.plot(threads, data["P1-64M-1K-rgc"]["hr"], label="RGC", marker='o', linestyle='dashed')
    ax2.plot(threads, data["P1-64M-1K-lru"]["hr"], label="LRU", marker='s', linestyle=':')
    ax2.set_xscale('log')
    # ax2.set_yscale('log')
    ax2.set_xlabel("Threads", fontsize=12)
    ax2.set_ylabel("Hit ratio(%)", fontsize=12)
    ax2.set_xticks([1, 2, 4, 8, 16, 32, 64, 128, 256, 512])
    ax2.set_xticklabels([1, 2, 4, 8, 16, 32, 64, 128, 256, 512])
    ax2.set_ylim(10, 60)
    ax2.legend(loc=4)

    ax3 = ax[1][0]
    ax3.plot(threads, data["P1-64M-1K-rgc"]["tpsdiskmb"], label="RGC", marker='o', linestyle='dashed')
    ax3.plot(threads, data["P1-64M-1K-lru"]["tpsdiskmb"], label="LRU", marker='s', linestyle=':')
    ax3.set_xscale('log')
    ax3.set_yscale('log')
    ax3.set_xlabel("Threads", fontsize=12)
    ax3.set_ylabel("Disk IO throughput (MB/s)", fontsize=12)
    ax3.set_xticks([1, 2, 4, 8, 16, 32, 64, 128, 256, 512])
    ax3.set_xticklabels([1, 2, 4, 8, 16, 32, 64, 128, 256, 512])
    ax3.set_yticks([2, 4, 8, 16, 32])
    ax3.set_yticklabels([2, 4, 8, 16, 32])
    ax3.legend(loc=4)

    ax4 = ax[1][1]
    ax4.plot(threads, data["P1-64M-1K-rgc"]["avg_lat"], label="RGC", marker='o', linestyle='dashed')
    ax4.plot(threads, data["P1-64M-1K-lru"]["avg_lat"], label="LRU", marker='s', linestyle=':')
    ax4.set_xscale('log')
    # ax4.set_yscale('log')
    ax4.set_xlabel("Threads", fontsize=12)
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
    ax1.plot(threads, data["P1-2048M-32K-rgc"]["tps"], label="RGC", marker='o', linestyle='dashed')
    ax1.plot(threads, data["P1-2048M-32K-lru"]["tps"], label="LRU", marker='s', linestyle=':')
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_xlabel("Threads", fontsize=12)
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
    ax2.set_xlabel("Threads", fontsize=12)
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
    ax3.set_xlabel("Threads", fontsize=12)
    ax3.set_ylabel("Throughput (MB/s)", fontsize=12)
    ax3.set_xticks([1, 2, 4, 8, 16, 32, 64])
    ax3.set_xticklabels([1, 2, 4, 8, 16, 32, 64])
    ax3.set_yticks([32,64,128,256,512,1024])
    ax3.set_yticklabels([32,64,128,256,512,1024])
    ax3.legend(loc=4)

    ax4 = ax[1][1]
    ax4.plot(threads, data["P1-2048M-32K-rgc"]["avg_lat"], label="RGC", marker='o', linestyle='dashed')
    ax4.plot(threads, data["P1-2048M-32K-lru"]["avg_lat"], label="LRU", marker='s', linestyle=':')
    ax4.set_xscale('log')
    # ax4.set_yscale('log')
    ax4.set_xlabel("Threads", fontsize=12)
    ax4.set_ylabel("Average latency (ms)", fontsize=12)
    ax4.set_xticks([1, 2, 4, 8, 16, 32, 64])
    ax4.set_xticklabels([1, 2, 4, 8, 16, 32, 64])
    # ax4.set_yticks([0.1 * i for i in np.arange(1, 11)])
    # ax4.set_yticklabels([0.1 * i for i in np.arange(1, 11)])
    ax4.set_ylim(-1, 20)
    ax4.legend(loc=4)

    plt.savefig("plots/4.2.2/2.png")
    plt.show()

if __name__ == "__main__":
    P1()
    P2()