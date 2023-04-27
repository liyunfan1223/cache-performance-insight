import matplotlib.axes
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

labels = ['A-LRFU', 'RGC', 'ARC', 'LFU', 'SRRIP']
trace_types = ['OLTP', 'OS Disk', 'ERP', 'Hotpots', 'Sequential', 'H-S', 'Overall']
# data_overall = [101.49, 97.19, 77.31, 12.07, 16.60]
colors=['r', 'b', 'g', 'y', 'purple']
X = np.arange(7)

"""
DS1
Performance rate of LFU: 16.055799756916503% average higher than lru.
Performance rate of SRRIP: 14.322847627488175% average higher than lru.
Performance rate of ARC: 10.859251895544181% average higher than lru.
Performance rate of A-LRFU: 14.018522372049569% average higher than lru.
Performance rate of RGC: 15.92908455706928% average higher than lru.
OLTP
Performance rate of LFU: -21.78926246434558% average higher than lru.
Performance rate of SRRIP: 1.3676911143467383% average higher than lru.
Performance rate of ARC: 4.206246025219573% average higher than lru.
Performance rate of A-LRFU: 5.307867936591788% average higher than lru.
Performance rate of RGC: 2.510720676392896% average higher than lru.
P
Performance rate of LFU: -2.0044724578575024% average higher than lru.
Performance rate of SRRIP: 5.152130264834779% average higher than lru.
Performance rate of ARC: 8.373715071739325% average higher than lru.
Performance rate of A-LRFU: 11.512516893627678% average higher than lru.
Performance rate of RGC: 9.58536295567872% average higher than lru.
Performance rate of OPT: 38.04929073778998% average higher than lru.
Hotpots
Performance rate of LFU: 11.60398679181312% average higher than lru.
Performance rate of SRRIP: 5.06944084824271% average higher than lru.
Performance rate of ARC: 11.284070279507452% average higher than lru.
Performance rate of A-LRFU: 16.696653757491408% average higher than lru.
Performance rate of RGC: 18.571407037390575% average higher than lru.
Performance rate of OPT: 44.90767955659087% average higher than lru.
Sequential
Performance rate of LFU: -60.67818467442766% average higher than lru.
Performance rate of SRRIP: 4.878089620205224% average higher than lru.
Performance rate of ARC: 1.3904803086388238% average higher than lru.
Performance rate of A-LRFU: 1.7048203838827227% average higher than lru.
Performance rate of RGC: -1.2405186257641003% average higher than lru.
Performance rate of OPT: 51.54282271252566% average higher than lru.
H-S
Performance rate of LFU: 1.3900574668865704% average higher than lru.
Performance rate of SRRIP: 4.913861644660482% average higher than lru.
Performance rate of ARC: 11.33684073555821% average higher than lru.
Performance rate of A-LRFU: 13.72241649488386% average higher than lru.
Performance rate of RGC: 12.669197566173102% average higher than lru.
Performance rate of OPT: 45.553242652438286% average higher than lru.
"""

data = {
    'A-LRFU': [5.30, 11.51, 7.12, 16.69, 1.70, 13.72, 11.75],
    'RGC': [2.51, 9.58, 9.85, 18.57, -1.24, 12.66, 10.77],
    'ARC': [4.20, 8.37, 7.02, 11.28, 1.39, 11.33, 8.53],
    'LFU': [-21.78, -2.00, 11.27, 11.60, -60.67, 1.39, -3.29],
    'SRRIP': [1.36, 5.15, 7.81, 5.06, 4.87, 4.91, 5.27],
}

plt.style.use('seaborn-v0_8-paper')

hatches = ['//', '\\', '||', '-', '+',]

if __name__ == "__main__":
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_xticks(X + 0.4)
    ax.set_xticklabels(trace_types, fontsize=14)
    for i, policy in enumerate(data.keys()):
        hatch = hatches[i]
        color = colors[i]
        x = []
        y = []
        for idx, d in enumerate(data[policy]):
            if d is None:
                continue
            x.append(idx + (i + 0.5) / 6)
            y.append(d)
        ax.bar(x, y, color='white', width=1/6,
               label=policy, bottom=0, hatch=hatch, edgecolor=color, linewidth = 1)
    # ax.set_title('Comparing the Performance of Various Policies and LRU', fontsize=14)
    ax.set_ylabel('Miss ratio lower than LRU (%)', fontsize=14)
    ax.set_ylim(-4.99, 19.99)
    plt.legend()
    plt.savefig('plots/3.3.4/1.png')