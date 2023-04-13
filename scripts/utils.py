import numpy as np
import cmd
import os
import matplotlib.pyplot as plt
import logging
import json
from collections import defaultdict

TRACES_LIST = [
    # 'OLTP',
    # 'P1',
    # 'P2',
    # 'P3',
    'P4',
    'P5',
    # 'P6',
    # 'P7',
    # 'P12',
    # 'DS1',
    # 'readrandom_5',
    # 'readrandom_6',
    # 'readrandom_7',
    # 'readseq_1',
    # 'readseq_2',
    # 'readseq_3',
    # 'randseq_1',
    # 'Rocks1',
    # 'Rocks2',
    # 'Rocks3',
    # 'Rocks4',
    # 'Rocks5',
    # 'Rocks6',
    # 'Rocks7',
    # 'Rocks8',
]
# 'Home1',
# 'Home2',
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
    'DS1': [2 ** k for k in range(18, 24 + 1)],
    'Home1': [2 ** k for k in range(4, 12 + 1)],
    'Home2': [2 ** k for k in range(4, 12 + 1)],
    'readrandom_5': [2 ** k for k in range(5, 13 + 1)],
    'readrandom_6': [2 ** k for k in range(5, 13 + 1)],
    'readrandom_7': [2 ** k for k in range(5, 13 + 1)],
    'readseq_1': [2 ** k for k in range(3, 10 + 1)],
    'readseq_2': [2 ** k for k in range(3, 10 + 1)],
    'readseq_3': [2 ** k for k in range(3, 10 + 1)],
    'randseq_1': [2 ** k for k in range(5, 13 + 1)],
    'Rocks1': [2 ** k for k in range(21, 25 + 1)],
    'Rocks2': [2 ** k for k in range(21, 25 + 1)],
    'Rocks3': [2 ** k for k in range(21, 25 + 1)],
    'Rocks4': [2 ** k for k in range(21, 25 + 1)],
    'Rocks5': [2 ** k for k in range(21, 25 + 1)],
    'Rocks6': [2 ** k for k in range(21, 25 + 1)],
    'Rocks7': [2 ** k for k in range(21, 25 + 1)],
    'Rocks8': [2 ** k for k in range(21, 25 + 1)],
    # 'Rocks9': [2 ** k for k in range(21, 25 + 1)],
    # 'Rocks10': [2 ** k for k in range(21, 25 + 1)],
}

class Recorder:
    pass


class SingleTestRunner:
    EXECUTION_PATH = './build/src/main'
    START_POSITION = len('hit_rate:')
    CACHE_FILE_PATH = 'local/single_test_runner_cache.json'

    def __init__(self, cache_policy=None, buffer_size=None, trace_file=None, params=None):
        self.cache_policy = cache_policy
        self.buffer_size = buffer_size
        self.trace_file = trace_file
        self.params = params

    def make_cache_key_string(self):
        return str(self.cache_policy) + '_' + str(self.buffer_size) + '_' + \
            str(self.trace_file) + '_' + str(self.params)

    def get_hit_rate(self, read_cache=True, write_cache=True):
        if read_cache and os.path.exists(self.CACHE_FILE_PATH):
            with open(self.CACHE_FILE_PATH, 'r') as f:
                data: dict = json.load(f)
            if self.make_cache_key_string() in data.keys():
                return data[self.make_cache_key_string()]
        cmdline = self.EXECUTION_PATH + f" {self.cache_policy} {self.buffer_size} {self.trace_file}"
        if self.params is not None:
            for param in self.params:
                cmdline += f" {param}"
        print('cmdline: ', cmdline)
        res = os.popen(cmdline).read().strip()
        print('No cache can be used. Result: ', res)
        if write_cache:
            if os.path.exists(self.CACHE_FILE_PATH):
                with open(self.CACHE_FILE_PATH, 'r') as f:
                    data: dict = json.load(f)
            else:
                data = dict()
            data[self.make_cache_key_string()] = float(res.split()[-1][self.START_POSITION:-1])
            with open(self.CACHE_FILE_PATH, 'w') as f:
                json.dump(data, f)
            print(f'Result saved in cache file. key:{self.make_cache_key_string()}')
        return float(res.split()[-1][self.START_POSITION:-1])


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

class StatisticsCompareLRU:

    def __init__(self):
        self.data = defaultdict()
        self.count = defaultdict()
        self.perf = defaultdict()

    def statistic(self, lru_result, compared_result, compared_label='default'):
        for lru, compared in zip(lru_result, compared_result):
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
        for label in self.data.keys():
            # print(f"Hit rate of {label}: {self.data[label] / self.count[label] * 100}% average higher than lru.")
            print(f"Performance rate of {label}: {self.perf[label] / self.count[label] * 100}% average higher than lru.")