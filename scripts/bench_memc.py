import subprocess
import time
from utils import SingleTestRunner, MultiTestRunner, TRACES_LIST, BUFFER_LIST_FOR_TRACES, StatisticsCompareLRU
from trace_analyzer import GetUniqueKeys

THREADS_LIST = [32]
TRACE_FILE_LIST = ["P6", "P1"]
LOGFILE = 'log1030'
results = []

def bench(thread_num, value_size, memcached_mem, trace_file, memc_suffix, early_stop=True, threads_sync=True, has_warmup=True, est_item_counts=0):
    print(f"Started. Args: threads-{thread_num} value_size-{value_size} memcached_mem-{memcached_mem} "
          f"trace-{trace_file} memc_suffix-{memc_suffix} earle_stop-{early_stop} threads_sync-{threads_sync} has_warmup-{has_warmup} est_item_counts-{est_item_counts}")
    params = [f"/tmp/memcached/memcached-{memc_suffix}", "-m", f"{memcached_mem}", "-o", "no_lru_crawler", "-o", "no_lru_maintainer"]
    if est_item_counts != 0:
        params.append("-E")
        params.append(f"{est_item_counts}")
    memc_process = subprocess.Popen(params)
    # print(1)
    time.sleep(3)
    # print(5)
    bench_process = subprocess.Popen(["build/rocksdb_use_multi_threads", f"{thread_num}", f"{value_size}", f"{trace_file}",
                                      f"{1 if early_stop else 0}", f"{1 if threads_sync else 0}", f"{1 if has_warmup else 0}", "0"],
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, errors = bench_process.communicate()
    if len(errors) > 0:
        print("Error occurred!", errors)
    else:
        try:
            result = output.decode('utf-8')
            # print(result)
            # result = result.split("\n")[-110]
            result_str = result.split("\n")[-110]
            # for item in result:
            #     result_str += item + '\n'
            log = f"Time: {time.time()} Args: threads-{thread_num} value_size-{value_size} memcached_mem-{memcached_mem} "\
                  f"trace-{trace_file} memc_suffix-{memc_suffix} earle_stop-{early_stop} threads_sync-{threads_sync} "\
                  f"has_warmup-{has_warmup} est_item_counts-{est_item_counts} \n{result_str}"
            # results.append(log)
            # result_str = log + result_str
            print("result: ", log)
            with open(f"local/{LOGFILE}.txt", "a") as f:
                f.write(f"{log}\n")
        except Exception as e:
            with open(f"local/{LOGFILE}.txt", "a") as f:
                f.write(f"Error occurred: {e}\n")
            print(f"Error occurred: {e}")
    memc_process.terminate()
    memc_process.wait()
    print("Finished.")


if __name__ == "__main__":
    for p_size in [0.1, 0.05, 0.01, 0.001]:
        for trace_file in TRACES_LIST:
            keys = GetUniqueKeys(f'traces/{trace_file}.lis')
            est_items = keys * p_size
            size = int(est_items / 1225)
            size = max(2, size)
            # bench(64, 1 * 1024, size, trace_file, "lru", early_stop=False, has_warmup=False)
            bench(64, 1 * 1024, size, trace_file, "rgc", early_stop=False, has_warmup=False, est_item_counts=est_items)
            runner = SingleTestRunner('RGC4', p_size, f'traces/{trace_file}.lis',
                                      [16, 1, 6, 4, 1.0, 20000, 0.5, 0.05, 0.00, 0.01, 1, 1024, 10000])
            ideal = runner.get_hit_rate()
            with open(f"local/{LOGFILE}.txt", "a") as f:
                f.write(f"Size:{size}, P_size:{p_size}, Est_items:{est_items}, Ideal Hit Rate:{ideal}\n")

    # for p_size in [0.1, 0.05, 0.01, 0.001]:
    #     for trace_file in TRACES_LIST:
    #         keys = GetUniqueKeys(f'traces/{trace_file}.lis')
    #         est_items = keys * p_size
    #         size = int(est_items / 1225)
    #         size = max(2, size)
    #         # bench(64, 1 * 1024, size, trace_file, "lru", early_stop=False, has_warmup=False)
    #         bench(64, 1 * 1024, size, trace_file, "rgc", early_stop=False, has_warmup=False, est_item_counts=est_items)
    #         runner = SingleTestRunner('RGC4', p_size, f'traces/{trace_file}.lis',
    #                                   [16, 1, 6, 4, 1.0, 20000, 0.5, 0.05, 0.00, 0.01, 1, 1024, 10000])
    #         ideal = runner.get_hit_rate()
    #         with open(f"local/{LOGFILE}.txt", "a") as f:
    #             f.write(f"Size:{size}, P_size:{p_size}, Est_items:{est_items}, Ideal Hit Rate:{ideal}\n")

    # for p_size in [0.1, 0.05, 0.01, 0.001]:
    #     for trace_file in TRACES_LIST:
    #         keys = GetUniqueKeys(f'traces/{trace_file}.lis')
    #         est_items = keys * p_size
    #         size = int(est_items / 1190)
    #         size = max(2, size)
    #         # bench(64, 1 * 1024, size, trace_file, "lru", early_stop=False, has_warmup=False)
    #         bench(64, 1 * 1024, size, trace_file, "lru", early_stop=False, has_warmup=False)
    #         runner = SingleTestRunner('LRU', p_size, f'traces/{trace_file}.lis',
    #                                   None)
    #         ideal = runner.get_hit_rate()
    #         with open(f"local/{LOGFILE}.txt", "a") as f:
    #             f.write(f"Size:{size}, P_size:{p_size}, Est_items:{est_items}, Ideal Hit Rate:{ideal}\n")
