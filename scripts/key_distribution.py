#!/usr/bin/env python3
import os
from collections import defaultdict

import matplotlib.pyplot as plt

TRACES_LIST = [
    'websearch',
    'P1',
    # 'P2',
    # 'P3',
    # 'P4',
    # 'P5',
    # 'P6',
    # 'P7',
    # 'P12',
    # 'OLTP',
    # 'DS1'
]


class KeyInfoDriver:

    def __init__(self, trace_file_path = None):
        self.trace_file_path = trace_file_path

    def get_key_dict(self):
        key_dict = defaultdict()
        f = open(self.trace_file_path)
        for line in f.readlines():
            start, length, _1, _2 = line.split()
            for idx in range(int(start), int(start) + int(length)):
                if idx in key_dict.keys():
                    key_dict[idx] += 1
                else:
                    key_dict[idx] = 1
        return key_dict


def get_key_distribution_plot(trace_name = None):
    print(f"STARTED. TRACE_NAME: {trace_name}")
    key_info_driver = KeyInfoDriver(trace_file_path=f'traces/{trace_name}.lis')
    key_dict = key_info_driver.get_key_dict()
    freq = [value for value in key_dict.values()]
    freq.sort()
    freq.reverse()
    down_sample_rate = len(freq) // 300

    print('GENERATING...')
    freq = freq[slice(0, len(freq), down_sample_rate)]
    fig, ax = plt.subplots(figsize=(14, 7))
    key_ticklabels = [i * down_sample_rate for i in range(len(freq))]
    ax.bar(key_ticklabels, freq, width = down_sample_rate / 3 * 2)

    ax.set_title(f'Key Distribution for {trace_name}.lis')
    ax.set_xlabel('Key')
    ax.set_ylabel('Frequency')
    if not os.path.exists('local'):
        os.mkdir('local')
    plt.savefig(f'local/KD_{trace_name}.png')

    print('FINISHED.')


def get_key_accumulated_distribution_plot(trace_name = None):
    print(f"STARTED. TRACE_NAME: {trace_name}")
    key_info_driver = KeyInfoDriver(trace_file_path=f'traces/{trace_name}.lis')
    key_dict = key_info_driver.get_key_dict()
    freq = [value for value in key_dict.values()]
    acc_freq = []
    acc = 0
    for f in freq:
        acc += f
        acc_freq.append(acc)

    down_sample_rate = len(acc_freq) // 300
    print('GENERATING...')
    acc_freq = acc_freq[slice(0, len(acc_freq), down_sample_rate)]
    fig, ax = plt.subplots(figsize=(14, 7))
    key_ticklabels = [i * down_sample_rate for i in range(len(acc_freq))]
    ax.plot(key_ticklabels, acc_freq)

    ax.set_title(f'Key Distribution for {trace_name}.lis')
    ax.set_xlabel('Key')
    ax.set_ylabel('Frequency')
    if not os.path.exists('local'):
        os.mkdir('local')
    plt.savefig(f'local/KD_ACC_{trace_name}.png')

    print('FINISHED.')


def get_key_distribution_plot_both(trace_name=None):

    print(f"STARTED. TRACE_NAME: {trace_name}")
    key_info_driver = KeyInfoDriver(trace_file_path=f'traces/{trace_name}.lis')
    key_dict = key_info_driver.get_key_dict()
    freq = [value for value in key_dict.values()]
    freq.sort()
    freq.reverse()
    acc_freq = []
    acc = 0
    for f in freq:
        acc += f
        acc_freq.append(acc)

    down_sample_rate = len(acc_freq) // 3000
    print('GENERATING...')
    acc_freq = acc_freq[slice(0, len(acc_freq), down_sample_rate)]
    fig, ax = plt.subplots(1, 2, figsize=(14, 7))
    key_ticklabels = [i * down_sample_rate for i in range(len(acc_freq))]
    ax[1].plot(key_ticklabels, acc_freq)

    ax[1].set_title(f'Key Accumulated Distribution for {trace_name}.lis')
    ax[1].set_xlabel('Key')
    ax[1].set_ylabel('Frequency')

    freq.sort()
    freq.reverse()
    down_sample_rate = len(freq) // 3000

    fq = freq
    freq = []
    for i in range(0, len(fq), down_sample_rate):
        s = 0
        ct = 0
        for j in range(0, down_sample_rate):
            if i + j >= len(fq):
                break
            s += fq[i + j]
            ct += 1
        freq.append(s / ct)
    # freq = freq[slice(0, len(freq), down_sample_rate)]
    key_ticklabels = [i * down_sample_rate for i in range(len(freq))]
    ax[0].bar(key_ticklabels, freq, width = down_sample_rate / 3 * 2)

    ax[0].set_title(f'Key Distribution for {trace_name}.lis')
    ax[0].set_xlabel('Key')
    ax[0].set_ylabel('Frequency')

    if not os.path.exists('local'):
        os.mkdir('local')
    plt.savefig(f'local/KD_BOTH_{trace_name}.png')

    print('FINISHED.')

if __name__ == "__main__":
    for trace in TRACES_LIST:
        # get_key_distribution_plot(trace_name=trace)
        # get_key_accumulated_distribution_plot(trace_name=trace)
        get_key_distribution_plot_both(trace_name=trace)
