#!/usr/bin/env python
import sys
sys.path.append("/home/ubuntu22/cache-performance-insight")
from scripts.utils import SingleTestRunner, MultiTestRunner, BUFFER_LIST_FOR_TRACES, TRACES_LIST
import os
import matplotlib.pyplot as plt
import math
import numpy as np
from matplotlib.ticker import FuncFormatter

def format_func(value, tick_number):
    return int(value)

plt.style.use('seaborn-v0_8-paper')

# print(matplotlib.l)
markers = ['o', 's', 'v', '^']
linestyles = ['dashed', ':', '-.', '--', '-', 'dashdot', 'dotted']
cache_file_path = 'local/decay_rate_hitratio.json'

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

colors = ['#c44e52', '#8172b2', '#ccb974', '#86a38d', '#4c90b0', '#55a868', '#757272', '#78cbe3']

def COMBINE_OLTP():
    # fig = plt.figure()

    fig, axes = plt.subplots(1, 2, figsize=(7, 3))
    ax = axes[0]
    # ax.set_title("$\lambda$")
    ax.set_xlabel("(a) Parameter with $\lambda$", fontsize=12)
    ax.yaxis.set_major_formatter(FuncFormatter(format_func))
    # ax.set_xlabel('Param ($\lambda$)')
    for trace_name in ["Home4"]:
        print("TRACE NAME:", trace_name)
        # fig, ax = plt.subplots(figsize=(10, 5))

        ax.set_ylabel('Hit Rate(%)', fontsize=12)
        ax.set_xscale('log')
        trace_file = f'traces/{trace_name}.lis'
        param_list = [math.pow(10, i) for i in np.arange(-6, 0, 0.1)]
        ax.set_xlim(param_list[0] / 2, param_list[-1] * 2)
        x = param_list
        for idx, buffer_size in enumerate([200, 1000, 2000, 4000]): #([0.001, 0.005, 0.01, 0.02]):#, 0.05, 0.1, 0.2]):
            hit_rate_list = []
            max_half = 0
            max_hr = 0
            for half_life_ratio in param_list:
                runner = SingleTestRunner("LRFU", buffer_size, trace_file, [half_life_ratio, 1, 1], cache_file_path=cache_file_path)
                hit_rate = runner.get_hit_rate()
                hit_rate_list.append(hit_rate)
                if hit_rate > max_hr:
                    max_hr = hit_rate
                    max_half = half_life_ratio
            ax.plot(param_list, hit_rate_list, label=f'c = {buffer_size}', linestyle=linestyles[idx], color=colors[idx])
            ax.scatter(max_half, max_hr, color=colors[idx], marker='^')
    ax.legend(loc="upper right")
    # plt.tight_layout()
    # plt.subplots_adjust(bottom=0.18)
    # fig_path =f'plots/D2.1/1'
    # plt.savefig(f'{fig_path}.png')
    # plt.savefig(f'{fig_path}.eps')
    # print(f'Fig generated path: {fig_path}. ')
        # plt.legend(loc=2)
        # fig_path = f'plots/3.1.2/{trace_name}_LRFU.png'
        # plt.savefig(fig_path)
        # print(f'Fig generated path: {fig_path}. ')

    # fig, ax = plt.subplots(figsize=(3.5, 3))
    ax = axes[1]
    ax.yaxis.set_major_formatter(FuncFormatter(format_func))
    ax.set_xlabel(r"(b) Parameter with $R=\frac{1}{\lambda \times c}$", fontsize=12)
    for trace_name in ["Home4"]:
        print("TRACE NAME:", trace_name)
        # ax.set_xlabel('Param ($\lambda$)')
        ax.set_ylabel('Hit Rate(%)', fontsize=12)
        # ax.set_title(trace_name)
        ax.set_xscale('log')
        trace_file = f'traces/{trace_name}.lis'
        param_list = [math.pow(10, i) for i in np.arange(-2, 4, 0.1)]
        ax.set_xlim(param_list[0] / 2, param_list[-1] * 2)
        x = param_list
        for idx, buffer_size in enumerate([200, 1000, 2000, 4000]): # 0.001, 0.005, 0.01, 0.02]):#, 0.05, 0.1, 0.2]):
            hit_rate_list = []
            max_half = 0
            max_hr = 0
            for half_life_ratio in param_list:
                runner = SingleTestRunner("EFSW", buffer_size, trace_file, [half_life_ratio, 1, 1], cache_file_path=cache_file_path)
                hit_rate = runner.get_hit_rate()
                hit_rate_list.append(hit_rate)
                if hit_rate > max_hr:
                    max_hr = hit_rate
                    max_half = half_life_ratio
            ax.plot(param_list, hit_rate_list, label=f'c = {buffer_size}', linestyle=linestyles[idx], color=colors[idx])
            ax.scatter(max_half, max_hr, color=colors[idx], marker='^')
        # plt.legend(loc=2)
        # fig_path = f'plots/3.1.2/{trace_name}_ESFW.png'
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.22)
    fig_path =f'plots/D2.1/3'
    # plt.legend(loc=9, bbox_to_anchor=(-0.15, -0.065), ncol=5)

    ax.legend(loc="upper left")
    plt.savefig(f'{fig_path}.png')
    plt.savefig(f'{fig_path}.eps')
    plt.savefig(f'{fig_path}.svg')
    print(f'Fig generated path: {fig_path}. ')

if __name__ == '__main__':
    # LRFU_OLTP()
    # EFSW_OLTP()

    COMBINE_OLTP()
    # LRFU_P1()
    # EFSW_P1()