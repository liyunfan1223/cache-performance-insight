import numpy as np
import cmd
import os
import matplotlib.pyplot as plt
import logging
import json

TRACES_LIST = [
    'OLTP',
    'Home1',
    'Home2',
    'P1',
    'P2',
    'P3',
    'P4',
    'P5',
    'P6',
    'P7',
    'P12',
    'DS1',
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
    'OLTP': [2 ** k for k in range(3, 13 + 1)],
    'DS1': [2 ** k for k in range(18, 22 + 1)],
    'Home1': [2 ** k for k in range(4, 12 + 1)],
    'Home2': [2 ** k for k in range(4, 12 + 1)],
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
        print('Not use cache. Result: ', res)
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
