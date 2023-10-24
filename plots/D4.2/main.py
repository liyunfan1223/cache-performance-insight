import matplotlib.axes
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import sys
from scipy.interpolate import make_interp_spline
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
params = [None, None, None, [2], [2], [], [16, 1, 6, 4, 1.0, 20000, 0.5, 0.05, 0.00, 0.05, 1, 1024, 10000], None]
buffer_sizes = [0.001, 0.01, 0.05, 0.1]
buffer_sizes_tag = ['0.1%', '1%', '5%', '10%']
# buffer_sizes = [0.0005, 0.001, 0.005]#, 0.01, 0.05, 0.1]

traces = ['online', 'webusers', 'webmail', 'cloudvps26107', 'cloudvps26215', 'cloudvps26511', 'msr_prn_0', 'msr_ts_0', 'msr_usr_0']
traces_tag = ['Online', 'Webusers', 'Webmail', 'CloudVPS26107', 'CloudVPS26215', 'CloudVPS26511', 'MSR_prn', 'MSR_ts', 'MSR_usr']
"""format: ct: 1 reality: 6.56 simulator: 6.56 r_cur_half: 1.00000000 31 1"""

start_line_n = 2
record_n = 15975
# down_sample_group_size = 500

# def GetHitRateAndParam(file_path):
#     hrs = []
#     ps = []
#     with open(file_path, 'r') as f:
#         lines = f.readlines()[start_line_n: start_line_n + record_n]
#         for line in lines:
#             # print(line.strip().split(' '))
#             _, _, _, hr, _, _, _, p, _, _ = line.strip().split(' ')
#             # print(hr, p)
#             hrs.append(float(hr))
#             ps.append(float(p))
#     dhrs = []
#     dps = []
#
#     tsum_hr = 0
#     tsum_p = 0
#     for idx, (hr, p) in enumerate(zip(hrs, ps)):
#         if (idx + 1) % down_sample_group_size == 0:
#             dhrs.append(tsum_hr / down_sample_group_size)
#             dps.append(tsum_p / down_sample_group_size)
#             tsum_hr = 0
#             tsum_p = 0
#         tsum_p += p
#         tsum_hr += hr
#     return dhrs, dps

def RunAndGetHitRateAndParam(policy, buffer_size, ptrace, param):
    runner = SingleTestRunner(policy, buffer_size, ptrace, param, execution_path='./build/src/main_log')
    lines = runner.get_outputs().split('\n')
    hrs = []
    ps = []
    # with open(file_path, 'r') as f:
    lines = lines[2: -1]
    for line in lines:
        print(line)
        _, _, _, hr, _, _, _, p, _, _ = line.strip().split(' ')
        hrs.append(float(hr))
        ps.append(float(p))
    dhrs = [0]
    dps = [param[0]]

    tsum_hr = 0
    tsum_p = 0

    down_sample_group_size = 100
    for idx, (hr, p) in enumerate(zip(hrs, ps)):
        if (idx + 1) % down_sample_group_size == 0:
            dhrs.append(tsum_hr / down_sample_group_size)
            dps.append(tsum_p / down_sample_group_size)
            tsum_hr = 0
            tsum_p = 0
        tsum_p += p
        tsum_hr += hr
    return dhrs, dps

total_size = 2000
buffer_size = 0.001
trace = 'proj_prxy'
p1 = [1, 1, 6, 4, 1.0, 20000, 0.5, 0.05, 0.00, 0.01, 1, 1024, 10000]
p2 = [1, 1, 6, 4, 1.0, 20000, 0.5, 0.05, 0.00, 0.00, 1, 1024, 10000]
p3 = [64, 1, 6, 4, 1.0, 20000, 0.5, 0.05, 0.00, 0.00, 1, 1024, 10000]

if __name__ == "__main__":
    # sim_hrs, sim_ps = GetHitRateAndParam('local/webmail_0.001_sim.log')
    sim_hrs, sim_ps = RunAndGetHitRateAndParam('RGC4', buffer_size, f'traces/{trace}.lis', p1)
    nosim_hrs, nosim_ps = RunAndGetHitRateAndParam('RGC4', buffer_size, f'traces/{trace}.lis', p2)
    nosim_hrs2, nosim_ps2 = RunAndGetHitRateAndParam('RGC4', buffer_size, f'traces/{trace}.lis', p3)
    # nosim_hrs, nosim_ps = GetHitRateAndParam('local/webmail_0.001_nosim.log')

    X = np.arange(len(sim_hrs))
    # print(X, len(sim_hrs), down_sample_group_size)
    fig, axes = plt.subplots(2, 1, figsize=(12, 6))

    ax = axes[0]
    ax.plot(X, sim_hrs, label='sim')

    ax.plot(X, nosim_hrs, label='nosim')
    ax.plot(X, nosim_hrs2, label='nosim2')
    # plt.legend()
    # plt.savefig(f'plots/D4.2/{trace}_1.png')

    ax = axes[1]
    # fig, ax = plt.subplots(figsize=(8, 5))

    # spl = make_interp_spline(X, sim_ps)
    # sim_ps_smooth = spl(x_smooth)
    # ax.plot(x_smooth, sim_ps_smooth, label='sim')
    ax.plot(X, sim_ps, label='sim')

    # spl = make_interp_spline(X, nosim_ps)
    # nosim_ps_smooth = spl(x_smooth)
    # ax.plot(x_smooth, nosim_ps_smooth, label='nosim')
    ax.plot(X, nosim_ps, label='nosim')
    ax.plot(X, nosim_ps2, label='nosim2')
    plt.legend()
    plt.savefig(f'plots/D4.2/{trace}_2.png')

    #
    # fig.tight_layout(h_pad=1.5, w_pad=0.0)
    # # plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
    # for i_trace, trace in enumerate(traces):
    #     ax = axes[i_trace // 3][i_trace % 3]
    #     ax.set_title(f'{traces_tag[i_trace]}', fontsize=10)
    #     ax.set_xticks(X * interval + 0.5)
    #     ax.set_xticklabels(buffer_sizes_tag, fontsize=10)
    #     # fig.set_label('Cache Size / Workload Size')
    #     ax.set_ylabel('Hit Rate(%)', fontsize=10)
    #     # if i_trace < len(ylims):
    #     #     ax.set_ylim(ylims[i_trace][0], ylims[i_trace][1])
    #
    #     ptrace = 'traces/' + trace + '.lis'
    #     hit_rates = []
    #     cur_x = 0
    #     for i, (policy, param) in enumerate(zip(policies, params)):
    #         x = []
    #         y = []
    #         for idx, buffer_size in enumerate(buffer_sizes):
    #             runner = SingleTestRunner(policy, buffer_size, ptrace, param)
    #             hr = runner.get_hit_rate()
    #             hit_rates.append(hr)
    #             cur_x += bar_width
    #             x.append(idx * interval + (i + 0.5) / n_policy)
    #             y.append(hr)
    #         print(x, y)
    #         color = None
    #         ax.bar(x, y, width=1/n_policy, label=policies_tag[i], bottom=0, linewidth=1, color=colors[i])
    #     # plt.legend()
    # print(f'Generate plots/D4.1/1.png')
    # # plt.legend(bbox_to_anchor=(0, -0.1), ncol=len(policies_tag))
    # # plt.subplots_adjust(hspace=0.2)
    # fig.savefig(f'plots/D4.1/1.png')
    #
    # # for i, policy in enumerate(data.keys()):
    # #     hatch = hatches[i]
    # #     color = colors[i]
    # #     x = []
    # #     y = []
    # #     for idx, d in enumerate(data[policy]):
    # #         if d is None:
    # #             continue
    # #         x.append(idx + (i + 0.5) / 6)
    # #         y.append(d)
    # #     ax.bar(x, y, color='white', width=1/6,
    # #            label=policy, bottom=0, hatch=hatch, edgecolor=color, linewidth = 1)
    # # # ax.set_title('Comparing the Performance of Various Policies and LRU', fontsize=14)
    # # ax.set_ylabel('Miss ratio lower than LRU (%)', fontsize=14)
    #


