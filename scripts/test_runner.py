#!/usr/bin/env python3
import os
import matplotlib.pyplot as plt
from utils import SingleTestRunner, MultiTestRunner, TRACES_LIST

# CACHE_POLICY_LIST = [
#     'LRU'
# ]
MIN_BUFFER_SIZE = 11
MAX_BUFFER_SIZE = 18
BUFFER_SIZE_LIST = [2 ** k for k in range(MIN_BUFFER_SIZE, MAX_BUFFER_SIZE + 1)]

TRACE_FILE_LIST = [
    'P1',
]

if __name__ == '__main__':
    print(f'Start run tests. Trace file: {TRACE_FILE_LIST}. Buffer size list: {BUFFER_SIZE_LIST}')
    for trace in TRACE_FILE_LIST:
        trace_file = f'traces/{trace}.lis'
        fig, ax = plt.subplots(figsize=(14, 7))
        ax.set_xlim(BUFFER_SIZE_LIST[0] // 2, BUFFER_SIZE_LIST[-1] * 2)
        ax.set_xticks(BUFFER_SIZE_LIST)
        ax.set_xticklabels(BUFFER_SIZE_LIST)
        ax.set_xlabel('Buffer Size')
        ax.set_ylabel('Hit Ratio(%)')
        ax.set_title(trace_file)

        # lru_runner = MultiTestRunner(['LRU'], BUFFER_SIZE_LIST, trace_file, None)
        # lru_result = lru_runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, lru_result, label='LRU', marker='+', linestyle=':')

        # lfu_runner = MultiTestRunner(['LFU'], BUFFER_SIZE_LIST, TRACE_FILE_LIST, [None] * len(BUFFER_SIZE_LIST))
        # lfu_result = lfu_runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, lfu_result, label='LFU')

        # arc_runner = MultiTestRunner(['ARC'], BUFFER_SIZE_LIST, trace_file, None)
        # arc_result = arc_runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, arc_result, label='ARC', marker='+', linestyle='dashed')

        # params_list = [5]
        # stw_runner = MultiTestRunner(['STW'], BUFFER_SIZE_LIST, trace_file, params_list)
        # stw_result = stw_runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, stw_result, label=f'STW, k={params_list[0]}', marker='+', linestyle='-')
        #
        # params_list = [20]
        # stw_runner = MultiTestRunner(['STW'], BUFFER_SIZE_LIST, trace_file, params_list)
        # stw_result = stw_runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, stw_result, label=f'STW, k={params_list[0]}', marker='+', linestyle='-')

        params_list = [1]
        srrip_runner = MultiTestRunner(['SRRIP'], BUFFER_SIZE_LIST, trace_file, params_list)
        srrip_result = srrip_runner.get_hit_rate_list()
        ax.plot(BUFFER_SIZE_LIST, srrip_result, label=f'SRRIP, m={params_list[0]}', marker='+', linestyle='dashed')

        params_list = [2]
        srrip_runner = MultiTestRunner(['SRRIP'], BUFFER_SIZE_LIST, trace_file, params_list)
        srrip_result = srrip_runner.get_hit_rate_list()
        ax.plot(BUFFER_SIZE_LIST, srrip_result, label=f'SRRIP, m={params_list[0]}', marker='+', linestyle='dashed')

        params_list = [3]
        srrip_runner = MultiTestRunner(['SRRIP'], BUFFER_SIZE_LIST, trace_file, params_list)
        srrip_result = srrip_runner.get_hit_rate_list()
        ax.plot(BUFFER_SIZE_LIST, srrip_result, label=f'SRRIP, m={params_list[0]}', marker='+', linestyle='dashed')

        # params_list = [200]
        # stw_runner = MultiTestRunner(['STW'], BUFFER_SIZE_LIST, trace_file, params_list)
        # stw_result = stw_runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, stw_result, label=f'STW, k={params_list[0]}', marker='+', linestyle='-')


        # params_list = [20]
        # stw2_runner = MultiTestRunner(['STW2'], BUFFER_SIZE_LIST, trace_file, params_list)
        # stw2_result = stw2_runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, stw2_result, label=f'STW2, k={params_list[0]}', marker='+', linestyle='-')

        # mrf_runner = MultiTestRunner(['MRF'], BUFFER_SIZE_LIST, trace_file, None)
        # mrf_result = mrf_runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, mrf_result, label='MRF*', marker='+', linestyle='-.')

        # opt_runner = MultiTestRunner(['OPT'], BUFFER_SIZE_LIST, trace_file, None)
        # opt_result = opt_runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, opt_result, label='OPT*', marker='+', linestyle='-.')

        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_yticks([2, 4, 8, 16, 32, 64, 100])
        ax.set_yticklabels([2, 4, 8, 16, 32, 64, ''])
        ax.set_ylim(0.5, 100)
        ax.set_xticks(BUFFER_SIZE_LIST)
        ax.set_xticklabels(BUFFER_SIZE_LIST)
        ax.set_xlim(BUFFER_SIZE_LIST[0] // 2, BUFFER_SIZE_LIST[-1] * 2)
        plt.legend(loc=2)
        if not os.path.exists('local'):
            os.mkdir('local')
        # fig_path = f'local/plot_{trace}.png'
        fig_path = 'local/plot.png'
        plt.savefig(fig_path)
        print(f'Fig generated path: {fig_path}. ')
