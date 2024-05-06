import matplotlib.axes
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import sys
sys.path.append("/home/ubuntu22/cache-performance-insight")

from scripts.utils import SingleTestRunner, MultiTestRunner, BUFFER_LIST_FOR_TRACES, TRACES_LIST

# labels = ['A-LRFU', 'RGC', 'ARC', 'LFU', 'SRRIP']
# trace_types = ['OLTP', 'OS Disk', 'ERP', 'Hotpots', 'Sequential', 'H-S', 'Overall']
# # data_overall = [101.49, 97.19, 77.31, 12.07, 16.60]
# colors = ['#4c90b0', '#55a868', '#c44e52', '#8172b2', '#ccb974', '#86a38d', '#78cbe3', '#757272']
# colors = ['#89aed6', '#8ec98d', '#da9ca3', '#a6adcc', '#e3d5a2', '#aabca5', '#9fd8f0', '#999999']#稍微浅色
colors=['#aec7e8', '#b3e2a1', '#f0abb5', '#c5c7e3', '#f4e5bd', '#c9d8bf', '#c0e1f5', '#c4c4c4']#最浅



hatch_types = ['/', '\\', 'o', '-', '.', 'x', '', '+']
# hatch_types = ['', '', '', '', '', '', '\\', '']

tag="seaborn-v0_8-whitegrid"
plt.style.use(tag)


# hatches = ['//', '\\', '||', '-', '+',]

policies = [ 'LRU', 'LRFU','ARC', 'LIRS', 'DLIRS', 'CACHEUS', 'RGC4', 'OPT']
policies_tag = [ 'LRU', 'LRFU','ARC', 'LIRS', 'DLIRS', 'CACHEUS', 'Hill-Cache', 'OPT']
params = [ None, [1e-5], None, [2], [2], [], [16, 1, 6, 4, 1.0, 20000, 0.5, 0.05, 0.00, 0.01, 1, 1024, 10000], None]
buffer_sizes = [0.001, 0.01, 0.05, 0.1]
buffer_sizes_tag = ['0.1', '1', '5', '10']
# buffer_sizes = [0.0005, 0.001, 0.005]#, 0.01, 0.05, 0.1]

traces = ['cloudvps26107', 'cloudvps26215', 'cloudvps26511','online', 'webusers', 'webmail', 'msr_prn_0', 'msr_prxy_0', 'msr_usr_0',  ]
traces_tag = ['vps26107', 'vps26215', 'vps26511', 'online', 'webusers', 'webmail', 'prn_0', 'prxy_0', 'usr_0',  ]

ylims = [(5, 55), (8, 60)]
bar_width = 1
interval = 1.2
# cmap =
plt.set_cmap(matplotlib.colormaps['viridis'])
n_policy = len(policies)
X = np.arange(len(buffer_sizes))
if __name__ == "__main__":
    fig, axes = plt.subplots(3, 3, figsize=(12, 6.5))

    for i_trace, trace in enumerate(traces):

        ax = axes[i_trace // 3][i_trace % 3]
        ax.set_title(f'{traces_tag[i_trace]}', fontsize=11)
        ax.set_xticks(X * interval + 0.5)
        ax.set_xticklabels(buffer_sizes_tag, fontsize=11)
        if i_trace == 7:
            ax.set_xlabel('Cache size / Footprint size (%)', fontsize=11)
        if i_trace % 3 == 0:
            ax.set_ylabel('Hit Rate (%)', fontsize=11)

        ptrace = 'traces/' + trace + '.lis'
        hit_rates = []
        cur_x = 0

        for i, (policy, param) in enumerate(zip(policies, params)):
            x = []
            y = []
            for idx, buffer_size in enumerate(buffer_sizes):
                runner = SingleTestRunner(policy, buffer_size, ptrace, param)
                hr = runner.get_hit_rate()
                hit_rates.append(hr)
                cur_x += bar_width
                x.append(idx * interval + (i + 0.5) / n_policy)
                y.append(hr)
            print(x, y)
            color = None
            ax.bar(x, y, width=1/n_policy * 0.7, label=policies_tag[i], bottom=0, linewidth=1, color=colors[i], hatch=hatch_types[i]*3, edgecolor='black')
        #子图之间如果要比较的话加上下面这句
        if i_trace not in [2,3,4,6,7,8]:
            ax.set_ylim(0, 85)
            print("##########################################")
        #         elif i_trace in [7]:
        #             ax.set_ylim(0, 100)
        #             print("##########################################")
        # plt.legend()
        # fig.tight_layout(h_pad=1.0, w_pad=0.0)
        # 只显示横向的网格线
        ax.grid(axis='x')
    print(f'Generate plots/D4.1/1d.png')
    # plt.subplots_adjust(hspace=0.2)
    plt.tight_layout()
    plt.subplots_adjust(top=0.92, right=1)
    # plt.suptitle('Cache Size / Footprint Size(%)')
    # plt.legend(loc='upper center', ncol=len(policies_tag), bbox_to_anchor=(-0.75, 4.3))
    plt.legend(loc='upper center', ncol=len(policies_tag), bbox_to_anchor=(-0.72, 4.15))
    # plt.tight_layout()

    fig.savefig(f'plots/D4.1/1d.png')
    fig.savefig(f'plots/D4.1/1d.eps')
#     fig.savefig('1c-{}.png'.format(tag))
#     fig.savefig('1c-{}.eps'.format(tag))