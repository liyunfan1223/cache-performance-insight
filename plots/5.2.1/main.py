#!/usr/bin/env python
import sys
sys.path.append("/home/ubuntu22/cache-performance-insight")
from scripts.utils import SingleTestRunner, MultiTestRunner, BUFFER_LIST_FOR_TRACES, TRACES_LIST
import os
import matplotlib.pyplot as plt
import math
import numpy as np

plt.style.use('seaborn-v0_8-paper')

def RGC_OLTP_GHOST():
    for trace_name in ["OLTP"]:
        print("TRACE NAME:", trace_name)
        fig, ax = plt.subplots(figsize=(14, 7))
        ax.set_xlabel('Param (lambda)')
        ax.set_ylabel('Hit Ratio(%)')
        ax.set_title(trace_name)
        # ax.set_xscale('log')
        trace_file = f'traces/{trace_name}.lis'
        param_list = [i * 0.1 + 0.1 for i in range(40)]
        ax.set_xlim(param_list[0] / 2, param_list[-1])
        # PL = [math.pow(2, i) for i in np.arange(0, 9)]
        ax.set_xlim(param_list[0] / 2, param_list[-1])
        x = param_list
        for buffer_size in [1000, 2000, 5000, 10000, 15000]:
            hit_rate_list = []
            for param in param_list:
                runner = SingleTestRunner("GLRFU2", buffer_size, trace_file, [20000, 20, 0.5, 5, 4, 10, param])
                hit_rate = runner.get_hit_rate()
                hit_rate_list.append(hit_rate)
            ax.plot(param_list, hit_rate_list, label=f'{"RGC"}_{buffer_size}', marker='+', linestyle='dashed')
        plt.legend(loc=2)
        fig_path = f'plots/5.2.1/{trace_name}_GHOST_RATIO.png'
        plt.savefig(fig_path)
        print(f'Fig generated path: {fig_path}. ')

def RGC_P1_GHOST():
    for trace_name in ["P1"]:
        print("TRACE NAME:", trace_name)
        fig, ax = plt.subplots(figsize=(14, 7))
        ax.set_xlabel('Param (lambda)')
        ax.set_ylabel('Hit Ratio(%)')
        ax.set_title(trace_name)
        # ax.set_xscale('log')
        trace_file = f'traces/{trace_name}.lis'
        param_list = [i * 0.1 + 0.1 for i in range(40)]
        ax.set_xlim(param_list[0] / 2, param_list[-1])
        # PL = [math.pow(2, i) for i in np.arange(0, 9)]
        ax.set_xlim(param_list[0] / 2, param_list[-1])
        x = param_list
        for buffer_size in [8192, 16384, 32768, 65536, 131072]:
            hit_rate_list = []
            for param in param_list:
                runner = SingleTestRunner("GLRFU2", buffer_size, trace_file, [20000, 20, 0.5, 5, 4, 10, param])
                hit_rate = runner.get_hit_rate()
                hit_rate_list.append(hit_rate)
            ax.plot(param_list, hit_rate_list, label=f'{"RGC"}_{buffer_size}', marker='+', linestyle='dashed')
        plt.legend(loc=2)
        fig_path = f'plots/5.2.1/{trace_name}_RGC_GHOST_RATIO.png'
        plt.savefig(fig_path)
        print(f'Fig generated path: {fig_path}. ')

def RGC_P4_GHOST():
    for trace_name in ["P4"]:
        print("TRACE NAME:", trace_name)
        fig, ax = plt.subplots(figsize=(14, 7))
        ax.set_xlabel('Param (lambda)')
        ax.set_ylabel('Hit Ratio(%)')
        ax.set_title(trace_name)
        # ax.set_xscale('log')
        trace_file = f'traces/{trace_name}.lis'
        param_list = [i * 0.1 + 0.1 for i in range(40)]
        ax.set_xlim(param_list[0] / 2, param_list[-1])
        # PL = [math.pow(2, i) for i in np.arange(0, 9)]
        ax.set_xlim(param_list[0] / 2, param_list[-1])
        x = param_list
        for buffer_size in [8192, 16384, 32768, 65536, 131072]:
            hit_rate_list = []
            for param in param_list:
                runner = SingleTestRunner("GLRFU2", buffer_size, trace_file, [20000, 20, 0.5, 5, 4, 10, param])
                hit_rate = runner.get_hit_rate()
                hit_rate_list.append(hit_rate)
            ax.plot(param_list, hit_rate_list, label=f'{"RGC"}_{buffer_size}', marker='+', linestyle='dashed')
        plt.legend(loc=2)
        fig_path = f'plots/5.2.1/{trace_name}_RGC_GHOST_RATIO.png'
        plt.savefig(fig_path)
        print(f'Fig generated path: {fig_path}. ')

def RGC_DS1_GHOST():
    for trace_name in ["DS1"]:
        print("TRACE NAME:", trace_name)
        fig, ax = plt.subplots(figsize=(14, 7))
        ax.set_xlabel('Param (lambda)')
        ax.set_ylabel('Hit Ratio(%)')
        ax.set_title(trace_name)
        # ax.set_xscale('log')
        trace_file = f'traces/{trace_name}.lis'
        param_list = [i * 0.1 + 0.1 for i in range(40)]
        ax.set_xlim(param_list[0] / 2, param_list[-1])
        # PL = [math.pow(2, i) for i in np.arange(0, 9)]
        ax.set_xlim(param_list[0] / 2, param_list[-1])
        x = param_list
        for buffer_size in [8192, 16384, 32768, 65536, 131072]:
            hit_rate_list = []
            for param in param_list:
                runner = SingleTestRunner("GLRFU2", buffer_size, trace_file, [20000, 20, 0.5, 5, 4, 10, param])
                hit_rate = runner.get_hit_rate()
                hit_rate_list.append(hit_rate)
            ax.plot(param_list, hit_rate_list, label=f'{"RGC"}_{buffer_size}', marker='+', linestyle='dashed')
        plt.legend(loc=2)
        fig_path = f'plots/5.2.1/{trace_name}_RGC_GHOST_RATIO.png'
        plt.savefig(fig_path)
        print(f'Fig generated path: {fig_path}. ')

def RGC_OLTP_SIM_RATIO():
    for trace_name in ["OLTP"]:
        print("TRACE NAME:", trace_name)
        fig, ax = plt.subplots(figsize=(14, 7))
        ax.set_xlabel('Param (lambda)')
        ax.set_ylabel('Hit Ratio(%)')
        ax.set_title(trace_name)
        # ax.set_xscale('log')
        trace_file = f'traces/{trace_name}.lis'
        param_list = [i * 0.1 + 0.1 for i in range(15)]
        ax.set_xlim(param_list[0] / 2, param_list[-1])
        # PL = [math.pow(2, i) for i in np.arange(0, 9)]
        ax.set_xlim(param_list[0] / 2, param_list[-1])
        x = param_list
        for buffer_size in [1000, 2000, 5000, 10000, 15000]:
            hit_rate_list = []
            for param in param_list:
                runner = SingleTestRunner("GLRFU2", buffer_size, trace_file, [20000, 20, param, 5, 4, 10, 4])
                hit_rate = runner.get_hit_rate()
                hit_rate_list.append(hit_rate)
            ax.plot(param_list, hit_rate_list, label=f'{"RGC"}_{buffer_size}', marker='+', linestyle='dashed')
        plt.legend(loc=2)
        fig_path = f'plots/5.2.1/{trace_name}_SIM_RATIO.png'
        plt.savefig(fig_path)
        print(f'Fig generated path: {fig_path}. ')

def RGC_P1_SIM_RATIO():
    for trace_name in ["P1"]:
        print("TRACE NAME:", trace_name)
        fig, ax = plt.subplots(figsize=(14, 7))
        ax.set_xlabel('Param (lambda)')
        ax.set_ylabel('Hit Ratio(%)')
        ax.set_title(trace_name)
        # ax.set_xscale('log')
        trace_file = f'traces/{trace_name}.lis'
        param_list = [i * 0.1 + 0.1 for i in range(15)]
        ax.set_xlim(param_list[0] / 2, param_list[-1])
        # PL = [math.pow(2, i) for i in np.arange(0, 9)]
        ax.set_xlim(param_list[0] / 2, param_list[-1])
        x = param_list
        for buffer_size in [8192, 16384, 32768, 65536, 131072]:
            hit_rate_list = []
            for param in param_list:
                runner = SingleTestRunner("GLRFU2", buffer_size, trace_file, [20000, 20, param, 5, 4, 10, 4])
                hit_rate = runner.get_hit_rate()
                hit_rate_list.append(hit_rate)
            ax.plot(param_list, hit_rate_list, label=f'{"RGC"}_{buffer_size}', marker='+', linestyle='dashed')
        plt.legend(loc=2)
        fig_path = f'plots/5.2.1/{trace_name}_SIM_RATIO.png'
        plt.savefig(fig_path)
        print(f'Fig generated path: {fig_path}. ')

def RGC_P4_SIM_RATIO():
    for trace_name in ["P4"]:
        print("TRACE NAME:", trace_name)
        fig, ax = plt.subplots(figsize=(14, 7))
        ax.set_xlabel('Param (lambda)')
        ax.set_ylabel('Hit Ratio(%)')
        ax.set_title(trace_name)
        # ax.set_xscale('log')
        trace_file = f'traces/{trace_name}.lis'
        param_list = [i * 0.1 + 0.1 for i in range(15)]
        ax.set_xlim(param_list[0] / 2, param_list[-1])
        # PL = [math.pow(2, i) for i in np.arange(0, 9)]
        ax.set_xlim(param_list[0] / 2, param_list[-1])
        x = param_list
        for buffer_size in [8192, 16384, 32768, 65536, 131072]:
            hit_rate_list = []
            for param in param_list:
                runner = SingleTestRunner("GLRFU2", buffer_size, trace_file, [20000, 20, param, 5, 4, 10, 4])
                hit_rate = runner.get_hit_rate()
                hit_rate_list.append(hit_rate)
            ax.plot(param_list, hit_rate_list, label=f'{"RGC"}_{buffer_size}', marker='+', linestyle='dashed')
        plt.legend(loc=2)
        fig_path = f'plots/5.2.1/{trace_name}_SIM_RATIO.png'
        plt.savefig(fig_path)
        print(f'Fig generated path: {fig_path}. ')

def RGC_DS1_SIM_RATIO():
    for trace_name in ["DS1"]:
        print("TRACE NAME:", trace_name)
        fig, ax = plt.subplots(figsize=(14, 7))
        ax.set_xlabel('Param (lambda)')
        ax.set_ylabel('Hit Ratio(%)')
        ax.set_title(trace_name)
        # ax.set_xscale('log')
        trace_file = f'traces/{trace_name}.lis'
        param_list = [i * 0.1 + 0.1 for i in range(15)]
        ax.set_xlim(param_list[0] / 2, param_list[-1])
        # PL = [math.pow(2, i) for i in np.arange(0, 9)]
        ax.set_xlim(param_list[0] / 2, param_list[-1])
        x = param_list
        for buffer_size in [8192, 16384, 32768, 65536, 131072]:
            hit_rate_list = []
            for param in param_list:
                runner = SingleTestRunner("GLRFU2", buffer_size, trace_file, [20000, 20, param, 5, 4, 10, 4])
                hit_rate = runner.get_hit_rate()
                hit_rate_list.append(hit_rate)
            ax.plot(param_list, hit_rate_list, label=f'{"RGC"}_{buffer_size}', marker='+', linestyle='dashed')
        plt.legend(loc=2)
        fig_path = f'plots/5.2.1/{trace_name}_SIM_RATIO.png'
        plt.savefig(fig_path)
        print(f'Fig generated path: {fig_path}. ')

if __name__ == '__main__':
    RGC_OLTP_GHOST()
    RGC_P1_GHOST()
    RGC_P4_GHOST()
    RGC_DS1_GHOST()

    RGC_OLTP_SIM_RATIO()
    RGC_P1_SIM_RATIO()
    RGC_P4_SIM_RATIO()
    RGC_DS1_SIM_RATIO()