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
colors = ['#4c90b0', '#55a868', '#c44e52', '#8172b2', '#ccb974', '#86a38d', '#78cbe3', '#757272']
#556c68
# colors = ['g']
# X = np.arange(7)


plt.style.use('seaborn-v0_8')

hatches = ['//', '\\', '||', '-', '+',]

policies = ['LFU', 'LRU', 'ARC', 'LIRS', 'DLIRS', 'CACHEUS', 'RGC4', 'OPT']
policies_tag = ['LFU', 'LRU', 'ARC', 'LIRS', 'DLIRS', 'CACHEUS', 'RGC', 'OPT']
params = [None, None, None, [2], [2], [], [16, 1, 6, 4, 1.0, 20000, 0.5, 0.05, 0.00, 0.01, 1, 1024, 10000], None]
buffer_sizes = [0.001, 0.01, 0.05, 0.1]
buffer_sizes_tag = ['0.1%', '1%', '5%', '10%']
# buffer_sizes = [0.0005, 0.001, 0.005]#, 0.01, 0.05, 0.1]

traces = ['online', 'webusers', 'webmail', 'cloudvps26107', 'cloudvps26215', 'cloudvps26511', 'msr_prn_0', 'msr_ts_0', 'msr_usr_0']
traces_tag = ['Online', 'Webusers', 'Webmail', 'CloudVPS26107', 'CloudVPS26215', 'CloudVPS26511', 'MSR_prn', 'MSR_ts', 'MSR_usr']

ylims = [(5, 55), (8, 60)]
bar_width = 1
interval = 1.1
# cmap =
plt.set_cmap(matplotlib.colormaps['viridis'])
n_policy = len(policies)
X = np.arange(len(buffer_sizes))
if __name__ == "__main__":
    fig, axes = plt.subplots(3, 3, figsize=(8, 5))


    # plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
    for i_trace, trace in enumerate(traces):
        ax = axes[i_trace // 3][i_trace % 3]
        ax.set_title(f'{traces_tag[i_trace]}', fontsize=10)
        ax.set_xticks(X * interval + 0.5)
        ax.set_xticklabels(buffer_sizes_tag, fontsize=10)
        # fig.set_label('Cache Size / Workload Size')
        ax.set_ylabel('Hit Rate(%)', fontsize=10)
        # if i_trace < len(ylims):
        #     ax.set_ylim(ylims[i_trace][0], ylims[i_trace][1])

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
            ax.bar(x, y, width=1/n_policy, label=policies_tag[i], bottom=0, linewidth=1, color=colors[i])
        # plt.legend()
    fig.tight_layout(h_pad=1.0, w_pad=0.0)

    print(f'Generate plots/D4.1/1.png')
    # plt.legend(bbox_to_anchor=(0, -0.1), ncol=len(policies_tag))
    # plt.subplots_adjust(hspace=0.2)
    fig.savefig(f'plots/D4.1/1.png')
    fig.savefig(f'plots/D4.1/1.eps')

    # for i, policy in enumerate(data.keys()):
    #     hatch = hatches[i]
    #     color = colors[i]
    #     x = []
    #     y = []
    #     for idx, d in enumerate(data[policy]):
    #         if d is None:
    #             continue
    #         x.append(idx + (i + 0.5) / 6)
    #         y.append(d)
    #     ax.bar(x, y, color='white', width=1/6,
    #            label=policy, bottom=0, hatch=hatch, edgecolor=color, linewidth = 1)
    # # ax.set_title('Comparing the Performance of Various Policies and LRU', fontsize=14)
    # ax.set_ylabel('Miss ratio lower than LRU (%)', fontsize=14)

    # plt.legend()
    # plt.savefig('plots/3.3.4/1.png')

