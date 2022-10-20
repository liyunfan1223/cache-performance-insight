#!/usr/bin/env python3

from utils import SingleTestRunner, MultiTestRunner

BUFFER_SIZE = 73728


def optimizer_arc_prior(cache_policy=None, buffer_size=None, trace_file=None):
    lf, rt = 0, buffer_size - 1
    itr = 0
    while rt - lf > max(10, (buffer_size // 100)):
        print(f'Iter: {itr + 1}, lf = {lf}, rt = {rt}')
        itr += 1
        lm = lf + (rt - lf) // 3
        rm = lf + (rt - lf) // 3 * 2
        single_test_runner = SingleTestRunner(cache_policy=cache_policy, buffer_size=buffer_size, trace_file=trace_file,
                                              params=[lm])
        l_hit_rate = single_test_runner.get_hit_rate()

        single_test_runner = SingleTestRunner(cache_policy=cache_policy, buffer_size=buffer_size, trace_file=trace_file,
                                              params=[rm])
        r_hit_rate = single_test_runner.get_hit_rate()
        print(f'l_hit_rate: {l_hit_rate}, r_hit_rate: {r_hit_rate}')
        if l_hit_rate < r_hit_rate:
            lf = lm
        else:
            rt = rm
    best_param = (lf + rt) // 2
    print('Best param:', best_param)


if __name__ == '__main__':
    print("BUFFER SIZE:", BUFFER_SIZE)
    optimizer_arc_prior('ARC_3', BUFFER_SIZE, 'traces/P1.lis')