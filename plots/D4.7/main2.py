import matplotlib.pyplot as plt
import numpy as np



trace_name = ['vps26107', 'webmail', 'prxy_0', ]
datas = [[70.26, 61.05, 70.16], [73.72, 75.68, 72.94], [71.06, 68.69, 46.17]]
len = 3
# colors = ['#c44e52', '#8172b2', '#ccb974', '#86a38d', '#4c90b0', '#55a868', '#757272', '#78cbe3']

# colors = ['#4c90b0', '#55a868', '#c44e52', '#8172b2', '#ccb974', '#86a38d', '#78cbe3', '#757272']
colors = ['#89aed6', '#8ec98d', '#da9ca3', '#a6adcc', '#e3d5a2', '#aabca5', '#9fd8f0', '#999999']#稍微浅色
# colors=['#aec7e8', '#b3e2a1', '#f0abb5', '#c5c7e3', '#f4e5bd', '#c9d8bf', '#c0e1f5', '#c4c4c4']#最浅

plt.style.use('seaborn-v0_8-whitegrid')

if __name__ == "__main__":

    fig, axes = plt.subplots(1, 3, figsize=(8, 3))

    # for i in range(len):
    ax = axes[0]
    # X = np.arange(len)
    # ax.bar(X + 0.3, rgc_tps, width=0.3, label='AERF', hatch='\\\\')
    # ax.bar(X, lru_tps, width=0.3, label='LRU', hatch='//')
    ax.bar([1], datas[0][1], hatch='\\\\\\', label='HC-L', color=colors[0], edgecolor='black')
    ax.bar([2], datas[0][2], hatch='...', label='HC-M', color=colors[1], edgecolor='black')
    ax.bar([3], datas[0][0], hatch='///', label='Hill-Cache', color=colors[2], edgecolor='black')
    ax.set_ylabel('Hit Rate (%)')
    ax.set_title(f'(a) vps26107 (5%)', y=-0.25)
    ax.set_ylim((50, 72))


    ax = axes[1]
    # X = np.arange(len)
    # ax.bar(X + 0.3, rgc_tps, width=0.3, label='AERF', hatch='\\\\')
    # ax.bar(X, lru_tps, width=0.3, label='LRU', hatch='//')
    ax.bar([1], datas[1][1], hatch='\\\\\\', label='HC-L', color=colors[0], edgecolor='black')
    ax.bar([2], datas[1][2], hatch='...', label='HC-M', color=colors[1], edgecolor='black')
    ax.bar([3], datas[1][0], hatch='///', label='Hill-Cache', color=colors[2], edgecolor='black')
    # ax.set_ylabel('Hit Rate (%)')
    ax.set_title(f'(b) webmail (10%)', y=-0.25)
    ax.set_ylim((60, 78))

    ax = axes[2]
    # X = np.arange(len)
    # ax.bar(X + 0.3, rgc_tps, width=0.3, label='AERF', hatch='\\\\')
    # ax.bar(X, lru_tps, width=0.3, label='LRU', hatch='//')
    ax.bar([1], datas[2][1], hatch='\\\\\\', label='HC-L', color=colors[0], edgecolor='black')
    ax.bar([2], datas[2][2], hatch='...', label='HC-M', color=colors[1], edgecolor='black')
    ax.bar([3], datas[2][0], hatch='///', label='Hill-Cache', color=colors[2], edgecolor='black')
    # ax.set_ylabel('Hit Rate (%)')
    ax.set_title(f'(c) prxy_0 (5%)', y=-0.25)
    ax.set_ylim((20, 78))
    plt.tight_layout()
    plt.subplots_adjust(top=0.9)
    ax.legend(loc='upper center', ncol=3, bbox_to_anchor=(-0.80, 1.2), fontsize=12)
    plt.savefig('plots/D4.7/2.eps')
    plt.savefig('plots/D4.7/2.png')

    # sum = 0
    # count = 0
    # for lru, rgc in zip(lru_tps, rgc_tps):
    #     sum += lru / rgc - 1
    #     count += 1
    # print(f'tps: {sum / count * 100}%')
    #
    # sum = 0
    # count = 0
    # for lru, rgc in zip(lru_lat, rgc_lat):
    #     sum += rgc / lru - 1
    #     count += 1
    # print(f'lat: {sum / count * 100}%')
