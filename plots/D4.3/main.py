import matplotlib.axes
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import sys
sys.path.append("/home/ubuntu22/cache-performance-insight")
from scripts.utils import SingleTestRunner, MultiTestRunner, BUFFER_LIST_FOR_TRACES, TRACES_LIST, StatisticsCompareLRU

plt.style.use('seaborn-v0_8-paper')

def gen():
    policies = ['ARC', 'LIRS', 'DLIRS', 'CACHEUS', 'RGC4', 'RGC4', 'RGC4', 'RGC4']
    policies_tag = ['ARC', 'LIRS', 'DLIRS', 'CACHEUS', 'AERF-naive', 'AERF-M', 'AERF-G', 'AERF']
    sizes = [0.001, 0.01, 0.05, 0.1]
    params = [None, [2], [2], [],
              [16, 1, 6, 0, 1.0, 20000, 0.5, 0.05, 0.00, 0.01, 1, -1, 10000],
              [16, 1, 6, 0, 1.0, 20000, 0.5, 0.05, 0.00, 0.01, 1, 1024, 10000],
              [16, 1, 6, 4, 1.0, 20000, 0.5, 0.05, 0.00, 0.01, 1, -1, 10000],
              [16, 1, 6, 4, 1.0, 20000, 0.5, 0.05, 0.00, 0.01, 1, 1024, 10000]]
    all_data = {}
    for policy in policies_tag:
        all_data[policy] = []

    for trace in TRACES_LIST:
        for size in sizes:
            trace_path = f'traces/{trace}.lis'
            lru_runner = SingleTestRunner('LRU', size, trace_path, None)
            lru_result = lru_runner.get_hit_rate()

            for policy, param, policy_tag in zip(policies, params, policies_tag):
                runner = SingleTestRunner(policy, size, trace_path, param)
                result = runner.get_hit_rate()

                stats = StatisticsCompareLRU()
                stats.statistic([lru_result], [result])
                perf = stats.perf['default']
                all_data[policy_tag].append(perf * 100)

    datas = []
    for policy in policies_tag:
        datas.append(all_data[policy])
    # print(all_data)
    # print(datas)

    # fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(9, 4))
    fig, ax = plt.subplots(figsize=(10, 4))
    # ax.set_ylim((-15, 15))
    # rectangular box plot
    # bplot1 = ax1.boxplot(all_data,
    #                      vert=True,  # vertical box alignment
    #                      patch_artist=True,  # fill with color
    #                      labels=labels)  # will be used to label x-ticks
    # ax1.set_title('Rectangular box plot')

    # notch shape box plot
    # bplot2 = ax2.boxplot(all_data,
    #                      notch=True,  # notch shape
    #                      vert=True,  # vertical box alignment
    #                      patch_artist=True,  # fill with color
    #                      labels=labels)  # will be used to label x-ticks
    # ax2.set_title('Notched box plot')

    # fill with colors
    # colors = ['pink', 'lightblue', 'lightgreen']
    # for bplot in (bplot1, bplot2):
    #     for patch, color in zip(bplot['boxes'], colors):
    #         patch.set_facecolor(color)

    # adding horizontal grid lines
    # for ax in [ax1, ax2]:
    #     ax.yaxis.grid(True)
    #     ax.set_xlabel('Three separate samples')
    #     ax.set_ylabel('Observed values')

    # ax.violinplot(datas,
    #               showmeans=False,
    #               showextrema=False,
    #               showmedians=True)
    bplot = ax.boxplot(datas,
               notch=True,  # notch shape
               vert=True,  # vertical box alignment
               patch_artist=True,  # fill with color
               showfliers=False,
               labels=policies_tag,
               medianprops={'color': 'black'},
               showmeans=True,
               meanline=True,
               meanprops={'color': 'black'},
               # whis=1.0)
               whis=(5, 95))  # will be used to label x-ticks
    # fill with colors
    colors = ['#c44e52', '#8172b2', '#ccb974', '#86a38d', '#4c90b0', '#55a868', '#757272', '#78cbe3']

    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)
    ax.yaxis.grid(True)
    ax.xaxis.grid(False)
    # ax.spines['top'].set_visible(True)
    # ax.spines['top'].set_linewidth(2)
    # ax.spines['right'].set_visible(True)
    ax.set_ylabel('Miss Rate lower than LRU(%)', fontsize=14)
    ax.tick_params(axis='x', labelsize=14)
    ax.tick_params(axis='y', labelsize=14)
    ax.set_ylim((-15, 48))
    # ax.set_xlabel()
    # ax.legend()
    fig.tight_layout()
    plt.savefig('plots/D4.3/1.png', format='png')
    plt.savefig('plots/D4.3/1.eps', format='eps')


if __name__ == "__main__":
    gen()
