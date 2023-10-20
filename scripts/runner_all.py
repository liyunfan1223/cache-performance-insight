#!/usr/bin/env python
import os
import matplotlib.pyplot as plt
from utils import SingleTestRunner, MultiTestRunner, TRACES_LIST, BUFFER_LIST_FOR_TRACES, StatisticsCompareLRU

# CACHE_POLICY_LIST = [
#     'LRU'
# ]
# MIN_BUFFER_SIZE = -4
MIN_BUFFER_SIZE = 0
MAX_BUFFER_SIZE = 4
# MAX_BUFFER_SIZE = 2
BASIC_BUFFER_SIZE_LIST = [(0.01 * (2 ** k)) for k in range(MIN_BUFFER_SIZE, MAX_BUFFER_SIZE + 1)]
# BUFFER_SIZE_LIST = [0.000625, 0.00125, 0.0025, 0.005, 0.01, 0.02, 0.04, 0.08]
# BUFFER_SIZE_LIST = [0.4]
PREFIX = '1020'
# TRACE_FILE_LIST = [
#     'P1',
# ]

stats = StatisticsCompareLRU()

if __name__ == '__main__':
    print(f'Start run tests. Trace file: {TRACES_LIST}.')
    for trace in TRACES_LIST:
        if trace in BUFFER_LIST_FOR_TRACES:
            BUFFER_SIZE_LIST = BUFFER_LIST_FOR_TRACES[trace]
        else:
            BUFFER_SIZE_LIST = BASIC_BUFFER_SIZE_LIST
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

        lfu_runner = MultiTestRunner(['LFU'], BUFFER_SIZE_LIST, trace_file, None)
        lfu_result = lfu_runner.get_hit_rate_list()
        ax.plot(BUFFER_SIZE_LIST, lfu_result, label='LFU', marker='+', linestyle='dashed')
        stats.statistic(lru_result, lfu_result, "LFU")

        # srrip_runner = MultiTestRunner(['SRRIP'], BUFFER_SIZE_LIST, trace_file, None)
        # srrip_result = srrip_runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, srrip_result, label='SRRIP', marker='+', linestyle='dashed')
        # stats.statistic(lru_result, srrip_result, "SRRIP")

        arc_runner = MultiTestRunner(['ARC'], BUFFER_SIZE_LIST, trace_file, None)
        arc_result = arc_runner.get_hit_rate_list()
        ax.plot(BUFFER_SIZE_LIST, arc_result, label='ARC', marker='+', linestyle='dashed')
        stats.statistic(lru_result, arc_result, "ARC")

        # lirs_runner = MultiTestRunner(['LIRS'], BUFFER_SIZE_LIST, trace_file, None)
        # lirs_result = lirs_runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, lirs_result, label='LIRS', marker='+', linestyle='dashed')
        # stats.statistic(lru_result, lirs_result, "LIRS")

        params_list = [2]
        lirs2_runner = MultiTestRunner(['LIRS'], BUFFER_SIZE_LIST, trace_file, params_list)
        lirs2_result = lirs2_runner.get_hit_rate_list()
        ax.plot(BUFFER_SIZE_LIST, lirs2_result, label=f'LIRS-{params_list}', marker='+', linestyle='dashed')
        stats.statistic(lru_result, lirs2_result, "LIRS2")

        params_list = [2]
        dlirs2_runner = MultiTestRunner(['DLIRS'], BUFFER_SIZE_LIST, trace_file, params_list)
        dlirs2_result = dlirs2_runner.get_hit_rate_list()
        ax.plot(BUFFER_SIZE_LIST, dlirs2_result, label=f'DLIRS-{params_list}', marker='+', linestyle='dashed')
        stats.statistic(lru_result, dlirs2_result, "DLIRS2")

        params_list = []
        cacheus_runner = MultiTestRunner(['CACHEUS'], BUFFER_SIZE_LIST, trace_file, params_list)
        cacheus_result = cacheus_runner.get_hit_rate_list()
        ax.plot(BUFFER_SIZE_LIST, cacheus_result, label=f'CACHEUS-{params_list}', marker='+', linestyle='dashed')
        stats.statistic(lru_result, cacheus_result, "CACHEUS")

        # params_list = [16, 1, 6, 4, 1.0, 20000, 0.5, 0.10, 0.00, 0.01, 1, 1024]
        # runner = MultiTestRunner(['RGC4'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC4 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC4(3)")
        #
        # params_list = [16, 1, 6, 4, 1.0, 20000, 0.5, 0.05, 0.00, 0.01, 1, 1024]
        # runner = MultiTestRunner(['RGC4'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC4 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC4(3b)")

        params_list = [16, 1, 6, 4, 1.0, 20000, 0.5, 0.05, 0.00, 0.05, 1, 1024]
        runner = MultiTestRunner(['RGC4'], BUFFER_SIZE_LIST, trace_file, params_list)
        rgc_result = runner.get_hit_rate_list()
        ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC4 {params_list}', marker='+', linestyle='-')
        stats.statistic(lru_result, rgc_result, "New-RGC4(3c)")

        # params_list = [16, 1, 6, 4, 1.0, 20000, 0.5, 0.05, 0.00, 0.10, 1, 1024]
        # runner = MultiTestRunner(['RGC4'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC4 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC4(3d)")

        # """with out MRU & Top-LRU"""
        # params_list = [16, 1, 6, 4, 1.0, 20000, 0.5, 0.00, 0.00, 0.01, 1, -1]
        # runner = MultiTestRunner(['RGC4'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC4 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC4(4)")
        #
        params_list = [16, 1, 6, 4, 1.0, 20000, 0.5, 0.00, 0.00, 0.05, 1, -1]
        runner = MultiTestRunner(['RGC4'], BUFFER_SIZE_LIST, trace_file, params_list)
        rgc_result = runner.get_hit_rate_list()
        ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC4 {params_list}', marker='+', linestyle='-')
        stats.statistic(lru_result, rgc_result, "New-RGC4(4b)")

        # """without MRU & Top-LRU"""
        # params_list = [16, 1, 6, 4, 1.0, 20000, 0.5, 0.00, 0.00, 5.0, 1, -1]
        # runner = MultiTestRunner(['RGC4'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC4 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC4(4b2)")

        # params_list = [16, 1, 6, 4, 1.0, 20000, 0.5, 0.00, 0.00, 10000.0, 1, -1]
        # runner = MultiTestRunner(['RGC4'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC4 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC4(4b3)")

        # params_list = [20000, 16, 0.5, 1.0, 1, 6, 4]
        # # params_list = [1000, 4, 0.3, 1, 32, 10, 8]
        # runner = MultiTestRunner(['GLRFU2'], BUFFER_SIZE_LIST, trace_file, params_list)
        # glrfu2_f_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, glrfu2_f_result, label=f'GLRFU2, p={params_list}', marker='+', linestyle='dotted')
        # stats.statistic(lru_result, glrfu2_f_result, f"GLRFU-{params_list}")
        #
        # params_list = [16, 1, 6, 4, 1.0, 20000, 0.5, 0.00, 0.00, 10000.0, 1, -1]
        # runner = MultiTestRunner(['RGC4'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC4 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC4(4c)")

        # """1 times ghost cache"""
        # params_list = [16, 1, 6, 1, 1.0, 20000, 0.5, 0.10, 0.00, 0.01, 1, 1024]
        # runner = MultiTestRunner(['RGC4'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC4 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC4(5)")
        #
        # params_list = [16, 1, 6, 1, 1.0, 20000, 0.5, 0.05, 0.00, 0.05, 1, 1024]
        # runner = MultiTestRunner(['RGC4'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC4 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC4(5b)")

        """no simulator"""
        # params_list = [16, 1, 6, 4, 1.0, 20000, 0.5, 0.10, 0.00, 0.0, 1, 1024]
        # runner = MultiTestRunner(['RGC4'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC4 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC4(20)")

        params_list = [16, 1, 6, 4, 1.0, 20000, 0.5, 0.05, 0.00, 0.0, 1, 1024]
        runner = MultiTestRunner(['RGC4'], BUFFER_SIZE_LIST, trace_file, params_list)
        rgc_result = runner.get_hit_rate_list()
        ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC4 {params_list}', marker='+', linestyle='-')
        stats.statistic(lru_result, rgc_result, "New-RGC4(20c)")


        # """1 times ghost cache & no simulator"""
        # params_list = [16, 1, 6, 1, 1.0, 20000, 0.5, 0.10, 0.00, 0.0, 1, 1024]
        # runner = MultiTestRunner(['RGC4'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC4 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC4(20b)")
        #
        # params_list = [16, 1, 6, 1, 1.0, 20000, 0.5, 0.05, 0.00, 0.0, 1, 1024]
        # runner = MultiTestRunner(['RGC4'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC4 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC4(21c)")

        opt_runner = MultiTestRunner(['OPT'], BUFFER_SIZE_LIST, trace_file, None)
        opt_result = opt_runner.get_hit_rate_list()
        ax.plot(BUFFER_SIZE_LIST, opt_result, label='OPT*', marker='+', linestyle='-.')
        stats.statistic(lru_result, opt_result, "OPT")

        ax.set_xscale('log')
        # ax.set_yscale('log')
        # ax.set_yticks([2, 4, 8, 16, 32, 64, 100])
        # ax.set_yticklabels([2, 4, 8, 16, 32, 64, ''])
        # ax.set_ylim(0.5, 100)
        ax.set_xticks(BUFFER_SIZE_LIST)
        ax.set_xticklabels(BUFFER_SIZE_LIST)
        ax.set_xlim(BUFFER_SIZE_LIST[0] / 2, BUFFER_SIZE_LIST[-1] * 2)
        # plt.legend(loc=3)
        plt.legend(loc=0)
        if not os.path.exists('local'):
            os.mkdir('local')
        fig_path = f'local/{PREFIX}_plot_{trace}.png'
        # fig_path = 'local/plot.png'
        plt.savefig(fig_path)
        print(f'Fig generated path: {fig_path}. ')
        stats.print_result()




        # params_list = [3]
        # lirs2_runner = MultiTestRunner(['LIRS'], BUFFER_SIZE_LIST, trace_file, params_list)
        # lirs2_result = lirs2_runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, lirs2_result, label=f'LIRS-{params_list}', marker='+', linestyle='dashed')
        # stats.statistic(lru_result, lirs2_result, "LIRS3")
        #
        # params_list = [4]
        # lirs2_runner = MultiTestRunner(['LIRS'], BUFFER_SIZE_LIST, trace_file, params_list)
        # lirs2_result = lirs2_runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, lirs2_result, label=f'LIRS-{params_list}', marker='+', linestyle='dashed')
        # stats.statistic(lru_result, lirs2_result, "LIRS4")
        #
        # params_list = [5]
        # lirs2_runner = MultiTestRunner(['LIRS'], BUFFER_SIZE_LIST, trace_file, params_list)
        # lirs2_result = lirs2_runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, lirs2_result, label=f'LIRS-{params_list}', marker='+', linestyle='dashed')
        # stats.statistic(lru_result, lirs2_result, "LIRS5")

        # params_list = [20000, 20, 0.5, 5, 4, 10, 1]
        # runner = MultiTestRunner(['GLRFU2'], BUFFER_SIZE_LIST, trace_file, params_list)
        # glrfu2_e_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, glrfu2_e_result, label=f'GLRFU2, p={params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, glrfu2_e_result, "RGC")

        # params_list = [20000, 20, 0.5, 5, 4, 10, 4]
        # runner = MultiTestRunner(['GLRFU2'], BUFFER_SIZE_LIST, trace_file, params_list)
        # glrfu2_e_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, glrfu2_e_result, label=f'GLRFU2, p={params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, glrfu2_e_result, "RGC")

        # params_list = [20000, 20, 0.5, 5, 4, 10, 1]
        # runner = MultiTestRunner(['GLRFU2'], BUFFER_SIZE_LIST, trace_file, params_list)
        # glrfu2_f_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, glrfu2_f_result, label=f'GLRFU2, p={params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, glrfu2_f_result, "RGC")

        # params_list = [20000, 20, 0.5, 0.1, 4, 10, 8]
        # # params_list = [1000, 4, 0.3, 1, 32, 10, 8]
        # runner = MultiTestRunner(['GLRFU2'], BUFFER_SIZE_LIST, trace_file, params_list)
        # glrfu2_f_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, glrfu2_f_result, label=f'GLRFU2, p={params_list}', marker='+', linestyle='--')
        # stats.statistic(lru_result, glrfu2_f_result, f"GLRFU-{params_list}")
        #
        # params_list = [20000, 20, 0.5, 0.1, 4, 10, 1]
        # # params_list = [1000, 4, 0.3, 1, 32, 10, 8]
        # runner = MultiTestRunner(['GLRFU2'], BUFFER_SIZE_LIST, trace_file, params_list)
        # glrfu2_f_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, glrfu2_f_result, label=f'GLRFU2, p={params_list}', marker='+', linestyle='--')
        # stats.statistic(lru_result, glrfu2_f_result, f"GLRFU-{params_list}")

        # params_list = [20000, 20, 0.5, 1.0, 4, 10, 4]
        # # params_list = [1000, 4, 0.3, 1, 32, 10, 8]
        # runner = MultiTestRunner(['GLRFU2'], BUFFER_SIZE_LIST, trace_file, params_list)
        # glrfu2_f_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, glrfu2_f_result, label=f'GLRFU2, p={params_list}', marker='+', linestyle='dotted')
        # stats.statistic(lru_result, glrfu2_f_result, f"GLRFU-{params_list}")



        # params_list = [20, 4, 10, 4, 1.0, 20000, 0.5, 0.01, 0.01, 5, 1, 1024]
        # runner = MultiTestRunner(['RGC'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC18")
        #
        # params_list = [20, 4, 10, 1, 1.0, 20000, 0.5, 0.01, 0.01, 5, 1, 1024]
        # runner = MultiTestRunner(['RGC'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC19")
        #
        # params_list = [20, 4, 10, 4, 1.0, 20000, 0.5, 0.01, 0.01, 5, 1, 1024]
        # runner = MultiTestRunner(['RGC3'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC3 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC3(1)")
        #
        # params_list = [20, 4, 10, 1, 1.0, 20000, 0.5, 0.01, 0.01, 5, 1, 1024]
        # runner = MultiTestRunner(['RGC3'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC3 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC3(2)")
        #
        # params_list = [20, 4, 10, 4, 1.0, 20000, 0.5, 0.00, 0.00, 5, 1, -1]
        # runner = MultiTestRunner(['RGC3'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC3 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC3(3)")
        #
        # params_list = [20, 4, 10, 1, 1.0, 20000, 0.5, 0.00, 0.00, 5, 1, -1]
        # runner = MultiTestRunner(['RGC3'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC3 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC3(4)")

        # params_list = [20, 4, 10, 4, 1.0, 20000, 0.5, 0.01, 0.00, 5, 1, 1024]
        # runner = MultiTestRunner(['RGC3'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC3 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC3(5)")
        #
        # params_list = [20, 4, 10, 4, 1.0, 20000, 0.5, 0.00, 0.00, 5, 1, -1]
        # runner = MultiTestRunner(['RGC3'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC3 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC3(6)")
        #
        # params_list = [20, 4, 10, 4, 1.0, 20000, 0.5, 0.00, 0.00, 10000, 0, -1]
        # runner = MultiTestRunner(['RGC3'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC3 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC3(7)")
        #
        # params_list = [20, 4, 10, 4, 1.0, 20000, 0.5, 0.00, 0.00, 10000, 0, -1]
        # runner = MultiTestRunner(['RGC'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "RGC20")
        #
        # params_list = [20, 1, 8, 4, 1.0, 20000, 0.5, 0.01, 0.00, 5, 1, 1024]
        # runner = MultiTestRunner(['RGC3'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC3 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC3(8)")
        #
        # params_list = [20, 4, 8, 4, 1.0, 20000, 0.5, 0.01, 0.00, 5, 1, 1024]
        # runner = MultiTestRunner(['RGC3'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC3 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC3(9)")

        # params_list = [20, 1, 6, 4, 1.0, 20000, 0.5, 0.01, 0.00, 5, 1, 1024]
        # runner = MultiTestRunner(['RGC3'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC3 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC3(10)")
        #
        # params_list = [20, 1, 7, 4, 1.0, 20000, 0.5, 0.01, 0.00, 5, 1, 1024]
        # runner = MultiTestRunner(['RGC3'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC3 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC3(14)")
        #
        # params_list = [20, 1, 6, 4, 1.0, 20000, 0.5, 0.00, 0.00, 5, 1, -1]
        # runner = MultiTestRunner(['RGC3'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC3 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC3(17)")
        #
        # params_list = [20, 1, 6, 4, 1.0, 19999, 0.5, 0.00, 0.00, 5, 1, -1]
        # runner = MultiTestRunner(['RGC3'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC3 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC3(18)")
        #
        # params_list = [20, 1, 6, 4, 1.0, 20000, 1.0, 0.01, 0.00, 5, 1, 1024]
        # runner = MultiTestRunner(['RGC3'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC3 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC3(19)")

        # params_list = [4, 1, 6, 4, 1.0, 20000, 0.5, 0.01, 0.00, 5, 1, 1024]
        # runner = MultiTestRunner(['RGC3'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC3 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC3(20)")

        # params_list = [20, 1, 6, 4, 1.0, 20000, 0.5, 0.05, 0.00, 5, 1, 1024]
        # runner = MultiTestRunner(['RGC3'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC3 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC3(21)")
        #
        # params_list = [20, 1, 6, 4, 1.0, 20000, 0.5, 0.10, 0.00, 5, 1, 1024]
        # runner = MultiTestRunner(['RGC3'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC3 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC3(22)")

        # params_list = [20, 1, 6, 3, 1.0, 20000, 0.5, 0.05, 0.00, 5, 1, 1024]
        # runner = MultiTestRunner(['RGC3'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC3 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC3(23)")
        #
        # params_list = [20, 1, 6, 2, 1.0, 20000, 0.5, 0.05, 0.00, 5, 1, 1024]
        # runner = MultiTestRunner(['RGC3'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC3 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC3(24)")

        # params_list = [20, 1, 6, 1, 1.0, 20000, 0.5, 0.05, 0.00, 5, 1, 1024]
        # runner = MultiTestRunner(['RGC3'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC3 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC3(25)")
        #
        # params_list = [20, 1, 6, 8, 1.0, 20000, 0.5, 0.05, 0.00, 5, 1, 1024]
        # runner = MultiTestRunner(['RGC3'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC3 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC3(26)")
        #
        # params_list = [20, 1, 6, 4, 1.0, 20000, 1.0, 0.05, 0.00, 5, 1, 1024]
        # runner = MultiTestRunner(['RGC3'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC3 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC3(27)")
        #
        # # params_list = [20, 1, 6, 4, 1.0, 20000, 0.5, 0.05, 0.00, 10, 1, 1024]
        # # runner = MultiTestRunner(['RGC3'], BUFFER_SIZE_LIST, trace_file, params_list)
        # # rgc_result = runner.get_hit_rate_list()
        # # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC3 {params_list}', marker='+', linestyle='-')
        # # stats.statistic(lru_result, rgc_result, "New-RGC3(28)")
        #
        # params_list = [20, 1, 6, 4, 1.0, 20000, 0.5, 0.10, 0.00, 1, 1, 1024]
        # runner = MultiTestRunner(['RGC3'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC3 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC3(29)")

        # params_list = [20, 1, 6, 4, 1.0, 20000, 0.5, 0.05, 0.00, 1, 1, 1024]
        # runner = MultiTestRunner(['RGC3'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC3 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC3(30)")

        # params_list = [20, 1, 6, 4, 1.0, 20000, 0.5, 0.00, 0.00, 1, 1, -1]
        # runner = MultiTestRunner(['RGC3'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC3 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC3(31)")
        #
        # params_list = [20, 1, 6, 4, 1.0, 20000, 0.5, 0.10, 0.00, 0.5, 1, 1024]
        # runner = MultiTestRunner(['RGC3'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC3 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC3(32)")
        #
        # params_list = [20, 1, 6, 4, 1.0, 20000, 0.5, 0.10, 0.00, 0.2, 1, 1024]
        # runner = MultiTestRunner(['RGC3'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC3 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC3(33)")
        #
        # params_list = [16, 1, 6, 4, 1.0, 20000, 0.5, 0.10, 0.00, 0.2, 1, 1024]
        # runner = MultiTestRunner(['RGC3'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC3 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC3(34)")

        # 1019
        # params_list = [16, 1, 6, 4, 1.0, 20000, 0.5, 0.10, 0.00, 0.1, 1, 1024]
        # runner = MultiTestRunner(['RGC3'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC3 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC3(35)")

        # params_list = [16, 1, 6, 4, 1.0, 20000, 0.5, 0.10, 0.00, 0.5, 1, 1024]
        # runner = MultiTestRunner(['RGC3'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC3 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC3(36)")
        #
        # params_list = [16, 1, 6, 4, 1.0, 20000, 0.5, 0.00, 0.00, 0.1, 1, -1]
        # runner = MultiTestRunner(['RGC3'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC3 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC3(37)")
        #
        # params_list = [16, 1, 6, 4, 1.0, 20000, 0.5, 0.10, 0.00, 0.05, 1, 1024]
        # runner = MultiTestRunner(['RGC3'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC3 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC3(38)")

        # params_list = [16, 1, 6, 4, 1.0, 20000, 0.5, 0.10, 0.00, 0.01, 1, 1024]
        # runner = MultiTestRunner(['RGC3'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC3 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC3(39)")
        #
        # params_list = [16, 1, 6, 4, 1.0, 20000, 0.5, 0.10, 0.00, 0.00, 1, 1024]
        # runner = MultiTestRunner(['RGC3'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC3 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC3(40)")
        #
        # # params_list = [10000, 1, 6, 4, 1.0, 20000, 0.5, 0.10, 0.00, 0.00, 1, 1024]
        # # runner = MultiTestRunner(['RGC3'], BUFFER_SIZE_LIST, trace_file, params_list)
        # # rgc_result = runner.get_hit_rate_list()
        # # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC3 {params_list}', marker='+', linestyle='-')
        # # stats.statistic(lru_result, rgc_result, "New-RGC3(41)")
        #
        # params_list = [8, 1, 6, 4, 1.0, 20000, 0.5, 0.10, 0.00, 0.01, 1, 1024]
        # runner = MultiTestRunner(['RGC3'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC3 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC3(42)")
        #
        # params_list = [32, 1, 6, 4, 1.0, 20000, 0.5, 0.10, 0.00, 0.1, 1, 1024]
        # runner = MultiTestRunner(['RGC3'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC3 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC3(43)")
        #
        # params_list = [32, 1, 6, 4, 1.0, 20000, 0.5, 0.10, 0.00, 0.01, 1, 1024]
        # runner = MultiTestRunner(['RGC3'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC3 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC3(44)")
        #
        # params_list = [32, 1, 6, 4, 1.0, 20000, 0.5, 0.10, 0.00, 0.00, 1, 1024]
        # runner = MultiTestRunner(['RGC3'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC3 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC3(45)")
        #
        # params_list = [16, 1, 6, 1, 1.0, 20000, 0.5, 0.10, 0.00, 0.01, 1, 1024]
        # runner = MultiTestRunner(['RGC3'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC3 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC3(46)")
        #
        # params_list = [16, 1, 6, 2, 1.0, 20000, 0.5, 0.10, 0.00, 0.01, 1, 1024]
        # runner = MultiTestRunner(['RGC3'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC3 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC3(47)")
        #
        # params_list = [16, 1, 6, 32, 1.0, 20000, 0.5, 0.10, 0.00, 0.01, 1, 1024]
        # runner = MultiTestRunner(['RGC3'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC3 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC3(48)")
        #
        # params_list = [16, 1, 6, 4, 0.0, 20000, 0.5, 0.10, 0.00, 0.00, 1, 1024]
        # runner = MultiTestRunner(['RGC3'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC3 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC3(49)")
        #
        # params_list = [16, 1, 6, 4, 1.0, 20000, 0.5, 0.10, 0.00, 0.10, 1, 1024]
        # runner = MultiTestRunner(['RGC4'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC4 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC4(1)")
        #
        # params_list = [16, 1, 6, 4, 1.0, 20000, 0.5, 0.10, 0.00, 0.05, 1, 1024]
        # runner = MultiTestRunner(['RGC4'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC4 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC4(2)")


        # params_list = [16, 1, 6, 4, 1.0, 20000, 0.5, 0.05, 0.00, 0.00, 1, 1024]
        # runner = MultiTestRunner(['RGC4'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC4 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC4(20d)")
        # params_list = [8, 1, 6, 4, 1.0, 20000, 0.5, 0.10, 0.00, 0.01, 1, 1024]
        # runner = MultiTestRunner(['RGC4'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC4 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC4(21)")
        #
        # params_list = [8, 1, 6, 4, 1.0, 20000, 0.5, 0.10, 0.00, 0.00, 1, 1024]
        # runner = MultiTestRunner(['RGC4'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC4 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC4(21b)")
        #
        # params_list = [8, 1, 6, 4, 1.0, 20000, 0.5, 0.10, 0.00, 0.1, 1, 1024]
        # runner = MultiTestRunner(['RGC4'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC4 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC4(21c)")

        # params_list = [16, 1, 6, 4, 1.0, 20000, 0.5, 0.10, 0.00, 0.00, 1, 1024]
        # runner = MultiTestRunner(['RGC4'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC4 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC4(4)")

        # params_list = [20, 1, 6, 4, 1.0, 20000, 0.5, 0.10, 0.00, 5, 1, 1024]
        # runner = MultiTestRunner(['RGC3'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC3 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC3(23)")

        # params_list = [20, 1, 6, 4, 1.0, 20000, 0.5, 0.05, 0.00, 5, 1, -1]
        # runner = MultiTestRunner(['RGC3'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC3 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC3(23)")
        #
        # params_list = [20, 1, 6, 4, 1.0, 20000, 0.5, 0.20, 0.00, 5, 1, 1024]
        # runner = MultiTestRunner(['RGC3'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC3 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC3(24)")
        #
        # params_list = [20, 1, 6, 4, 1.0, 20000, 0.5, 0.80, 0.00, 5, 1, 1024]
        # runner = MultiTestRunner(['RGC3'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC3 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC3(25)")

        # params_list = [20, 1, 5, 4, 1.0, 20000, 0.5, 0.01, 0.00, 5, 1, 1024]
        # runner = MultiTestRunner(['RGC3'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC3 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC3(15)")

        # params_list = [20, 1, 6, 4, 1.0, 20000, 0.5, 0.00, 0.00, 5, 1, -1]
        # runner = MultiTestRunner(['RGC3'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC3 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC3(16)")

        # params_list = [20, 4, 6, 4, 1.0, 20000, 0.5, 0.01, 0.00, 5, 1, 1024]
        # runner = MultiTestRunner(['RGC3'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC3 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC3(11)")
        #
        # params_list = [20, 1, 4, 4, 1.0, 20000, 0.5, 0.01, 0.00, 5, 1, 1024]
        # runner = MultiTestRunner(['RGC3'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC3 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC3(12)")
        #
        # params_list = [20, 1, 2, 4, 1.0, 20000, 0.5, 0.01, 0.00, 5, 1, 1024]
        # runner = MultiTestRunner(['RGC3'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC3 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC3(13)")

        # params_list = [2, 4, 10, 4, 1.0, 20000, 0.5, 0.01, 0.01, 5, 1, 1024]
        # runner = MultiTestRunner(['RGC'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC20")

        # params_list = [20, 4, 10, 4, 1.0, 20000, 0.5, 0.01, 0.01, 5, 1, 4]
        # runner = MultiTestRunner(['RGC'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC19")

        # params_list = [20, 4, 10, 4, 1.0, 20000, 0.5, 0.01, 0.01, 10000]
        # runner = MultiTestRunner(['RGC'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC15")

        # params_list = [20, 4, 10, 1, 1.0, 20000, 1.0, 0.01, 0.01, 10000]
        # runner = MultiTestRunner(['RGC'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC11")
        # params_list = [20, 4, 10, 4, 1.0, 20000, 0.5, 0.01, 0.01, 5]
        # runner = MultiTestRunner(['RGC2'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC2 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC-2")

        # params_list = [20, 4, 10, 4, 0.1, 20000, 0.5, 0.01, 0.01, 10000]
        # runner = MultiTestRunner(['RGC'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC3")

        # params_list = [20, 4, 10, 4, 1.0, 20000, 0.5, 0.01, 0.01, 10000]
        # runner = MultiTestRunner(['RGC'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC4")


        # params_list = [20, 4, 10, 4, 1.0, 20000, 0.25, 0.01, 0.01, 1]
        # runner = MultiTestRunner(['RGC'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC5")


        # params_list = [16, 1, 6, 1, 1.0, 20000, 0.5, 0.10, 0.00, 0.1, 1, 1024]
        # runner = MultiTestRunner(['RGC4'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC4 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC4(6)")

        # params_list = [16, 1, 6, 4, 1.0, 20000, 0.5, 0.10, 0.00, 0.00, 1, 1024]
        # runner = MultiTestRunner(['RGC4'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC4 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC4(7)")

        # params_list = [16, 1, 6, 4, 1.0, 20000, 0.5, 0.10, 0.00, 0.10, 1, 1024]
        # runner = MultiTestRunner(['RGC4'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC4 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC4(7)")


        # params_list = [16, 1, 6, 4, 1.0, 20000, 0.2, 0.10, 0.00, 0.10, 1, 1024]
        # runner = MultiTestRunner(['RGC4'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC4 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC4(8)")
        #
        # params_list = [16, 1, 6, 4, 1.0, 20000, 0.1, 0.10, 0.00, 0.10, 1, 1024]
        # runner = MultiTestRunner(['RGC4'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC4 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC4(9)")
        #
        # params_list = [16, 1, 6, 4, 1.0, 20000, 1.0, 0.10, 0.00, 0.10, 1, 1024]
        # runner = MultiTestRunner(['RGC4'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC4 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC4(10)")

        # params_list = [16, 1, 6, 4, 1.0, 20000, 0.5, 0.10, 0.00, 10000.0, 1, 1024]
        # runner = MultiTestRunner(['RGC4'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC4 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC4(11)")
        #
        # params_list = [16, 1, 6, 4, 1.0, 20000, 0.5, 0.10, 0.00, 5.0, 1, 1024]
        # runner = MultiTestRunner(['RGC4'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC4 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC4(12)")
        #
        # params_list = [16, 1, 6, 4, 1.0, 20000, 0.5, 0.10, 0.00, 1.0, 1, 1024]
        # runner = MultiTestRunner(['RGC4'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC4 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC4(13)")

        # params_list = [16, 1, 6, 4, 1.0, 20000, 0.5, 0.10, 0.00, 0.1, 1, 1024]
        # runner = MultiTestRunner(['RGC4'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC4 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC4(14)")
        #
        # params_list = [16, 1, 6, 4, 0.1, 20000, 0.5, 0.10, 0.00, 0.1, 1, 1024]
        # runner = MultiTestRunner(['RGC4'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC4 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC4(14b)")

        # params_list = [16, 1, 6, 4, 1.0, 20000, 0.5, 0.10, 0.00, 0.05, 1, 1024]
        # runner = MultiTestRunner(['RGC4'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC4 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC4(15)")
        #
        # params_list = [16, 1, 6, 4, 1.0, 20000, 0.5, 0.10, 0.00, 0.02, 1, 1024]
        # runner = MultiTestRunner(['RGC4'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC4 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC4(16)")

        # params_list = [16, 1, 6, 4, 1.0, 20000, 0.5, 0.10, 0.00, 0.01, 1, 1024]
        # runner = MultiTestRunner(['RGC4'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC4 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC4(17)")

        # params_list = [16, 1, 6, 4, 0.1, 20000, 0.5, 0.10, 0.00, 0.01, 1, 1024]
        # runner = MultiTestRunner(['RGC4'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC4 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC4(17b)")

        # params_list = [16, 1, 6, 4, 1.0, 20000, 0.5, 0.10, 0.00, 0.01, 1, 1024]
        # runner = MultiTestRunner(['RGC4'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC4 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC4(17c)")

        # params_list = [16, 1, 6, 4, 1.0, 20000, 0.5, 0.10, 0.00, 0.005, 1, 1024]
        # runner = MultiTestRunner(['RGC4'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC4 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC4(18)")

        # params_list = [16, 1, 6, 4, 1.0, 20000, 0.5, 0.10, 0.00, 0.001, 1, 1024]
        # runner = MultiTestRunner(['RGC4'], BUFFER_SIZE_LIST, trace_file, params_list)
        # rgc_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC4 {params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, rgc_result, "New-RGC4(19)")