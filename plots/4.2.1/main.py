import matplotlib.pyplot as plt
import matplotlib.style
import numpy as np
from matplotlib.ticker import LogitLocator, LogitFormatter

# print(matplotlib.style.available)
plt.style.use('seaborn-v0_8-paper')

data = {
    "4M1K-rgc" : {
        "tps": np.asarray([13004.35, 23046.69, 40102.26, 78825.54, 95719.11, 100310.20, 99769.55]),
        "hr": np.asarray([47.55, 48.10, 47.39, 47.72, 47.97, 48.70, 49.26]),
        "avg_lat": np.asarray([0.075, 0.086, 0.098, 0.100, 0.165, 0.317, 0.639]),
        "tpskb":np.asarray([12409.81, 21993.03, 38268.85, 75221.76, 91342.98, 95724.17, 95208.24]),
    },
    "4M1K-lru" : {
        "tps": np.asarray([12906.35, 23012.05, 41165.04, 82259.88, 118961.79, 133140.57, 127745.77]),
        "hr": np.asarray([38.42, 40.62, 41.68, 43.60, 44.21, 45.45, 46.97]),
        "avg_lat": np.asarray([0.075, 0.085, 0.096, 0.096, 0.133, 0.238, 0.497]),
        "tpskb": np.asarray([12316.29, 21959.97, 39283.04, 78499.09, 113523.04, 127053.59, 121905.43]),
    },

    "4M1K-rgc_2" : {
        "tps": np.asarray([11519.96, 21871.33, 39019.47, 74482.30, 95594.96, 92624.05, 89026.53]),
        "hr": np.asarray([47.55, 49.36, 50.25, 50.82, 49.75, 46.03, 43.42, ]),
        "avg_lat": np.asarray([0.085, 0.090, 0.100, 0.105, 0.165, 0.343, 0.715]),
        "tpskb":np.asarray([10993.28, 20871.41, 37235.56, 71077.09, 91224.51, 88389.43, 84956.38]),
    },
    "4M1K-lru_2" : {
        "tps": np.asarray([12205.73, 23842.95, 41737.47, 85914.91, 121824.53, 142896.48, 138361.86]),
        "hr": np.asarray([38.42, 38.34, 38.38, 38.46, 38.57, 38.51, 38.53]),
        "avg_lat": np.asarray([0.080, 0.083, 0.094, 0.091, 0.129, 0.222, 0.459]),
        "tpskb": np.asarray([11647.70, 22752.89, 39829.30, 81987.02, 116254.91, 136363.47, 132036.17]),
    },

    "128M32K-rgc" : {
        "tps": np.asarray([11074.99, 19070.93, 31617.69, 52183.93, 61441.06, 62754.18, 57231.74]),
        "hr": np.asarray([51.11, 51.13, 51.24, 51.46, 51.37, 51.78, 52.18]),
        "avg_lat": np.asarray([0.089, 0.103, 0.124, 0.151, 0.259, 0.508, 1.116]),
        "tpskb": np.asarray([322682.78, 555654.00, 921218.42, 1520440.18, 1790157.54, 1828416.71, 1667513.97]),
    },
    "128M32K-lru" : {
        "tps": np.asarray([11232.36, 18765.95, 32374.43, 51649.36, 63646.56, 63606.41, 58740.76]),
        "hr": np.asarray([41.33, 45.28, 45.20, 47.39, 47.94, 48.26, 49.64]),
        "avg_lat": np.asarray([0.079, 0.095, 0.119, 0.127, 0.199, 0.391, 0.903]),
        "tpskb": np.asarray([327269.01, 546768.12, 943267.17, 1504864.72, 1854417.39, 1853247.42, 1711481.20]),
    },

    "128M32K-rgc_2" : {
        "tps": np.asarray([11280.64, 19689.30, 33378.88, 59860.56, 75278.17, 71795.83, 69522.18]),
        "hr": np.asarray([51.11, 52.92, 53.94, 54.63, 53.67, 49.90, 46.96]),
        "avg_lat": np.asarray([0.087, 0.100, 0.118, 0.132, 0.211, 0.444, 0.917]),
        "tpskb": np.asarray([328674.57, 573670.95, 972532.74, 1744107.68, 2193318.01, 2091856.00, 2025610.39]),
    },
    "128M32K-lru_2" : {
        "tps": np.asarray([10829.53, 20015.20, 35235.35, 62481.10, 82845.90, 90888.91, 94003.99]),
        "hr": np.asarray([41.33, 41.35, 41.64, 41.60, 41.66, 41.66, 41.63]),
        "avg_lat": np.asarray([0.091, 0.098, 0.112, 0.126, 0.191, 0.349, 0.679]),
        "tpskb": np.asarray([315530.97, 583166.28, 1026623.24, 1820460.15, 2413812.76, 2648155.11, 2738916.70]),
    },
}

threads = [2 ** k for k in range(0, 7)]

def P1():

    fig = plt.figure(figsize=(8, 4))
    ax = fig.subplots(2, 2)
    ax1 = ax[0][0]
    ax1.plot(threads, data["4M1K-rgc_2"]["tps"], label="RGC", marker='o', linestyle='-')
    ax1.plot(threads, data["4M1K-lru_2"]["tps"], label="LRU", marker='s', linestyle=':')
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_xlabel("Threads")
    ax1.set_ylabel("Throughput (requests/s)", fontsize=10)
    ax1.set_xticks([1, 2, 4, 8, 16, 32, 64])
    ax1.set_xticklabels([1, 2, 4, 8, 16, 32, 64])
    ax1.set_yticks([2 ** i for i in range(14, 18)])
    ax1.set_yticklabels([f"$2^{{{i}}}$" for i in range(14, 18)])
    ax1.legend(loc=4)

    ax2 = ax[0][1]
    ax2.plot(threads, data["4M1K-rgc_2"]["hr"], label="RGC", marker='o', linestyle='-')
    ax2.plot(threads, data["4M1K-lru_2"]["hr"], label="LRU", marker='s', linestyle=':')
    ax2.set_xscale('log')
    # ax2.set_yscale('log')
    ax2.set_xlabel("Threads")
    ax2.set_ylabel("Hit ratio(%)", fontsize=10)
    ax2.set_xticks([1, 2, 4, 8, 16, 32, 64])
    ax2.set_xticklabels([1, 2, 4, 8, 16, 32, 64])
    ax2.set_ylim(32)
    # ax3.set_yticklabels([16, 32, 64, 128])
    ax2.legend(loc=4)

    ax3 = ax[1][0]
    ax3.plot(threads, data["4M1K-rgc_2"]["tpskb"] / 1024, label="RGC", marker='o', linestyle='-')
    ax3.plot(threads, data["4M1K-lru_2"]["tpskb"] / 1024, label="LRU", marker='s', linestyle=':')
    ax3.set_xscale('log')
    ax3.set_yscale('log')
    ax3.set_xlabel("Threads")
    ax3.set_ylabel("Throughput (MB/s)", fontsize=10)
    ax3.set_xticks([1, 2, 4, 8, 16, 32, 64])
    ax3.set_xticklabels([1, 2, 4, 8, 16, 32, 64])
    ax3.set_yticks([16, 32, 64, 128])
    ax3.set_yticklabels([16, 32, 64, 128])
    # ax3.set_xticklabels([1, 2, 4, 8, 16, 32, 64])
    ax3.legend(loc=4)

    ax4 = ax[1][1]
    ax4.plot(threads, data["4M1K-rgc_2"]["avg_lat"], label="RGC", marker='o', linestyle='-')
    ax4.plot(threads, data["4M1K-lru_2"]["avg_lat"], label="LRU", marker='s', linestyle=':')
    ax4.set_xscale('log')
    # ax4.set_yscale('log')
    ax4.set_xlabel("Threads")
    ax4.set_ylabel("Average latency (ms)", fontsize=10)
    ax4.set_xticks([1, 2, 4, 8, 16, 32, 64])
    ax4.set_xticklabels([1, 2, 4, 8, 16, 32, 64])
    ax4.legend(loc=4)

    plt.savefig("plots/4.2.1/1.png")
    plt.show()

def P2():
    fig = plt.figure(figsize=(8, 4))
    ax = fig.subplots(2, 2)
    ax1 = ax[0][0]
    ax1.plot(threads, data["128M32K-rgc_2"]["tps"], label="RGC", marker='o', linestyle='-')
    ax1.plot(threads, data["128M32K-lru_2"]["tps"], label="LRU", marker='s', linestyle=':')
    ax1.set_xlabel("Threads")
    ax1.set_ylabel("Throughput (requests/s)", fontsize=10)
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    # ax1.set_yticks([2 ** i for i in range(14, 17)])
    # ax1.set_yticklabels([f"$2^{{{i}}}$" for i in range(14, 17)])
    ax1.set_yticks([2 ** i for i in range(13, 18)])
    ax1.set_yticklabels([f"$2^{{{i}}}$" for i in range(13, 18)])

    ax1.legend(loc=4)

    ax2 = ax[0][1]
    ax2.plot(threads, data["128M32K-rgc_2"]["hr"], label="RGC", marker='o', linestyle='-')
    ax2.plot(threads, data["128M32K-lru_2"]["hr"], label="LRU", marker='s', linestyle=':')
    ax2.set_xscale('log')
    # ax2.set_yscale('log')
    ax2.set_xlabel("Threads")
    ax2.set_ylabel("Hit ratio(%)", fontsize=10)
    ax2.set_xticks([1, 2, 4, 8, 16, 32, 64])
    ax2.set_xticklabels([1, 2, 4, 8, 16, 32, 64])
    ax2.set_ylim(36)
    ax2.legend(loc=4)

    ax3 = ax[1][0]
    ax3.plot(threads, data["128M32K-rgc_2"]["tpskb"] / 1024, label="RGC", marker='o', linestyle='-')
    ax3.plot(threads, data["128M32K-lru_2"]["tpskb"] / 1024, label="LRU", marker='s', linestyle=':')
    ax3.set_xscale('log')
    ax3.set_yscale('log')
    ax3.set_xlabel("Threads")
    ax3.set_ylabel("Throughput (MB/s)", fontsize=10)
    ax3.set_xticks([1, 2, 4, 8, 16, 32, 64])
    ax3.set_xticklabels([1, 2, 4, 8, 16, 32, 64])
    ax3.set_yticks([])
    ax3.set_yticks([128, 256, 512, 1024, 2048])
    ax3.set_yticklabels([128, 256, 512, 1024, 2048])
    ax3.legend(loc=4)

    ax4 = ax[1][1]
    ax4.plot(threads, data["128M32K-rgc_2"]["avg_lat"], label="RGC", marker='o', linestyle='-')
    ax4.plot(threads, data["128M32K-lru_2"]["avg_lat"], label="LRU", marker='s', linestyle=':')
    ax4.set_xscale('log')
    # ax4.set_yscale('log')
    ax4.set_xlabel("Threads")
    ax4.set_ylabel("Average latency (ms)", fontsize=10)
    ax4.set_xticks([1, 2, 4, 8, 16, 32, 64])
    ax4.set_xticklabels([1, 2, 4, 8, 16, 32, 64])
    ax4.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax4.set_yticklabels([0.2, 0.4, 0.6, 0.8, 1.0])
    ax4.legend(loc=4)

    plt.savefig("plots/4.2.1/2.png")
    plt.show()

if __name__ == "__main__":
    P1()
    P2()