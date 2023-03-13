#!/usr/bin/env python
import os
import matplotlib.pyplot as plt
from utils import SingleTestRunner, MultiTestRunner, TRACES_LIST, BUFFER_LIST_FOR_TRACES, StatisticsCompareLRU

# CACHE_POLICY_LIST = [
#     'LRU'
# ]
MIN_BUFFER_SIZE = 11
MAX_BUFFER_SIZE = 18
BUFFER_SIZE_LIST = [2 ** k for k in range(MIN_BUFFER_SIZE, MAX_BUFFER_SIZE + 1)]

SUFFIX = '313g'
# TRACE_FILE_LIST = [
#     'P1',
# ]

stats = StatisticsCompareLRU()

if __name__ == '__main__':
    print(f'Start run tests. Trace file: {TRACES_LIST}.')
    for trace in TRACES_LIST:
        BUFFER_SIZE_LIST = BUFFER_LIST_FOR_TRACES[trace]
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

        params_list = [20000, 5, 0.1, 5, -1, 1, 1]
        runner = MultiTestRunner(['ALRFU5'], BUFFER_SIZE_LIST, trace_file, params_list)
        alrfu_result = runner.get_hit_rate_list()
        ax.plot(BUFFER_SIZE_LIST, alrfu_result, label=f'ALRFU5, p={params_list}', marker='+', linestyle='-')

        # params_list = [20000, 5, 0.1, 5, 8, 1, 1]
        # runner = MultiTestRunner(['ALRFU5'], BUFFER_SIZE_LIST, trace_file, params_list)
        # alrfu_limit_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, alrfu_limit_result, label=f'ALRFU5, p={params_list}', marker='+', linestyle='-')

        params_list = [20000, 5, 1.0, 1, 8, 10]
        runner = MultiTestRunner(['GLRFU'], BUFFER_SIZE_LIST, trace_file, params_list)
        glrfu_result = runner.get_hit_rate_list()
        ax.plot(BUFFER_SIZE_LIST, glrfu_result, label=f'GLRFU, p={params_list}', marker='+', linestyle='-')

        params_list = [20000, 10, 0.5, 5, 4, 10]
        runner = MultiTestRunner(['GLRFU'], BUFFER_SIZE_LIST, trace_file, params_list)
        glrfu_higher_result = runner.get_hit_rate_list()
        ax.plot(BUFFER_SIZE_LIST, glrfu_higher_result, label=f'GLRFU, p={params_list}', marker='+', linestyle='-')

        params_list = [20000, 10, 0.3, 5, 4, 10]
        runner = MultiTestRunner(['GLRFU'], BUFFER_SIZE_LIST, trace_file, params_list)
        glrfu_result_p3 = runner.get_hit_rate_list()
        ax.plot(BUFFER_SIZE_LIST, glrfu_result_p3, label=f'GLRFU, p={params_list}', marker='+', linestyle='-')

        params_list = [20000, 10, 0.3, 5, 4, 10, 8]
        runner = MultiTestRunner(['GLRFU2'], BUFFER_SIZE_LIST, trace_file, params_list)
        glrfu2_8r_result = runner.get_hit_rate_list()
        ax.plot(BUFFER_SIZE_LIST, glrfu2_8r_result, label=f'GLRFU2, p={params_list}', marker='+', linestyle='-')

        params_list = [20000, 10, 0.25, 5, 4, 10, 4]
        runner = MultiTestRunner(['GLRFU2'], BUFFER_SIZE_LIST, trace_file, params_list)
        glrfu2_4r_result = runner.get_hit_rate_list()
        ax.plot(BUFFER_SIZE_LIST, glrfu2_4r_result, label=f'GLRFU2, p={params_list}', marker='+', linestyle='-')

        params_list = [20000, 10, 1.0, 5, 4, 10, 4]
        runner = MultiTestRunner(['GLRFU2'], BUFFER_SIZE_LIST, trace_file, params_list)
        glrfu2_a_result = runner.get_hit_rate_list()
        ax.plot(BUFFER_SIZE_LIST, glrfu2_a_result, label=f'GLRFU2, p={params_list}', marker='+', linestyle='-')

        params_list = [20000, 10, 0.5, 5, 4, 10, 4]
        runner = MultiTestRunner(['GLRFU2'], BUFFER_SIZE_LIST, trace_file, params_list)
        glrfu2_b_result = runner.get_hit_rate_list()
        ax.plot(BUFFER_SIZE_LIST, glrfu2_b_result, label=f'GLRFU2, p={params_list}', marker='+', linestyle='-')

        opt_runner = MultiTestRunner(['OPT'], BUFFER_SIZE_LIST, trace_file, None)
        opt_result = opt_runner.get_hit_rate_list()
        ax.plot(BUFFER_SIZE_LIST, opt_result, label='OPT*', marker='+', linestyle='-.')

        stats.statistic(lru_result, arc_result, "ARC")
        stats.statistic(lru_result, alrfu_result, "ALRFU")
        # stats.statistic(lru_result, alrfu_limit_result, "ALRFU_LIMIT")
        stats.statistic(lru_result, glrfu_result, "GLRFU")
        stats.statistic(lru_result, glrfu_result_p3, "GLRFU_P3")
        stats.statistic(lru_result, glrfu2_8r_result, "GLRFU2_8r")
        stats.statistic(lru_result, glrfu2_4r_result, "GLRFU2_4r")
        stats.statistic(lru_result, glrfu2_a_result, "GLRFU2_a")
        stats.statistic(lru_result, glrfu2_b_result, "GLRFU2_b")
        stats.statistic(lru_result, glrfu_higher_result, "GLRFU_HIGHER")
        stats.statistic(lru_result, opt_result, "OPT")
        # statistics_compare_lru(lru_result, arc_result)
        # statistics_compare_lru(lru_result, glrfu_result)
        # statistics_compare_lru(lru_result, opt_result)
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
        fig_path = f'local/{SUFFIX}_plot_{trace}.png'
        # fig_path = 'local/plot.png'
        plt.savefig(fig_path)
        print(f'Fig generated path: {fig_path}. ')
        stats.print_result()

