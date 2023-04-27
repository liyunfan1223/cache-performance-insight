#!/usr/bin/env python
import os
import matplotlib.pyplot as plt
from scripts.utils import SingleTestRunner, MultiTestRunner, TRACES_LIST, BUFFER_LIST_FOR_TRACES, StatisticsCompareLRU

plt.style.use('seaborn-paper')
# CACHE_POLICY_LIST = [
#     'LRU'
# ]
MIN_BUFFER_SIZE = 11
MAX_BUFFER_SIZE = 18
BUFFER_SIZE_LIST = [2 ** k for k in range(MIN_BUFFER_SIZE, MAX_BUFFER_SIZE + 1)]

SUFFIX = '417'
TRACE_FILE_LIST = [
    'P1',
]
markers = ['o', 's', 'v', '^']
stats = StatisticsCompareLRU()

def P1():
    print(f'Start run tests. Trace file: {TRACES_LIST}.')
    for trace in ["P1"]:
        BUFFER_SIZE_LIST = BUFFER_LIST_FOR_TRACES[trace]
        trace_file = f'traces/{trace}.lis'
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.set_xlim(BUFFER_SIZE_LIST[0] // 2, BUFFER_SIZE_LIST[-1] * 2)
        ax.set_xticks(BUFFER_SIZE_LIST)
        ax.set_xticklabels(BUFFER_SIZE_LIST)
        ax.set_xlabel('Buffer Size')
        ax.set_ylabel('Hit Ratio(%)', fontsize=12)
        ax.set_title("P1")

        lru_runner = MultiTestRunner(['LRU'], BUFFER_SIZE_LIST, trace_file, None)
        lru_result = lru_runner.get_hit_rate_list()
        ax.plot(BUFFER_SIZE_LIST, lru_result, label='LRU', marker='o', linestyle=':', color='black')

        lfu_runner = MultiTestRunner(['LFU'], BUFFER_SIZE_LIST, trace_file, None)
        lfu_result = lfu_runner.get_hit_rate_list()
        ax.plot(BUFFER_SIZE_LIST, lfu_result, label='LFU', marker='s', linestyle='dashed', color='y')
        stats.statistic(lru_result, lfu_result, "LFU")

        srrip_runner = MultiTestRunner(['SRRIP'], BUFFER_SIZE_LIST, trace_file, None)
        srrip_result = srrip_runner.get_hit_rate_list()
        ax.plot(BUFFER_SIZE_LIST, srrip_result, label='SRRIP', marker='v', linestyle='dashed', color='purple')
        stats.statistic(lru_result, srrip_result, "SRRIP")

        arc_runner = MultiTestRunner(['ARC'], BUFFER_SIZE_LIST, trace_file, None)
        arc_result = arc_runner.get_hit_rate_list()
        ax.plot(BUFFER_SIZE_LIST, arc_result, label='ARC', marker='^', linestyle='dashed', color='g')
        stats.statistic(lru_result, arc_result, "ARC")

        params_list = [20000, 5, 0.1, 5, -1, 1, 1]
        runner = MultiTestRunner(['ALRFU5'], BUFFER_SIZE_LIST, trace_file, params_list)
        alrfu_result = runner.get_hit_rate_list()
        ax.plot(BUFFER_SIZE_LIST, alrfu_result, label=f'A-LRFU', marker='d', linestyle='-', color='r')
        stats.statistic(lru_result, alrfu_result, "A-LRFU")


        params_list = [20000, 20, 0.5, 5, 4, 10, 4]
        runner = MultiTestRunner(['GLRFU2'], BUFFER_SIZE_LIST, trace_file, params_list)
        glrfu2_e_result = runner.get_hit_rate_list()
        ax.plot(BUFFER_SIZE_LIST, glrfu2_e_result, label=f'RGC', marker='X', linestyle='-', color='b')
        stats.statistic(lru_result, glrfu2_e_result, "RGC")

        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_yticks([2, 4, 8, 16, 32, 64, 100])
        ax.set_yticklabels([2, 4, 8, 16, 32, 64, ''])
        ax.set_ylim(0.5, 100)
        ax.set_xticks(BUFFER_SIZE_LIST)
        ax.set_xticklabels(BUFFER_SIZE_LIST)
        ax.set_xlim(BUFFER_SIZE_LIST[0] // 2, BUFFER_SIZE_LIST[-1] * 2)
        plt.legend(loc=4)
        if not os.path.exists('local'):
            os.mkdir('local')
        fig_path = f'plots/3.3.4/2.png'
        plt.savefig(fig_path)
        print(f'Fig generated path: {fig_path}. ')
        stats.print_result()

def OLTP():
    print(f'Start run tests. Trace file: {TRACES_LIST}.')
    for trace in ["OLTP"]:
        BUFFER_SIZE_LIST = [2 ** k for k in range(5, 11 + 1)]
        # BUFFER_SIZE_LIST = [1000, 2000, 5000, 10000, 15000]
        trace_file = f'traces/{trace}.lis'
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.set_xlim(BUFFER_SIZE_LIST[0] // 2, BUFFER_SIZE_LIST[-1] * 2)
        ax.set_xticks(BUFFER_SIZE_LIST)
        ax.set_xticklabels(BUFFER_SIZE_LIST)
        ax.set_xlabel('Buffer Size')
        ax.set_ylabel('Hit Ratio(%)', fontsize=12)
        ax.set_title("OLTP")

        lru_runner = MultiTestRunner(['LRU'], BUFFER_SIZE_LIST, trace_file, None)
        lru_result = lru_runner.get_hit_rate_list()
        ax.plot(BUFFER_SIZE_LIST, lru_result, label='LRU', marker='o', linestyle=':', color='black')

        lfu_runner = MultiTestRunner(['LFU'], BUFFER_SIZE_LIST, trace_file, None)
        lfu_result = lfu_runner.get_hit_rate_list()
        ax.plot(BUFFER_SIZE_LIST, lfu_result, label='LFU', marker='s', linestyle='dashed', color='y')
        stats.statistic(lru_result, lfu_result, "LFU")

        srrip_runner = MultiTestRunner(['SRRIP'], BUFFER_SIZE_LIST, trace_file, None)
        srrip_result = srrip_runner.get_hit_rate_list()
        ax.plot(BUFFER_SIZE_LIST, srrip_result, label='SRRIP', marker='v', linestyle='dashed', color='purple')
        stats.statistic(lru_result, srrip_result, "SRRIP")

        arc_runner = MultiTestRunner(['ARC'], BUFFER_SIZE_LIST, trace_file, None)
        arc_result = arc_runner.get_hit_rate_list()
        ax.plot(BUFFER_SIZE_LIST, arc_result, label='ARC', marker='^', linestyle='dashed', color='g')
        stats.statistic(lru_result, arc_result, "ARC")

        params_list = [20000, 5, 0.1, 5, -1, 1, 1]
        runner = MultiTestRunner(['ALRFU5'], BUFFER_SIZE_LIST, trace_file, params_list)
        alrfu_result = runner.get_hit_rate_list()
        ax.plot(BUFFER_SIZE_LIST, alrfu_result, label=f'A-LRFU', marker='d', linestyle='-', color='r')
        stats.statistic(lru_result, alrfu_result, "A-LRFU")


        params_list = [20000, 20, 0.5, 5, 4, 10, 4]
        runner = MultiTestRunner(['GLRFU2'], BUFFER_SIZE_LIST, trace_file, params_list)
        glrfu2_e_result = runner.get_hit_rate_list()
        ax.plot(BUFFER_SIZE_LIST, glrfu2_e_result, label=f'RGC', marker='X', linestyle='-', color='b')
        stats.statistic(lru_result, glrfu2_e_result, "RGC")

        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_yticks([2, 4, 8, 16, 32, 64, 100])
        ax.set_yticklabels([2, 4, 8, 16, 32, 64, ''])
        ax.set_ylim(0.5, 100)
        ax.set_xticks(BUFFER_SIZE_LIST)
        ax.set_xticklabels(BUFFER_SIZE_LIST)
        ax.set_xlim(BUFFER_SIZE_LIST[0] // 2, BUFFER_SIZE_LIST[-1] * 2)
        plt.legend(loc=4)
        if not os.path.exists('local'):
            os.mkdir('local')
        fig_path = f'plots/3.3.4/3.png'
        plt.savefig(fig_path)
        print(f'Fig generated path: {fig_path}. ')
        stats.print_result()

if __name__ == "__main__":
    P1()
    OLTP()