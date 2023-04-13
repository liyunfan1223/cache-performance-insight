#!/usr/bin/env python

from utils import SingleTestRunner, MultiTestRunner, BUFFER_LIST_FOR_TRACES, TRACES_LIST
import os
import matplotlib.pyplot as plt
import math
import numpy as np

BUFFER_SIZES = [
    # 200,
    # 500,
    # 1000,
    # 2000
    2 ** 12,
    2 ** 14,
    2 ** 15,
    2 ** 16,
    2 ** 17,
]
CACHE_POLICY = 'GLRFU3'
TRACE_FILES = [
    # 'Home1',
    'P1',
    'P2',
    'P3',
    'P4',
    'P5',
    'P6',
    'P7',
    'P12',
    'OLTP',
    'DS1'
]
PARAM_START = -2
PARAM_END = 3
PARAM_LIST = [math.pow(10, i) for i in np.arange(PARAM_START, PARAM_END + 1, 0.1)]


def optimizer_arc_prior(cache_policy=None, buffer_size=None, trace_name=None, ax=None):
    trace_file = f'traces/{trace_name}.lis'

    hit_rate_list = []
    for param in PARAM_LIST:
        single_test_runner = SingleTestRunner(cache_policy=cache_policy, buffer_size=buffer_size, trace_file=trace_file,
                                              params=[param, 1, 1])
        hit_rate = single_test_runner.get_hit_rate()
        hit_rate_list.append(hit_rate)

    ax.plot(PARAM_LIST, hit_rate_list, label=f'{cache_policy}_{buffer_size}', marker='+', linestyle='dashed')

def optimizer_glrfu4(cache_policy=None, buffer_size=None, trace_name=None, ax=None):
    trace_file = f'traces/{trace_name}.lis'

    hit_rate_list = []
    PL = [math.pow(2, i) for i in np.arange(0, 9)]
    for param in PL:
        single_test_runner = SingleTestRunner(cache_policy=cache_policy, buffer_size=buffer_size, trace_file=trace_file,
                                              params=[20000, 20, 0.5, 5, 4, 10, 4, param])
        hit_rate = single_test_runner.get_hit_rate()
        hit_rate_list.append(hit_rate)

    ax.plot(PL, hit_rate_list, label=f'{cache_policy}_{buffer_size}', marker='+', linestyle='dashed')

def EFSW():
    for trace_name in TRACES_LIST:
        print("TRACE NAME:", trace_name)
        fig, ax = plt.subplots(figsize=(14, 7))
        ax.set_xlabel('Param (lambda)')
        ax.set_ylabel('Hit Ratio(%)')
        ax.set_title(trace_name)
        ax.set_xscale('log')
        trace_file = f'traces/{trace_name}.lis'
        ax.set_xlim(PARAM_LIST[0] / 2, PARAM_LIST[-1] * 2)
        # PL = [math.pow(2, i) for i in np.arange(0, 9)]
        ax.set_xlim(PARAM_LIST[0] / 2, PARAM_LIST[-1] * 2)
        for buffer_size in BUFFER_LIST_FOR_TRACES[trace_name]:
            print("BUFFER SIZE:", buffer_size)
            # optimizer_arc_prior(CACHE_POLICY, buffer_size, trace_name, ax)
            optimizer_arc_prior('EFSW', buffer_size, trace_name, ax)
        plt.legend(loc=2)
        if not os.path.exists('local'):
            os.mkdir('local')
        fig_path = f'local/param_plot_{trace_name}_{CACHE_POLICY}.png'
        plt.savefig(fig_path)
        print(f'Fig generated path: {fig_path}. ')

def glrfu4():
    for trace_name in TRACES_LIST:
        print("TRACE NAME:", trace_name)
        fig, ax = plt.subplots(figsize=(14, 7))
        ax.set_xlabel('Param (lambda)')
        ax.set_ylabel('Hit Ratio(%)')
        ax.set_title(trace_name)
        ax.set_xscale('log')
        trace_file = f'traces/{trace_name}.lis'
        # ax.set_xlim(PARAM_LIST[0] / 2, PARAM_LIST[-1] * 2)
        PL = [math.pow(2, i) for i in np.arange(0, 9)]
        ax.set_xlim(PL[0] / 2, PL[-1] * 2)
        for buffer_size in BUFFER_LIST_FOR_TRACES[trace_name]:
            print("BUFFER SIZE:", buffer_size)
            # optimizer_arc_prior(CACHE_POLICY, buffer_size, trace_name, ax)
            optimizer_glrfu4('GLRFU3', buffer_size, trace_name, ax)
        plt.legend(loc=2)
        if not os.path.exists('local'):
            os.mkdir('local')
        fig_path = f'local/param_plot_{trace_name}_{CACHE_POLICY}.png'
        plt.savefig(fig_path)
        print(f'Fig generated path: {fig_path}. ')


if __name__ == '__main__':
    EFSW()