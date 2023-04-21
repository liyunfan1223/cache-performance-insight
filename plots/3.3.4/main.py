import matplotlib.axes
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

labels = ['ALRFU', 'GLRFU', 'ARC', 'LFU', 'SRRIP']
trace_types = ['OLTP', 'OS Disk', 'ERP', 'Read Skew', 'Read Seq', 'Alter', 'YCSB', 'Overall']
data_overall = [101.49, 97.19, 77.31, 12.07, 16.60]
colors=['r', 'b', 'g', 'y', 'purple']
X = np.arange(8)

# data = {
#     'ALRFU': [43.50, 129.65, 99.78, 139.46, -2.60, 44.29, 0, 101.49,],
#     'GLRFU': [38.17, 120.44, 95.02, 147.64, -11.37, 46.86, 184.30, 97.19,],
#     'ARC': [13.02, 102.46, 87.20, 94.57, 4.10, 49.97, 24.98, 77.31,],
#     'LFU': [-52.93, 16.21, 92.68, 83.70, -94.68, 1.83, 9.90, 12.73,],
#     'SRRIP': [3.67, 23.80, 37.93, 10.15, 3.80, 11.56, 37.51, 16.60,],
# }
# data = {
#     'ALRFU': [4.99, 9.23, 6.34, 13.89, 1.37, 11.65, 0, 9.24],
#     'GLRFU': [2.07, 7.77, 8.23, 15.15, -1.67, 10.94, 1.06, 8.32],
#     'ARC': [3.93, 7.30, 6.35, 9.88, 1.27, 9.99, 0.31, 7.12],
#     'LFU': [-31.96, -9.31, 9.20, 10.13, -572.89, 1.31, -1.42, -45.31],
#     'SRRIP': [1.27, 4.42, 6.28, 4.69, 4.45, 4.55, -0.86, 4.27],
# }
data = {
    'ALRFU': [5.30, 11.51, 7.12, 16.69, 1.70, 13.72, None, None],
    'GLRFU': [2.51, 9.58, 9.85, 18.57, -1.24, 12.66, 1.22, 8.19],
    'ARC': [4.20, 8.37, 7.02, 11.28, 1.39, 11.33, 0.32, 6.39],
    'LFU': [-21.78, -2.00, 11.27, 11.60, -60.67, 1.39, -1.34, -3.20],
    'SRRIP': [1.36, 5.15, 7.81, 5.06, 4.87, 4.91, -0.79, 3.48],
}
# data_overall = {
#     'ALRFU': 101.49,
#     'GLRFU': 97.19,
#     'ARC': 77.31,
#     'LFU': 12.07,
#     'SRRIP': 16.60,
# }

plt.style.use('seaborn')

if __name__ == "__main__":
    # fig = plt.figure()
    # ax = fig.add_axes([0, 0, 1, 1])
    fig, ax = plt.subplots(figsize=(14, 7))
    # axes:matplotlib.axes.Axes = fig.gca()
    # for i, key in enumerate(data_overall.keys()):
    #     ax.bar(l)
    ax.set_xticks(X + 0.4)
    ax.set_xticklabels(trace_types, fontsize=14)
    # ax.xaxis.set_major_locator(ticker.FixedLocator(X + 0.4))
    # ax.xaxis.set_major_formatter(ticker.FixedFormatter(trace_types))
    for i, policy in enumerate(data.keys()):
        hatch = '//' if policy == 'ALRFU' else None
        color = 'white' if policy == 'ALRFU' else colors[i]
        x = []
        y = []
        for idx, d in enumerate(data[policy]):
            if d is None:
                continue
            if (idx >= 6):
                x.append(idx + (i) / 6)
            else:
                x.append(idx + (i + 0.5) / 6)
            y.append(d)
        ax.bar(x, y, color=color, width=1/6,
               label=policy, bottom=0, hatch=hatch, edgecolor=colors[i],)
    ax.set_title('Comparing the Performance of Various Policies and LRU', fontsize=14)
    ax.set_ylabel('Performance higher than LRU (%)', fontsize=14)
    ax.set_ylim(-4.99, 19.99)
    plt.legend()
    plt.savefig('plots/3.3.4/1.png')