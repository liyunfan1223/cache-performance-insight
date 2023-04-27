#!/usr/bin/env python
import sys
sys.path.append("/home/ubuntu22/cache-performance-insight")
from scripts.utils import SingleTestRunner, MultiTestRunner, BUFFER_LIST_FOR_TRACES, TRACES_LIST
import os
import matplotlib.pyplot as plt
import math
import numpy as np

plt.style.use('seaborn-v0_8-paper')

# print(matplotlib.l)
markers = ['o', 's', 'v', '^']
linestyles = ['dashed', ':', '-.', '--', '-', 'dashdot', 'dotted']

BUFFER_SIZES = [
    200,
    500,
    1000,
    2000
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

def LRFU_OLTP():
    for trace_name in ["OLTP"]:
        print("TRACE NAME:", trace_name)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.set_xlabel('Param (lambda)')
        ax.set_ylabel('Hit Ratio(%)')
        # ax.set_title(trace_name)
        ax.set_xscale('log')
        trace_file = f'traces/{trace_name}.lis'
        param_list = [math.pow(10, i) for i in np.arange(-6, 0, 0.1)]
        ax.set_xlim(param_list[0] / 2, param_list[-1] * 2)
        # PL = [math.pow(2, i) for i in np.arange(0, 9)]
        ax.set_xlim(param_list[0] / 2, param_list[-1] * 2)
        x = param_list
        for buffer_size in [1000, 2000, 5000, 10000, 15000]:
            hit_rate_list = []
            for half_life_ratio in param_list:
                runner = SingleTestRunner("LRFU", buffer_size, trace_file, [half_life_ratio, 1, 1])
                hit_rate = runner.get_hit_rate()
                hit_rate_list.append(hit_rate)
            ax.plot(param_list, hit_rate_list, label=f'{"LRFU"}_{buffer_size}', marker='+', linestyle='dashed')
        plt.legend(loc=2)
        fig_path = f'plots/3.1.2/{trace_name}_LRFU.png'
        plt.savefig(fig_path)
        print(f'Fig generated path: {fig_path}. ')

def LRFU_P1():
    for trace_name in ["P1"]:
        print("TRACE NAME:", trace_name)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.set_xlabel('Param (lambda)')
        ax.set_ylabel('Hit Ratio(%)')
        # ax.set_title(trace_name)
        ax.set_xscale('log')
        trace_file = f'traces/{trace_name}.lis'
        param_list = [math.pow(10, i) for i in np.arange(-6, 0, 0.1)]
        ax.set_xlim(param_list[0] / 2, param_list[-1] * 2)
        # PL = [math.pow(2, i) for i in np.arange(0, 9)]
        ax.set_xlim(param_list[0] / 2, param_list[-1] * 2)
        x = param_list
        for buffer_size in [8192, 16384, 32768, 65536, 131072]:
            hit_rate_list = []
            for half_life_ratio in param_list:
                runner = SingleTestRunner("LRFU", buffer_size, trace_file, [half_life_ratio, 1, 1])
                hit_rate = runner.get_hit_rate()
                hit_rate_list.append(hit_rate)
            ax.plot(param_list, hit_rate_list, label=f'{"LRFU"}_{buffer_size}', marker='+', linestyle='dashed')
        plt.legend(loc=2)
        fig_path = f'plots/3.1.2/{trace_name}_LRFU.png'
        plt.savefig(fig_path)
        print(f'Fig generated path: {fig_path}. ')

def EFSW_OLTP():
    for trace_name in ["OLTP"]:
        print("TRACE NAME:", trace_name)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.set_xlabel('Param (lambda)')
        ax.set_ylabel('Hit Ratio(%)')
        # ax.set_title(trace_name)
        ax.set_xscale('log')
        trace_file = f'traces/{trace_name}.lis'
        param_list = [math.pow(10, i) for i in np.arange(-2, 3, 0.1)]
        ax.set_xlim(param_list[0] / 2, param_list[-1] * 2)
        # PL = [math.pow(2, i) for i in np.arange(0, 9)]
        ax.set_xlim(param_list[0] / 2, param_list[-1] * 2)
        x = param_list
        for buffer_size in [1000, 2000, 5000, 10000, 15000]:
            hit_rate_list = []
            for half_life_ratio in param_list:
                runner = SingleTestRunner("EFSW", buffer_size, trace_file, [half_life_ratio, 1, 1])
                hit_rate = runner.get_hit_rate()
                hit_rate_list.append(hit_rate)
            ax.plot(param_list, hit_rate_list, label=f'{"EFSW"}_{buffer_size}', marker='+', linestyle='dashed')
        plt.legend(loc=2)
        fig_path = f'plots/3.1.2/{trace_name}_ESFW.png'
        plt.savefig(fig_path)
        print(f'Fig generated path: {fig_path}. ')

def EFSW_P1():
    for trace_name in ["P1"]:
        print("TRACE NAME:", trace_name)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.set_xlabel('Param (lambda)')
        ax.set_ylabel('Hit Ratio(%)')
        # ax.set_title(trace_name)
        ax.set_xscale('log')
        trace_file = f'traces/{trace_name}.lis'
        param_list = [math.pow(10, i) for i in np.arange(-2, 3, 0.1)]
        ax.set_xlim(param_list[0] / 2, param_list[-1] * 2)
        # PL = [math.pow(2, i) for i in np.arange(0, 9)]
        ax.set_xlim(param_list[0] / 2, param_list[-1] * 2)
        x = param_list
        for buffer_size in [8192, 16384, 32768, 65536, 131072]:
            hit_rate_list = []
            for half_life_ratio in param_list:
                runner = SingleTestRunner("EFSW", buffer_size, trace_file, [half_life_ratio, 1, 1])
                hit_rate = runner.get_hit_rate()
                hit_rate_list.append(hit_rate)
            ax.plot(param_list, hit_rate_list, label=f'{"ESFW"}_{buffer_size}', marker='+', linestyle='dashed')
        plt.legend(loc=2)
        fig_path = f'plots/3.1.2/{trace_name}_ESFW.png'
        plt.savefig(fig_path)
        print(f'Fig generated path: {fig_path}. ')

def COMBINE_OLTP():
    fig = plt.figure(figsize=(11, 4))
    fig.tight_layout()
    axes = fig.subplots(1, 2)
    ax = axes[0]
    ax.set_title("$\lambda$")
    # ax.set_xlabel('Param ($\lambda$)')
    for trace_name in ["OLTP"]:
        print("TRACE NAME:", trace_name)
        # fig, ax = plt.subplots(figsize=(10, 5))

        ax.set_ylabel('Hit Ratio(%)')
        ax.set_xscale('log')
        trace_file = f'traces/{trace_name}.lis'
        param_list = [math.pow(10, i) for i in np.arange(-6, 0, 0.1)]
        ax.set_xlim(param_list[0] / 2, param_list[-1] * 2)
        x = param_list
        for idx, buffer_size in enumerate([1000, 2000, 5000, 10000, 15000]):
            hit_rate_list = []
            for half_life_ratio in param_list:
                runner = SingleTestRunner("LRFU", buffer_size, trace_file, [half_life_ratio, 1, 1])
                hit_rate = runner.get_hit_rate()
                hit_rate_list.append(hit_rate)
            ax.plot(param_list, hit_rate_list, label=f'size={buffer_size}', marker='+', linestyle=linestyles[idx])
        # plt.legend(loc=2)
        # fig_path = f'plots/3.1.2/{trace_name}_LRFU.png'
        # plt.savefig(fig_path)
        # print(f'Fig generated path: {fig_path}. ')

    ax = axes[1]
    ax.set_title("$\lambda'$")
    for trace_name in ["OLTP"]:
        print("TRACE NAME:", trace_name)
        # ax.set_xlabel('Param ($\lambda$)')
        ax.set_ylabel('Hit Ratio(%)')
        # ax.set_title(trace_name)
        ax.set_xscale('log')
        trace_file = f'traces/{trace_name}.lis'
        param_list = [math.pow(10, i) for i in np.arange(-2, 3, 0.1)]
        ax.set_xlim(param_list[0] / 2, param_list[-1] * 2)
        x = param_list
        for idx, buffer_size in enumerate([1000, 2000, 5000, 10000, 15000]):
            hit_rate_list = []
            for half_life_ratio in param_list:
                runner = SingleTestRunner("EFSW", buffer_size, trace_file, [half_life_ratio, 1, 1])
                hit_rate = runner.get_hit_rate()
                hit_rate_list.append(hit_rate)
            ax.plot(param_list, hit_rate_list, label=f'size={buffer_size}', marker='+', linestyle=linestyles[idx])
        # plt.legend(loc=2)
        # fig_path = f'plots/3.1.2/{trace_name}_ESFW.png'
    fig_path =f'plots/3.1.2/OLTP_combine.png'
    plt.legend(loc=9, bbox_to_anchor=(-0.15, -0.065), ncol=5)
    plt.savefig(fig_path)
    print(f'Fig generated path: {fig_path}. ')

if __name__ == '__main__':
    # LRFU_OLTP()
    # EFSW_OLTP()

    COMBINE_OLTP()
    # LRFU_P1()
    # EFSW_P1()