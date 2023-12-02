import numpy as np
import cmd
import os
import matplotlib.pyplot as plt
import logging
import json
from collections import defaultdict

TRACES_LIST = [
    # 'P1',
    # 'P2',
    # 'P3',
    # 'P4',
    # 'P5',
    # 'P6',
    # 'P7',
    # 'P12',
    # "Rocks1",
    # 'lun2',

    # 'webmail',
    # 'websearch',
    'webusers',
    'online',
    # 'Home1',
    # 'Home2',
    # 'Home3',
    # 'Home4',
    #
    # "cloudvps26107",
    # "cloudvps26391",
    # 'cloudvps26136',
    # 'cloudvps26148',
    # 'cloudvps26215',
    # 'cloudvps26255',
    # 'cloudvps26330',
    # 'cloudvps26511',
    # # #
    # 'msr_usr_0',
    # 'msr_proj_0',
    # 'msr_prn_0',
    # 'msr_hm_0',
    # 'msr_rsrch_0',
    # 'msr_prxy_0',
    # 'msr_src2_0',
    # 'msr_stg_0',
    # 'msr_ts_0',
    # 'msr_web_0',
    # 'msr_mds_0',
    # 'msr_wdev_0',

    # #
    # # 'msr_proj_0_1d',
    # # 'msr_prxy_0_1d',
    # # 'msr_wdev_0_1d',
    # # 'msr_stg_0_1d',
    # # 'msr_mds_0_1d',
    # # 'msr_web_0_1d',
    # # 'msr_hm_0_1d',
    # # # # #
    # # # #
    # # # # # # # # # # #
    # 'DS1',
    # 'OLTP',
    #


    #
    # #
    # # #

    # #
    # # #
    # # #
    # #
    # # #MSR
    # # # # 'msr_proj_1_1d', # TOO LARGE?
    # 'msr_usr_1_1d', # TOO LARGE
    # 'msr_usr_1', # TOO LARGE
    # # # # FIU
    # # #
    # 'readrandom_5',
    # 'readrandom_6',
    # 'readrandom_7',
    # # # 'readseq_3',
    # # 'randseq_1',
    # # #
    # # # # 'msr_usr_1_sample',
    # # #
    # # # # 'Rocks4',
    # # # # 'Rocks5',
    # # # # 'Rocks6',
    # # # # 'Rocks7',
    # # # # 'Rocks8',

]
BUFFER_LIST_FOR_TRACES = {
    'P1': [2 ** k for k in range(11, 18 + 1)],
    'P2': [2 ** k for k in range(11, 18 + 1)],
    'P3': [2 ** k for k in range(11, 18 + 1)],
    'P4': [2 ** k for k in range(11, 18 + 1)],
    'P5': [2 ** k for k in range(11, 18 + 1)],
    'P6': [2 ** k for k in range(11, 18 + 1)],
    'P7': [2 ** k for k in range(11, 18 + 1)],
    'P12': [2 ** k for k in range(11, 18 + 1)],
    'OLTP': [2 ** k for k in range(5, 15 + 1)],
    # 'DS1': [2 ** k for k in range(18, 24 + 1)],

    # 'Home1': [2 ** k for k in range(4, 12 + 1)],
    # 'Home2': [2 ** k for k in range(4, 12 + 1)],
    # 'Home4': [2 ** k for k in range(4, 18 + 1)],
    # 'readrandom_5': [2 ** k for k in range(5, 13 + 1)],
    # 'readrandom_6': [2 ** k for k in range(5, 13 + 1)],
    # 'readrandom_7': [2 ** k for k in range(5, 13 + 1)],
    # 'readseq_1': [2 ** k for k in range(3, 10 + 1)],
    # 'readseq_2': [2 ** k for k in range(3, 10 + 1)],
    # 'readseq_3': [2 ** k for k in range(3, 10 + 1)],
    # 'randseq_1': [2 ** k for k in range(5, 13 + 1)],
    # 'Rocks1': [2 ** k for k in range(21, 25 + 1)],
    # 'Rocks2': [2 ** k for k in range(21, 25 + 1)],
    # 'Rocks3': [2 ** k for k in range(21, 25 + 1)],
    # 'Rocks4': [2 ** k for k in range(21, 25 + 1)],
    # 'Rocks5': [2 ** k for k in range(21, 25 + 1)],
    # 'Rocks6': [2 ** k for k in range(21, 25 + 1)],
    # 'Rocks7': [2 ** k for k in range(21, 25 + 1)],
    # 'Rocks8': [2 ** k for k in range(21, 25 + 1)],
    # # 'Rocks9': [2 ** k for k in range(21, 25 + 1)],
    # # 'Rocks10': [2 ** k for k in range(21, 25 + 1)],
    # 'msr_hm_0': [2 ** k for k in range(10, 22 + 1)],
    # 'msr_prxy_0': [2 ** k for k in range(10, 22 + 1)],
    # 'msr_proj_0': [2 ** k for k in range(10, 22 + 1)],
    # 'msr_proj_1': [2 ** k for k in range(16, 26 + 1)],
    # 'msr_web_0': [2 ** k for k in range(10, 22 + 1)],
    # 'msr_mds_0': [2 ** k for k in range(10, 22 + 1)],
    # 'msr_stg_0': [2 ** k for k in range(10, 22 + 1)],
    # 'msr_usr_1': [2 ** k for k in range(16, 20 + 1)],
    # 'msr_usr_1_sample': [2 ** k for k in range(16, 20 + 1)],
    # # 'msr_usr_1': [2 ** k for k in range(10, 22 + 1)],
    # 'websearch': [2 ** k for k in range(2, 16)],
    # 'webusers': [2 ** k for k in range(2, 16)],
}

class Recorder:
    pass


class SingleTestRunner:
    # EXECUTION_PATH = './build/src/main'
    execution_path = './'
    START_POSITION = len('hit_rate:')
    # CACHE_FILE_PATH = 'local/single_test_runner_cache.json'

    def __init__(self, cache_policy=None, buffer_size=None, trace_file=None, params=None, execution_path = './build/src/main', cache_file_path='local/single_test_runner_cache.json'):
        self.cache_policy = cache_policy
        self.buffer_size = buffer_size
        self.trace_file = trace_file
        self.params = params
        self.cache_file_path = cache_file_path
        self.execution_path = execution_path

    def make_cache_key_string(self):
        return str(self.cache_policy) + '_' + str(self.buffer_size) + '_' + \
            str(self.trace_file) + '_' + str(self.params)

    def get_hit_rate(self, read_cache=True, write_cache=True):
        if read_cache and os.path.exists(self.cache_file_path):
            with open(self.cache_file_path, 'r') as f:
                data: dict = json.load(f)
            if self.make_cache_key_string() in data.keys():
                return data[self.make_cache_key_string()]
        cmdline = self.execution_path + f" {self.cache_policy} {self.buffer_size} {self.trace_file}"
        if self.params is not None:
            for param in self.params:
                cmdline += f" {param}"
        print('cmdline: ', cmdline)
        res = os.popen(cmdline).read().strip()
        print('No cache can be used. Result: ', res)
        if write_cache:
            if os.path.exists(self.cache_file_path):
                with open(self.cache_file_path, 'r') as f:
                    data: dict = json.load(f)
            else:
                data = dict()
            data[self.make_cache_key_string()] = float(res.split()[-1][self.START_POSITION:-1])
            with open(self.cache_file_path, 'w') as f:
                json.dump(data, f)
            print(f'Result saved in cache file. key:{self.make_cache_key_string()}')
        return float(res.split()[-1][self.START_POSITION:-1])

    def get_outputs(self):
        cmdline = self.execution_path + f" {self.cache_policy} {self.buffer_size} {self.trace_file}"
        if self.params is not None:
            for param in self.params:
                cmdline += f" {param}"
        print('cmdline: ', cmdline)
        res = os.popen(cmdline).read().strip()
        return res
class MultiTestRunner:

    def __init__(self, cache_policy_list=None, buffer_size_list=None, trace_file=None, params=None):
        self.cache_policy_list = cache_policy_list
        self.buffer_size_list = buffer_size_list
        self.trace_file = trace_file
        self.params = params

    def get_hit_rate_list(self):
        hit_rate_list = []
        for cache_policy in self.cache_policy_list:
            for buffer_size in self.buffer_size_list:
                single_test_runner = SingleTestRunner(cache_policy, buffer_size, self.trace_file, self.params)
                hit_rate_list.append(single_test_runner.get_hit_rate())
        hit_rate_list = [float(hit_rate) for hit_rate in hit_rate_list]
        print('Multi Test Runner Start:')
        print('\tcache policy list: ', self.cache_policy_list,
              '\n\tbuffer size list', self.buffer_size_list,
              '\n\ttrace file', self.trace_file,
              '\n\tparams params', self.params,
              '\n\thit rate list: ', hit_rate_list)
        return hit_rate_list

    def get_miss_rate_list(self):
        hit_rate_list = self.get_hit_rate_list()
        miss_rate_list = [(100 - x) for x in hit_rate_list]
        return miss_rate_list
class StatisticsCompareLRU:

    def __init__(self):
        self.data = defaultdict()
        self.count = defaultdict()
        self.perf = defaultdict()
        self.lru = None

    def statistic(self, lru_result, compared_result, compared_label='default'):
        self.lru = lru_result
        for lru, compared in zip(lru_result, compared_result):
            if lru == 0:
                ratio = 0
            else:
                ratio = (compared - lru) / lru
            perf = (100 - lru) / (100 - compared) - 1
            if compared_label in self.data:
                self.data[compared_label] += ratio
                self.perf[compared_label] += perf
                self.count[compared_label] += 1
            else:
                self.data[compared_label] = ratio
                self.perf[compared_label] = perf
                self.count[compared_label] = 1

    def print_result(self):
        # print(f"LRU average hit rate: {sum(self.lru) / len(self.lru)}%")
        for label in self.data.keys():
            print(f"Performance rate of {label}: {self.perf[label] / self.count[label] * 100}% average higher than lru.")
        for label in self.data.keys():
            print(f"Hit rate of {label}: {self.data[label] / self.count[label] * 100}% average higher than lru.")
