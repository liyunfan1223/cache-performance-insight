//
// Created by MorphLing on 2023/4/15.
//

#include <cstdio>
#include <string>
#include <iostream>
#include <sys/time.h>
#include <rocksdb/db.h>
#include <rocksdb/slice.h>
#include <rocksdb/options.h>
#include <libmemcached/memcached.h>
#include <thread>
#include <csignal>
#include <queue>
#include "src/def.h"

using ROCKSDB_NAMESPACE::DB;
using ROCKSDB_NAMESPACE::Options;
using ROCKSDB_NAMESPACE::PinnableSlice;
using ROCKSDB_NAMESPACE::ReadOptions;
using ROCKSDB_NAMESPACE::Status;
using ROCKSDB_NAMESPACE::WriteBatch;
using ROCKSDB_NAMESPACE::WriteOptions;
using namespace std;

const uint32_t MAX_THREAD_NUM = 1024;
const uint32_t MAX_TOTAL_COUNTER = 1 << 22;
const uint32_t MEGABYTES = 1 << 20;
const char * config_string = "--SERVER=127.0.0.1";
const uint32_t  warmup_seconds = 30;
const uint32_t  warmup_access = 1 << 20;
const uint32_t  report_interval = 1 << 14;

const uint32_t simulated_network_latency = 5; // 5ms - 10ms for network request
//const uint32_t simulated_network_latency = 0; // 5ms - 10ms for network request
bool earlyStop = false;
uint32_t maxLength;
uint32_t threadNum;
std::string kDBPath;
DB* rocksDB;
string traceFile;
string default_str;

double timer[MAX_THREAD_NUM + 1][3];
uint32_t counter[MAX_THREAD_NUM + 1][3];
bool warming_up[MAX_THREAD_NUM + 1];
timeval start_time[MAX_THREAD_NUM + 1];

vector<int> access_list;
int warming_up_counter = 0;
int hasWarmup;
bool test_finished = false;
pthread_mutex_t stats_mutex;

int global_i;
pthread_mutex_t i_mutex;
bool threadsSync = false;

std::vector<double> latency_vec;
std::mutex latency_mutex;

double GenerateRandomRTT() {
    return (1 + rand() % 100 / 100.0) * simulated_network_latency;
}

DB* rocksdb_create()
{
    DB* db;
    Options options;
    options.use_direct_reads = true;
    options.use_direct_io_for_flush_and_compaction = true;
    options.IncreaseParallelism(threadNum);
    options.max_background_jobs = threadNum * 4;
    //文件夹没有数据就创建
    options.create_if_missing = true;
    // 打开数据库，加载数据到内存
    Status s=DB::Open(options,kDBPath,&db);
    return db;
}

bool request_from_memcached( const char * key, string &value, memcached_st * memc )
{
    memcached_return_t ret;
    size_t value_len;
    uint32_t flags;
    char * v = memcached_get(memc, key, strlen(key), &value_len, &flags, &ret);
    if (ret == MEMCACHED_SUCCESS) {
        value = v;
        // must free manually
        free(v);
    }
    return ret == MEMCACHED_SUCCESS;
}

bool save_to_memcached( const char * key, string& value, uint32_t v_len, memcached_st * memc )
{
    memcached_return_t ret;
    size_t value_len;
    uint32_t flags;
    ret = memcached_set(memc, key, strlen(key), value.substr(0, v_len).c_str(), v_len, 0, 0);
    return ret == 0;
}

bool request_from_rocksdb( const char * key, string& value )
{
    usleep(GenerateRandomRTT() * 1000);
    Status status = rocksDB->Get(ReadOptions(), key, &value);
    assert(!status.ok() || value.length() >= maxLength / 2);
    return status.ok();
}

bool save_to_rocksdb( const char * key, string &value, uint32_t v_len)
{
    Status status = rocksDB->Put(WriteOptions(), key, value.substr(0, v_len));
    return status.ok();
}

enum RequestResult {
    in_memcached,
    in_rocksdb,
    not_found,
    unknown,
};

RequestResult do_request_item(const char * key, memcached_st * memc)
{
    string value;
    timeval start_time, end_time;
//    gettimeofday(&start_time, NULL);
    if (request_from_memcached(key, value, memc)) {
        return in_memcached;
    }
//    gettimeofday(&end_time, NULL);
//    double time = (end_time.tv_sec - start_time.tv_sec) * 1000 + (end_time.tv_usec - start_time.tv_usec) / 1000.0; // ms
//    printf("memcached miss time: %.2f\n", time);
    if (request_from_rocksdb(key, value)) {
        save_to_memcached(key, value, value.length(), memc);
        return in_rocksdb;
    }

    uint32_t v_len = rand() % (maxLength / 2) + (maxLength / 2) + 1;
    save_to_rocksdb(key, default_str, v_len);
    save_to_memcached(key, default_str, v_len, memc);
    return not_found;
}

RequestResult request_item(const char * key, int thread_id, memcached_st * memc)
{
    timeval start_time, end_time;
    gettimeofday(&start_time, NULL);
    RequestResult rr;
    rr = do_request_item(key, memc);
    gettimeofday(&end_time, NULL);
    double time = (end_time.tv_sec - start_time.tv_sec) * 1000 + (end_time.tv_usec - start_time.tv_usec) / 1000.0; // ms
    counter[thread_id][rr]++;
    timer[thread_id][rr] += time;
    if (rand() % 100 <= 10) {
        if (latency_mutex.try_lock()) {
            latency_vec.push_back(time);
            latency_mutex.unlock();
        }
    }
    return rr;
}

struct ThreadArg {
    int pid;
};

void* subprocess_work(void * arg)
{
    int thread_id = ((ThreadArg *)arg)->pid;
    printf("Thread-%d Started.\n", thread_id);
    memcached_st * memc = memcached(config_string, strlen(config_string));
    if (!memc) {
        cerr << "Memcached initialization failed!" << std::endl;
        return nullptr;
    }
    timeval end_time;
    int i = thread_id;
    while (threadsSync ? global_i < access_list.size() : i < access_list.size()) {
        if (threadsSync) {
            pthread_mutex_lock(&i_mutex);
            int now_i = global_i;
            global_i++;
            pthread_mutex_unlock(&i_mutex);
            request_item(to_string(access_list[now_i]).c_str(), thread_id, memc);
        } else {
            request_item(to_string(access_list[i]).c_str(), thread_id, memc);
            i += threadNum;
        }
        gettimeofday(&end_time, NULL);
        if (hasWarmup) {
            if (!warming_up[thread_id]) {
                if (counter[thread_id][0] + counter[thread_id][1] + counter[thread_id][2] >=
                    warmup_access / threadNum) {
                    pthread_mutex_lock(&stats_mutex);
                    warming_up[thread_id] = true;
                    for (int j = 0; j < 3; j++) {
                        timer[thread_id][j] = 0;
                        counter[thread_id][j] = 0;
                    }
                    warming_up_counter++;
                    printf("Thread-%d warmed up.\n", thread_id);
                    gettimeofday(&start_time[thread_id], NULL);
                    if (warming_up_counter == threadNum) {
                        printf("All threads warmed up, clean statics.\n");
                    }
                    pthread_mutex_unlock(&stats_mutex);
                }
            }
        }
        // 0 for public
        if ((counter[thread_id][0] + counter[thread_id][1] + counter[thread_id][2]) % (report_interval / threadNum) == 0 && thread_id == 1) {
            pthread_mutex_lock(&stats_mutex);
            double total_time = 0; // (end_time.tv_sec - start_time[thread_ud].tv_sec) + (end_time.tv_usec - start_time.tv_usec) / 1000000.0; //s
            for (int j = 1; j <= threadNum; j++) {
                total_time += end_time.tv_sec - start_time[j].tv_sec + (end_time.tv_usec - start_time[j].tv_usec) / 1000000.0;
            }
            total_time /= threadNum;
            for (int k = 0; k < 3; k++) {
                timer[0][k] = 0;
                counter[0][k] = 0;
                for (int j = 1; j <= threadNum; j++) {
                    timer[0][k] += timer[j][k];
                    counter[0][k] += counter[j][k];
                }

            }
            uint32_t tot_counter = counter[0][0] + counter[0][1] + counter[0][2];
            double average_latency = (timer[0][0] + timer[0][1] + timer[0][2]) / tot_counter;
            double mem_latency = counter[0][0] ? timer[0][0] / counter[0][0] : 0;
            double rdb_latency = counter[0][1] ? timer[0][1] / counter[0][1] : 0;
            double nf_latency = counter[0][2] ? timer[0][2] / counter[0][2] : 0;
            double throughput_req = tot_counter / total_time;
            double throughput_mb = throughput_req * (maxLength / 4 * 3) / MEGABYTES;
            double hit_ratio = (double) counter[0][0] / tot_counter * 100;
            double throughput_mem = throughput_mb * hit_ratio / 100;
            double throughput_rdb = throughput_mb * (100 - hit_ratio) / 100;
            printf("runtime: %.2fs "
                   "warming up: %d "
                   "average latency: %.4f "
                   "mem: %.4f "
                   "rdb: %.4f "
                   "nf: %.4f "
                   "tps: %.2f tps_mb: %.2f tps_mem: %.2f tps_rdb: %.2f "
                   "h_ratio: %.2f%% t_counter: %u "
                   "mem:rdb:nf=%d:%d:%d\n",
                   total_time,
                   warming_up_counter == threadNum,
                   average_latency,
                   mem_latency, rdb_latency, nf_latency,
                   throughput_req, throughput_mb, throughput_mem, throughput_rdb,
                   hit_ratio, tot_counter,
                   counter[0][0], counter[0][1], counter[0][2]);
            fflush(stdout);

            pthread_mutex_unlock(&stats_mutex);
            if (earlyStop && tot_counter > MAX_TOTAL_COUNTER) {
                test_finished = true;
                printf("Finished.\n");
            }
        }
        if (test_finished && earlyStop) return 0;

    }
    delete memc;
    // small trace
    if (hasWarmup) {
        if (!warming_up[thread_id]) {
            pthread_mutex_lock(&stats_mutex);
            warming_up[thread_id] = true;
            for (int j = 0; j < 3; j++) {
                timer[thread_id][j] = 0;
                counter[thread_id][j] = 0;
            }
            gettimeofday(&start_time[thread_id], NULL);
            warming_up_counter++;
            if (warming_up_counter == threadNum) {
                printf("All threads warmed up, clean statics.\n");
            }
            pthread_mutex_unlock(&stats_mutex);
        }
    }
    return nullptr;
}

/* argv: threadNum - maxLength - traceFile - earlyStop - threadsSync - hasWarmup */
int main(int argc, char* argv[])
{
    printf("Bench started.\n");
    threadNum = stoi(argv[1]);
    if (threadNum <= 0 || threadNum > MAX_THREAD_NUM) {
        cerr << "Threads number invalid." << std::endl;
        return 0;
    }
    maxLength = stoi(argv[2]);
    traceFile = argv[3];
    string str_length;
    if (maxLength % 1024 == 0) {
        str_length = to_string(maxLength / 1024) + 'k';
    } else {
        str_length = to_string(maxLength);
    }
    kDBPath = "/tmp/rocksdb_simple_" + str_length + "_" + traceFile;
    if (argv[4] == nullptr) {
        cerr << "No early stop option." << std::endl;
        return 0;
    }
    earlyStop = stoi(argv[4]);
    if (argv[5] == nullptr) {
        cerr << "No threads synchronize option." << std::endl;
        return 0;
    }
    threadsSync = stoi(argv[5]);
    if (argv[6] == nullptr) {
        cerr << "No warmup option." << std::endl;
        return 0;
    }
    hasWarmup = stoi(argv[6]);
    /* initialize connection of rocksdb & memcached */
    rocksDB = rocksdb_create();
    if (!rocksDB) {
        cerr << "RocksDB initialization failed!" << std::endl;
        return 0;
    }
    /* generate default string */
    for (int i = 0; i < maxLength + 1; i++) {
        default_str += rand() % 26 + 'a';
    }
    /* get trace */
    FILE * pFile;
    pFile = fopen(("traces/" + traceFile + ".lis").c_str(), "r");
    if (pFile == NULL) {
        cerr << "File open failed!" << std::endl;
        return 0;
    }
    trace_line l;
    while (fscanf(pFile, "%d %d %d %d\n",
                  &l.starting_block, &l.number_of_blocks, &l.ignore, &l.request_number) != EOF) {
        for (auto i = l.starting_block; i < (l.starting_block + l.number_of_blocks); ++i) {
            access_list.push_back(i);
        }
    }
    for (int i = 1; i <= threadNum; i++)
        gettimeofday(&start_time[i], NULL);

    pthread_t threads[threadNum];

    for (int i = 0; i < threadNum; i++) {
        ThreadArg* targ = new ThreadArg();
        targ->pid = i + 1;
        pthread_create(&threads[i], NULL, subprocess_work, (void *)(targ));
        pthread_setname_np(threads[i], ("THREAD-" + to_string(i + 1)).c_str());
    }
    pthread_join(threads[0], NULL);
    for (int i = 1; i < threadNum; i++) {
        pthread_join(threads[i], NULL);
    }
    printf("Sampled %zu, now calculating tail latency...\n", latency_vec.size());
    std::sort(latency_vec.begin(), latency_vec.end());
    static std::vector<double> stastic_percentiles;
    for (int i = 0; i <= 100; i++) {
        stastic_percentiles.push_back(i / 100.0);
    }
    stastic_percentiles.push_back(0.90);
    stastic_percentiles.push_back(0.95);
    stastic_percentiles.push_back(0.99);
    stastic_percentiles.push_back(0.999);
    stastic_percentiles.push_back(0.9999);
    stastic_percentiles.push_back(0.99999);
//    {0.01, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.75, 0.8, 0.9, 0.95, 0.99, 0.999, 0.9999};
    for (double percentile : stastic_percentiles) {
        printf("Percentage %.8f%%: %.8fms\n", percentile * 100, latency_vec[(int)(latency_vec.size() * percentile)]);
    }
    delete rocksDB;
    return 0;
}