#!/usr/bin/env python
import os
import matplotlib.pyplot as plt
from utils import SingleTestRunner, MultiTestRunner, TRACES_LIST, BUFFER_LIST_FOR_TRACES, StatisticsCompareLRU

# CACHE_POLICY_LIST = [
#     'LRU'
# ]
# MIN_BUFFER_SIZE = 11
# MAX_BUFFER_SIZE = 18
# MIN_BUFFER_SIZE = -6
MIN_BUFFER_SIZE = -3
MAX_BUFFER_SIZE = 4
BASIC_BUFFER_SIZE_LIST = [(0.01 * (2 ** k)) for k in range(MIN_BUFFER_SIZE, MAX_BUFFER_SIZE + 1)]
# BUFFER_SIZE_LIST = [0.000625, 0.00125, 0.0025, 0.005, 0.01, 0.02, 0.04, 0.08]
# BUFFER_SIZE_LIST = [0.4]
PREFIX = '1008'
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

        srrip_runner = MultiTestRunner(['SRRIP'], BUFFER_SIZE_LIST, trace_file, None)
        srrip_result = srrip_runner.get_hit_rate_list()
        ax.plot(BUFFER_SIZE_LIST, srrip_result, label='SRRIP', marker='+', linestyle='dashed')
        stats.statistic(lru_result, srrip_result, "SRRIP")

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
        # params_list = [20000, 5, 0.1, 5, -1, 1, 1]
        # runner = MultiTestRunner(['ALRFU5'], BUFFER_SIZE_LIST, trace_file, params_list)
        # alrfu_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, alrfu_result, label=f'ALRFU5, p={params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, alrfu_result, "A-LRFU")

        #
        # params_list = [20000, 5, 0.1, 5, 8, 1, 1]
        # runner = MultiTestRunner(['ALRFU5'], BUFFER_SIZE_LIST, trace_file, params_list)
        # alrfu_limit_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, alrfu_limit_result, label=f'ALRFU5, p={params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, alrfu_limit_result, "ALRFU5-limited")

        # params_list = [20000, 5, 1.0, 1, 8, 10]
        # runner = MultiTestRunner(['GLRFU'], BUFFER_SIZE_LIST, trace_file, params_list)
        # glrfu_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, glrfu_result, label=f'GLRFU, p={params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, glrfu_result, "GLRFU")
        #
        # params_list = [20000, 10, 0.5, 5, 4, 10]
        # runner = MultiTestRunner(['GLRFU'], BUFFER_SIZE_LIST, trace_file, params_list)
        # glrfu_higher_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, glrfu_higher_result, label=f'GLRFU, p={params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, glrfu_higher_result, "GLRFU_HIGHER")
        #
        # params_list = [20000, 10, 0.3, 5, 4, 10]
        # runner = MultiTestRunner(['GLRFU'], BUFFER_SIZE_LIST, trace_file, params_list)
        # glrfu_result_p3 = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, glrfu_result_p3, label=f'GLRFU, p={params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, glrfu_result_p3, "GLRFU_P3")
        #
        # params_list = [20000, 10, 0.3, 5, 4, 10, 8]
        # runner = MultiTestRunner(['GLRFU2'], BUFFER_SIZE_LIST, trace_file, params_list)
        # glrfu2_8r_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, glrfu2_8r_result, label=f'GLRFU2, p={params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, glrfu2_8r_result, "GLRFU2_8r")
        #
        # params_list = [20000, 10, 0.25, 5, 4, 10, 4]
        # runner = MultiTestRunner(['GLRFU2'], BUFFER_SIZE_LIST, trace_file, params_list)
        # glrfu2_4r_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, glrfu2_4r_result, label=f'GLRFU2, p={params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, glrfu2_4r_result, "GLRFU2_4r")
        #
        # params_list = [20000, 10, 1.0, 5, 4, 10, 4]
        # runner = MultiTestRunner(['GLRFU2'], BUFFER_SIZE_LIST, trace_file, params_list)
        # glrfu2_a_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, glrfu2_a_result, label=f'GLRFU2, p={params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, glrfu2_a_result, "GLRFU2_a")
        #
        # params_list = [20000, 10, 0.5, 5, 4, 10, 4]
        # runner = MultiTestRunner(['GLRFU2'], BUFFER_SIZE_LIST, trace_file, params_list)
        # glrfu2_b_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, glrfu2_b_result, label=f'GLRFU2, p={params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, glrfu2_b_result, "GLRFU2_b")

        # params_list = [20000, 10, 0.5, 5, 4, 10, 2]
        # runner = MultiTestRunner(['GLRFU2'], BUFFER_SIZE_LIST, trace_file, params_list)
        # glrfu2_c_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, glrfu2_c_result, label=f'GLRFU2, p={params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, glrfu2_c_result, "GLRFU2_c")

        # params_list = [20000, 10, 0.5, 5, 4, 10, 1]
        # runner = MultiTestRunner(['GLRFU2'], BUFFER_SIZE_LIST, trace_file, params_list)
        # glrfu2_d_result = runner.get_hit_rate_list()
        # ax.plot(BUFFER_SIZE_LIST, glrfu2_d_result, label=f'GLRFU2, p={params_list}', marker='+', linestyle='-')
        # stats.statistic(lru_result, glrfu2_d_result, "GLRFU2_d")

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

        params_list = [20000, 20, 0.5, 1.0, 4, 10, 4]
        # params_list = [1000, 4, 0.3, 1, 32, 10, 8]
        runner = MultiTestRunner(['GLRFU2'], BUFFER_SIZE_LIST, trace_file, params_list)
        glrfu2_f_result = runner.get_hit_rate_list()
        ax.plot(BUFFER_SIZE_LIST, glrfu2_f_result, label=f'GLRFU2, p={params_list}', marker='+', linestyle='dotted')
        stats.statistic(lru_result, glrfu2_f_result, f"GLRFU-{params_list}")

        params_list = [20000, 20, 0.5, 1.0, 1, 6, 4]
        # params_list = [1000, 4, 0.3, 1, 32, 10, 8]
        runner = MultiTestRunner(['GLRFU2'], BUFFER_SIZE_LIST, trace_file, params_list)
        glrfu2_f_result = runner.get_hit_rate_list()
        ax.plot(BUFFER_SIZE_LIST, glrfu2_f_result, label=f'GLRFU2, p={params_list}', marker='+', linestyle='dotted')
        stats.statistic(lru_result, glrfu2_f_result, f"GLRFU-{params_list}")

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

        params_list = [20, 1, 6, 4, 1.0, 20000, 0.5, 0.01, 0.00, 5, 1, 1024]
        runner = MultiTestRunner(['RGC3'], BUFFER_SIZE_LIST, trace_file, params_list)
        rgc_result = runner.get_hit_rate_list()
        ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC3 {params_list}', marker='+', linestyle='-')
        stats.statistic(lru_result, rgc_result, "New-RGC3(10)")

        params_list = [20, 1, 7, 4, 1.0, 20000, 0.5, 0.01, 0.00, 5, 1, 1024]
        runner = MultiTestRunner(['RGC3'], BUFFER_SIZE_LIST, trace_file, params_list)
        rgc_result = runner.get_hit_rate_list()
        ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC3 {params_list}', marker='+', linestyle='-')
        stats.statistic(lru_result, rgc_result, "New-RGC3(14)")

        params_list = [20, 1, 6, 4, 1.0, 20000, 0.5, 0.00, 0.00, 5, 1, -1]
        runner = MultiTestRunner(['RGC3'], BUFFER_SIZE_LIST, trace_file, params_list)
        rgc_result = runner.get_hit_rate_list()
        ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC3 {params_list}', marker='+', linestyle='-')
        stats.statistic(lru_result, rgc_result, "New-RGC3(17)")

        params_list = [20, 1, 6, 4, 1.0, 20000, 0.5, 0.00, 0.00, 5, 1, -1]
        runner = MultiTestRunner(['RGC'], BUFFER_SIZE_LIST, trace_file, params_list)
        rgc_result = runner.get_hit_rate_list()
        ax.plot(BUFFER_SIZE_LIST, rgc_result, label=f'RGC {params_list}', marker='+', linestyle='-')
        stats.statistic(lru_result, rgc_result, "New-RGC(17)")

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
        plt.legend(loc=4)
        if not os.path.exists('local'):
            os.mkdir('local')
        fig_path = f'local/{PREFIX}_plot_{trace}.png'
        # fig_path = 'local/plot.png'
        plt.savefig(fig_path)
        print(f'Fig generated path: {fig_path}. ')
        stats.print_result()

