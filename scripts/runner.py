#!/usr/bin/env python
import os
import matplotlib.pyplot as plt
from utils import SingleTestRunner, MultiTestRunner, TRACES_LIST

# CACHE_POLICY_LIST = [
#     'LRU'
# ]
# # Home2
# MIN_BUFFER_SIZE = 6
# MAX_BUFFER_SIZE = 20
# BUFFER_SIZE_LIST = [2 ** k for k in range(MIN_BUFFER_SIZE, MAX_BUFFER_SIZE + 1)]
#
# TRACE_FILE_LIST = [
#     # 'websearch',
#     'Home2',
# ]

# websearch
MIN_BUFFER_SIZE = 2
MAX_BUFFER_SIZE = 10
BUFFER_SIZE_LIST = [2 ** k for k in range(MIN_BUFFER_SIZE, MAX_BUFFER_SIZE + 1)]

TRACE_FILE_LIST = [
    'websearch',
    # 'Home2',
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

        arc_runner = MultiTestRunner(['ARC'], BUFFER_SIZE_LIST, trace_file, None)
        arc_result = arc_runner.get_hit_rate_list()
        ax.plot(BUFFER_SIZE_LIST, arc_result, label='ARC', marker='+', linestyle='dashed')

        lirs_runner = MultiTestRunner(['LIRS'], BUFFER_SIZE_LIST, trace_file, None)
        lirs_result = lirs_runner.get_hit_rate_list()
        ax.plot(BUFFER_SIZE_LIST, lirs_result, label='LIRS', marker='+', linestyle='dashed')

        # params_list = [20000, 5, 0.1, 5, -1, 1, 1]
        # runner = MultiTestRunner(['ALRFU5'], BUFFER_SIZE_LIST, trace_file, params_list)
        # result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, result, label=f'ALRFU5, p={params_list}', marker='+', linestyle='-')

        # params_list = [20000, 20, 0.5, 1, 8, 10]
        # runner = MultiTestRunner(['GLRFU'], BUFFER_SIZE_LIST, trace_file, params_list)
        # result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, result, label=f'GLRFU, p={params_list}', marker='+', linestyle='-')

        params_list = [20000, 20, 0.5, 5, 4, 10, 8]
        # params_list = [1000, 4, 0.3, 1, 32, 10, 8]
        runner = MultiTestRunner(['GLRFU2'], BUFFER_SIZE_LIST, trace_file, params_list)
        glrfu2_f_result = runner.get_hit_rate_list()
        ax.plot(BUFFER_SIZE_LIST, glrfu2_f_result, label=f'GLRFU2, p={params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, glrfu2_f_result, "RGC")

        params_list = [20000, 20, 0.5, 1, 4, 10, 8]
        # params_list = [1000, 4, 0.3, 1, 32, 10, 8]
        runner = MultiTestRunner(['GLRFU2'], BUFFER_SIZE_LIST, trace_file, params_list)
        glrfu2_f_result = runner.get_hit_rate_list()
        ax.plot(BUFFER_SIZE_LIST, glrfu2_f_result, label=f'GLRFU2, p={params_list}', marker='+', linestyle='-')

        params_list = [20000, 20, 0.5, 0.1, 4, 10, 8]
        # params_list = [1000, 4, 0.3, 1, 32, 10, 8]
        runner = MultiTestRunner(['GLRFU2'], BUFFER_SIZE_LIST, trace_file, params_list)
        glrfu2_f_result = runner.get_hit_rate_list()
        ax.plot(BUFFER_SIZE_LIST, glrfu2_f_result, label=f'GLRFU2, p={params_list}', marker='+', linestyle='-')

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
        fig_path = f'local/plot_{trace}_921.png'
        plt.savefig(fig_path)
        print(f'Fig generated path: {fig_path}. ')
