//
// Created by MorphLing on 2023/4/15.
//

#include <cstdio>
#include <string>
#include <iostream>
#include <sys/time.h>
#include "src/def.h"

#include <rocksdb/db.h>
#include <rocksdb/slice.h>
#include <rocksdb/options.h>
#include <libmemcached/memcached.h>
#include <thread>

using ROCKSDB_NAMESPACE::DB;
using ROCKSDB_NAMESPACE::Options;
using ROCKSDB_NAMESPACE::PinnableSlice;
using ROCKSDB_NAMESPACE::ReadOptions;
using ROCKSDB_NAMESPACE::Status;
using ROCKSDB_NAMESPACE::WriteBatch;
using ROCKSDB_NAMESPACE::WriteOptions;
using namespace std;
// rocksdb存储路径

const uint32_t MAX_LENGTH = 1 * 1024;
const uint32_t THREAD_NUM = 1;

std::string kDBPath="/tmp/rocksdb_simple_1k";
const char * config_string = "--SERVER=127.0.0.1";
DB* rocksDB;

double timer[THREAD_NUM + 1][3];
uint32_t counter[THREAD_NUM + 1][3];
string default_str;
bool warming_up[THREAD_NUM + 1] = {true};
uint32_t  warmup_seconds = 30;
vector<int> access_list;
int my_thread_id;
timeval start_time;
int warming_up_counter = 0;

pthread_mutex_t stats_mutex;

DB* rocksdb_create()
{
    DB* db;
    Options options;
    options.use_direct_reads = true;
    options.IncreaseParallelism(THREAD_NUM);
    options.max_background_jobs = THREAD_NUM * 4;
    //文件夹没有数据就创建
    options.create_if_missing=true;
    // 打开数据库，加载数据到内存
    Status s=DB::OpenForReadOnly(options,kDBPath,&db);
    return db;
}

bool request_from_memcached( const char * key, string &value, memcached_st * memc )
{
    memcached_return_t ret;
    size_t value_len;
    uint32_t flags;
    char * v = memcached_get(memc, key, strlen(key), &value_len, &flags, &ret);
    if (ret == 0) {
        value = v;
        // must free manually
        free(v);
    }
    return ret == 0;
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
    Status status = rocksDB->Get(ReadOptions(), key, &value);
    assert(!status.ok() || value.length() >= MAX_LENGTH / 2);
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
    if (request_from_memcached(key, value, memc)) {
        return in_memcached;
    }
    if (request_from_rocksdb(key, value)) {
        save_to_memcached(key, value, value.length(), memc);
        return in_rocksdb;
    }

    uint32_t v_len = (rand() % (MAX_LENGTH / 2)) + MAX_LENGTH / 2;
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
        return 0;
    }
    timeval end_time;
    for (int i = thread_id; i < access_list.size(); i += THREAD_NUM) {
        request_item(to_string(access_list[i]).c_str(), thread_id, memc);

        gettimeofday(&end_time, NULL);
        double total_time = (end_time.tv_sec - start_time.tv_sec) + (end_time.tv_usec - start_time.tv_usec) / 1000000.0; //s
        if (!warming_up[thread_id] && total_time > warmup_seconds) {
            pthread_mutex_lock(&stats_mutex);
            warming_up[thread_id] = true;
            for (int j = 0; j < 3; j++) {
                timer[thread_id][j] = 0;
                counter[thread_id][j] = 0;
            }
            warming_up_counter++;
            if (warming_up_counter == THREAD_NUM) {
                printf("All threads warmed up. Clean statics.\n");
                gettimeofday(&start_time, NULL);
            }
            pthread_mutex_unlock(&stats_mutex);
        }
        // 0 for public
        if (((counter[thread_id][0] + counter[thread_id][1] + counter[thread_id][2]) % 10000 == 0) && thread_id == 1) {
            pthread_mutex_lock(&stats_mutex);
            for (int k = 0; k < 3; k++) {
                timer[0][k] = 0;
                counter[0][k] = 0;
                for (int j = 1; j <= THREAD_NUM; j++) {
                    timer[0][k] += timer[j][k];
                    counter[0][k] += counter[j][k];
                }
            }
            double average_latency = (timer[0][0] + timer[0][1] + timer[0][2]) / (counter[0][0] + counter[0][1] + counter[0][2]);
            double mem_latency = counter[0][0] ? timer[0][0] / counter[0][0] : 0;
            double rdb_latency = counter[0][1] ? timer[0][1] / counter[0][1] : 0;
            double nf_latency = counter[0][2] ? timer[0][2] / counter[0][2] : 0;
            double total_time = (end_time.tv_sec - start_time.tv_sec) + (end_time.tv_usec - start_time.tv_usec) / 1000000.0; //s
            double throughput = (counter[0][0] + counter[0][1] + counter[0][2]) / total_time;
            double hit_ratio = (double) counter[0][0] / (counter[0][0] + counter[0][1] + counter[0][2]) * 100;
            printf("runtime: %.2fs "
                   "warming up: %d "
                   "average latency: %.4f "
                   "mem: %.4f "
                   "rdb: %.4f "
                   "nf: %.4f "
                   "tps: %.2f h_ratio: %.2f%% "
                   "mem:rdb:nf=%d:%d:%d\n",
                   total_time,
                   warming_up_counter == THREAD_NUM,
                   average_latency,
                   mem_latency, rdb_latency, nf_latency,
                   throughput, hit_ratio,
                   counter[0][0], counter[0][1], counter[0][2]);
            fflush(stdout);
            pthread_mutex_unlock(&stats_mutex);
        }
    }
    delete memc;
    // small trace
    pthread_mutex_lock(&stats_mutex);
    if (!warming_up[thread_id]) {
        warming_up[thread_id] = true;
        for (int j = 0; j < 3; j++) {
            timer[thread_id][j] = 0;
            counter[thread_id][j] = 0;
        }
        warming_up_counter++;
        if (warming_up_counter == THREAD_NUM) {
            gettimeofday(&start_time, NULL);
        }
    }
    pthread_mutex_unlock(&stats_mutex);
    return 0;
}

int main()
{
//    setvbuf(stdout, NULL, _IONBF, 0);
    /* initialize connection of rocksdb & memcached */
    rocksDB = rocksdb_create();
    if (!rocksDB) {
        cerr << "RocksDB initialization failed!" << std::endl;
        return 0;
    }
    /* generate default string */
    for (int i = 0; i < MAX_LENGTH; i++) {
        default_str += rand() % 26 + 'a';
    }
    /* get trace */
    FILE * pFile;
    pFile = fopen("traces/P1.lis", "r");
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
    gettimeofday(&start_time, NULL);
    pthread_t threads[THREAD_NUM];

    for (int i = 0; i < THREAD_NUM; i++) {
        ThreadArg* targ = new ThreadArg();
        targ->pid = i + 1;
        pthread_create(&threads[i], NULL, subprocess_work, (void *)(targ));
        pthread_setname_np(threads[i], ("THREAD-" + to_string(i + 1)).c_str());
    }
    for (int i = 0; i < THREAD_NUM; i++) {
        pthread_join(threads[i], NULL);
    }

    delete rocksDB;
    return 0;
}