#!/usr/bin/env python3
import numpy as np
import cmd
import os
import matplotlib.pyplot as plt
import logging


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
        res = os.popen(cmdline).read().strip()
        print(res)
        return res.split()[-1][self.START_POSITION:-1]


class MultiTestRunner:

    def __init__(self, cache_policy_list=None, buffer_size_list=None, trace_file_list=None, params_list=None):
        self.cache_policy_list = cache_policy_list
        self.buffer_size_list = buffer_size_list
        self.trace_file_list = trace_file_list
        self.params_list = params_list

    def get_hit_rate_list(self):
        hit_rate_list = []
        for cache_policy in self.cache_policy_list:
            for trace_file in self.trace_file_list:
                for buffer_size, params in zip(self.buffer_size_list, self.params_list):
                    single_test_runner = SingleTestRunner(cache_policy, buffer_size, trace_file, params)
                    hit_rate_list.append(single_test_runner.get_hit_rate())
        hit_rate_list = [float(hit_rate) for hit_rate in hit_rate_list]
        print('hit rate list: ', hit_rate_list)
        return hit_rate_list


CACHE_POLICY_LIST = [
    'LRU'
]
MIN_BUFFER_SIZE = 10
MAX_BUFFER_SIZE = 18
BUFFER_SIZE_LIST = [2 ** k for k in range(MIN_BUFFER_SIZE, MAX_BUFFER_SIZE + 1)]
TRACE_FILE_LIST = [
    'traces/P1.lis'
]
PARAMS_LIST = [None] * len(BUFFER_SIZE_LIST)


if __name__ == '__main__':

    fig, ax = plt.subplots(figsize=(14, 7))
    ax.set_ylim(0, 100)
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels([20, 40, 60, 80, 100])
    ax.set_xlabel('BUFFER SIZE')
    ax.set_ylabel('HIT RATE(%)')
    lru_runner = MultiTestRunner(['LRU'], BUFFER_SIZE_LIST, TRACE_FILE_LIST, [None] * len(BUFFER_SIZE_LIST))
    lru_result = lru_runner.get_hit_rate_list()
    ax.plot(BUFFER_SIZE_LIST, lru_result, label='LRU')

    lfu_runner = MultiTestRunner(['LFU'], BUFFER_SIZE_LIST, TRACE_FILE_LIST, [None] * len(BUFFER_SIZE_LIST))
    lfu_result = lfu_runner.get_hit_rate_list()
    ax.plot(BUFFER_SIZE_LIST, lfu_result, label='LFU')

    arc_runner = MultiTestRunner(['ARC'], BUFFER_SIZE_LIST, TRACE_FILE_LIST, [None] * len(BUFFER_SIZE_LIST))
    arc_result = arc_runner.get_hit_rate_list()
    ax.plot(BUFFER_SIZE_LIST, arc_result, label='ARC')

    ff_runner = MultiTestRunner(['FF'], BUFFER_SIZE_LIST, TRACE_FILE_LIST, [None] * len(BUFFER_SIZE_LIST))
    ff_result = ff_runner.get_hit_rate_list()
    ax.plot(BUFFER_SIZE_LIST, ff_result, label='FF')

    params_list = [[k - 1] for k in BUFFER_SIZE_LIST]
    prior_freq_runner = MultiTestRunner(['ARC_3'], BUFFER_SIZE_LIST, TRACE_FILE_LIST, params_list)
    prior_freq_result = prior_freq_runner.get_hit_rate_list()
    ax.plot(BUFFER_SIZE_LIST, prior_freq_result, label='PriorFreq')

    params_list = [[k // 2] for k in BUFFER_SIZE_LIST]
    arc_prior_freq_runner = MultiTestRunner(['ARC_3'], BUFFER_SIZE_LIST, TRACE_FILE_LIST, params_list)
    arc_prior_freq_result = arc_prior_freq_runner.get_hit_rate_list()
    ax.plot(BUFFER_SIZE_LIST, arc_prior_freq_result, label='ARC + PriorFreq')

    plt.legend()
    if not os.path.exists('local'):
        os.mkdir('local')
    plt.savefig('local/plot.png')
