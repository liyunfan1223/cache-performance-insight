import matplotlib.pyplot as plt
import numpy as np

threads_displayed = 10
data = {
    "tps": {
        "lru": [4744.19, 7488.77, 11417.57, 18369.07, 30691.91, 45962.01, 64197.73, 53522.28, 53681.52, 52942.06],
        "gs-lrfu": [5419.63, 8608.72, 13451.86, 23638.03, 36596.83, 57214.80, 76438.50, 62737.08, 62348.38, 62363.91],
    },
    "avg_lat": {
        "lru": [0.1909, 0.2551, 0.3338, 0.4110, 0.4859, 0.6066, 0.8603, 2.2697, 4.7334, 9.2552],
        "gs-lrfu": [0.1708, 0.2218, 0.2871, 0.3417, 0.4076, 0.5180, 0.7448, 1.9328, 3.8810, 7.9703],
    },
    "mem_lat": {
        "lru": [0.0598, 0.0703, 0.0799, 0.0711, 0.0993, 0.1604, 0.2822, 0.5712, 1.4768, 3.8671],
        "gs-lrfu": [0.0602, 0.0718, 0.0817, 0.0739, 0.1064, 0.1716, 0.3125, 0.5686, 1.5739, 4.1545],
    },
    "rdb_lat": {
        "lru": [0.2724, 0.3699, 0.4915, 0.6220, 0.7258, 0.8830, 1.2166, 3.2670, 6.6149, 12.3679],
        "gs-lrfu": [0.2840, 0.3754, 0.4974, 0.6155, 0.7158, 0.8720, 1.1845, 3.2686, 6.1517, 11.6957],
    },
}

threads = [2 ** k for k in range(0, 10)]
# threads[-2] = threads[-1] = threads[-3]
def tps():
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.plot(threads[:threads_displayed], data["tps"]["lru"][:threads_displayed], label="LRU", marker='o', linestyle='-.')
    ax.plot(threads[:threads_displayed], data["tps"]["gs-lrfu"][:threads_displayed], label="GS-LRFU", marker='o', linestyle='-.')
    ax.set_xscale('log')
    ax.set_yscale('log')
    plt.legend()
    plt.savefig("local/vis_memc_rdb_tp.png")
    plt.show()

def avg_lat():
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.plot(threads[:threads_displayed], data["avg_lat"]["lru"][:threads_displayed], label="avg-LRU", color='r')
    ax.plot(threads[:threads_displayed], data["avg_lat"]["gs-lrfu"][:threads_displayed], label="avg-GS-LRFU", color='b')

    ax.plot(threads[:threads_displayed], data["mem_lat"]["lru"][:threads_displayed], label="mem-LRU", color='r')
    ax.plot(threads[:threads_displayed], data["mem_lat"]["gs-lrfu"][:threads_displayed], label="mem-GS-LRFU", color='b')

    ax.plot(threads[:threads_displayed], data["rdb_lat"]["lru"][:threads_displayed], label="rdb-LRU", color='r')
    ax.plot(threads[:threads_displayed], data["rdb_lat"]["gs-lrfu"][:threads_displayed], label="rdb-GS-LRFU", color='b')
    # ax.set_xscale('log')
    # ax.set_yscale('log')
    plt.legend()
    plt.savefig("local/vis_memc_rdb_avglat.png")
    plt.show()

if __name__ == "__main__":
    tps()
    avg_lat()