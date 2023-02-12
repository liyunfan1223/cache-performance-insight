#!/usr/bin/env python
import os
import matplotlib.pyplot as plt
from utils import SingleTestRunner, MultiTestRunner, TRACES_LIST

# CACHE_POLICY_LIST = [
#     'LRU'
# ]
MIN_BUFFER_SIZE = 6
MAX_BUFFER_SIZE = 13
BUFFER_SIZE_LIST = [2 ** k for k in range(MIN_BUFFER_SIZE, MAX_BUFFER_SIZE + 1)]

TRACE_FILE_LIST = [
    'Home1',
    'Home2',
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

        lru_runner = MultiTestRunner(['LRU'], BUFFER_SIZE_LIST, trace_file, None)
        lru_result = lru_runner.get_hit_rate_list()
        ax.plot(BUFFER_SIZE_LIST, lru_result, label='LRU', marker='+', linestyle=':')

        # lfu_runner = MultiTestRunner(['LFU'], BUFFER_SIZE_LIST, trace_file, [None])
        # lfu_result = lfu_runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, lfu_result, label='LFU', marker='+', linestyle=':')

        arc_runner = MultiTestRunner(['ARC'], BUFFER_SIZE_LIST, trace_file, None)
        arc_result = arc_runner.get_hit_rate_list()
        ax.plot(BUFFER_SIZE_LIST, arc_result, label='ARC', marker='+', linestyle='dashed')

        # params_list = [1e-6]
        # runner = MultiTestRunner(['LRFU'], BUFFER_SIZE_LIST, trace_file, params_list)
        # result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, result, label=f'LRFU p={params_list}', marker='+', linestyle='-')
        # params_list = [1e-4]
        # runner = MultiTestRunner(['LRFU'], BUFFER_SIZE_LIST, trace_file, params_list)
        # result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, result, label=f'LRFU p={params_list}', marker='+', linestyle='-')
        # params_list = [1e-2]
        # runner = MultiTestRunner(['LRFU'], BUFFER_SIZE_LIST, trace_file, params_list)
        # result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, result, label=f'LRFU p={params_list}', marker='+', linestyle='-')
        # params_list = [1]
        # runner = MultiTestRunner(['LRFU'], BUFFER_SIZE_LIST, trace_file, params_list)
        # result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, result, label=f'LRFU p={params_list}', marker='+', linestyle='-')
        # params_list = [1e2]
        # runner = MultiTestRunner(['LRFU'], BUFFER_SIZE_LIST, trace_file, params_list)
        # result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, result, label=f'LRFU p={params_list}', marker='+', linestyle='-')
        # params_list = [1e4]
        # runner = MultiTestRunner(['LRFU'], BUFFER_SIZE_LIST, trace_file, params_list)
        # result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, result, label=f'LRFU p={params_list}', marker='+', linestyle='-')
        # params_list = [1e6]
        # runner = MultiTestRunner(['LRFU'], BUFFER_SIZE_LIST, trace_file, params_list)
        # result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, result, label=f'LRFU p={params_list}', marker='+', linestyle='-')
        params_list = [1e-6, 1, 1]
        efsw_runner = MultiTestRunner(['EFSW'], BUFFER_SIZE_LIST, trace_file, params_list)
        efsw_result = efsw_runner.get_hit_rate_list()
        ax.plot(BUFFER_SIZE_LIST, efsw_result, label=f'EFSW, p={params_list}', marker='+', linestyle='-.')

        params_list = [1e-4, 1, 1]
        efsw_runner = MultiTestRunner(['EFSW'], BUFFER_SIZE_LIST, trace_file, params_list)
        efsw_result = efsw_runner.get_hit_rate_list()
        ax.plot(BUFFER_SIZE_LIST, efsw_result, label=f'EFSW, p={params_list}', marker='+', linestyle='-.')

        params_list = [0.01, 1, 1]
        efsw_runner = MultiTestRunner(['EFSW'], BUFFER_SIZE_LIST, trace_file, params_list)
        efsw_result = efsw_runner.get_hit_rate_list()
        ax.plot(BUFFER_SIZE_LIST, efsw_result, label=f'EFSW, p={params_list}', marker='+', linestyle='-.')

        params_list = [1, 1, 1]
        efsw_runner = MultiTestRunner(['EFSW'], BUFFER_SIZE_LIST, trace_file, params_list)
        efsw_result = efsw_runner.get_hit_rate_list()
        ax.plot(BUFFER_SIZE_LIST, efsw_result, label=f'EFSW, p={params_list}', marker='+', linestyle='-.')

        params_list = [100, 1, 1]
        efsw_runner = MultiTestRunner(['EFSW'], BUFFER_SIZE_LIST, trace_file, params_list)
        efsw_result = efsw_runner.get_hit_rate_list()
        ax.plot(BUFFER_SIZE_LIST, efsw_result, label=f'EFSW, p={params_list}', marker='+', linestyle='-.')

        params_list = [10000, 1, 1]
        efsw_runner = MultiTestRunner(['EFSW'], BUFFER_SIZE_LIST, trace_file, params_list)
        efsw_result = efsw_runner.get_hit_rate_list()
        ax.plot(BUFFER_SIZE_LIST, efsw_result, label=f'EFSW, p={params_list}', marker='+', linestyle='-.')

        params_list = [20000, 5, 0.1, 5]
        runner = MultiTestRunner(['ALRFU'], BUFFER_SIZE_LIST, trace_file, params_list)
        result = runner.get_hit_rate_list()
        ax.plot(BUFFER_SIZE_LIST, result, label=f'ALRFU, p={params_list}', marker='+', linestyle='-')

        opt_runner = MultiTestRunner(['OPT'], BUFFER_SIZE_LIST, trace_file, None)
        opt_result = opt_runner.get_hit_rate_list()
        ax.plot(BUFFER_SIZE_LIST, opt_result, label='OPT*', marker='+', linestyle='-.')

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
        # fig_path = f'local/plot_{trace}.png'
        fig_path = f'local/plot_{trace}.png'
        plt.savefig(fig_path)
        print(f'Fig generated path: {fig_path}. ')
