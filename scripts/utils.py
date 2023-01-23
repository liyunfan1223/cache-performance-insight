import numpy as np
import cmd
import os
import matplotlib.pyplot as plt
import logging

TRACES_LIST = [
    'P1',
    'P2',
    'P3',
    'P4',
    'P5',
    'P6',
    'P7',
    'P12',
    'OLTP',
    'DS1',
]


class Recorder:
    pass


class SingleTestRunner:
    EXECUTION_PATH = './build/src/main'
    START_POSITION = len('hit_rate:')

    def __init__(self, cache_policy=None, buffer_size=None, trace_file=None, params=None):
        self.cache_policy = cache_policy
        self.buffer_size = buffer_size
        self.trace_File = trace_file
        self.params = params

    def get_hit_rate(self):
        cmdline = self.EXECUTION_PATH + f" {self.cache_policy} {self.buffer_size} {self.trace_File}"
        if self.params is not None:
            for param in self.params:
                cmdline += f" {param}"
        # print('cmdline: ', cmdline)
        res = os.popen(cmdline).read().strip()
        print(res)
        return res.split()[-1][self.START_POSITION:-1]


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
        print('hit rate list: ', hit_rate_list)
        return hit_rate_list
