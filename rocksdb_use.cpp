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

using ROCKSDB_NAMESPACE::DB;
using ROCKSDB_NAMESPACE::Options;
using ROCKSDB_NAMESPACE::PinnableSlice;
using ROCKSDB_NAMESPACE::ReadOptions;
using ROCKSDB_NAMESPACE::Status;
using ROCKSDB_NAMESPACE::WriteBatch;
using ROCKSDB_NAMESPACE::WriteOptions;
using namespace std;
// rocksdb存储路径

const uint32_t maxLength = 1 * 1024;

std::string kDBPath="/tmp/rocksdb_simple_1k";
const char * config_string = "--SERVER=127.0.0.1";
DB* rocksDB;
memcached_st * memc;
double timer[3];
uint32_t counter[3];
string default_str;
bool warming_up = true;
uint32_t  warmup_seconds = 30;

DB* rocksdb_create()
{
    DB* db;
    Options options;
    options.use_direct_reads = true;
    //文件夹没有数据就创建
    options.create_if_missing=true;
    // 打开数据库，加载数据到内存
    Status s=DB::Open(options,kDBPath,&db);
    return db;
}

bool request_from_memcached( const char * key, string &value )
{
    memcached_return_t ret;
    size_t value_len;
    uint32_t flags;
    char * v = memcached_get(memc, key, strlen(key), &value_len, &flags, &ret);
    if (ret == 0) {
        value = v;
    }
    return ret == 0;
}

bool save_to_memcached( const char * key, string& value, uint32_t v_len )
{
    memcached_return_t ret;
    size_t value_len;
    uint32_t flags;
//    char * value = memcached_get(memc, key, strlen(key), &value_len, &flags, &ret);
//    assert(v_len >= maxLength / 2);
    ret = memcached_set(memc, key, strlen(key), value.substr(0, v_len).c_str(), v_len, 0, 0);
    return ret == 0;
}

bool request_from_rocksdb( const char * key, string& value )
{
    // string value;
    Status status = rocksDB->Get(ReadOptions(), key, &value);
    assert(!status.ok() || value.length() >= maxLength / 2);
    return status.ok();
}

bool save_to_rocksdb( const char * key, string &value, uint32_t v_len)
{
    assert(v_len >= maxLength / 2);
    assert(value.substr(0, v_len).length() == v_len);
    Status status = rocksDB->Put(WriteOptions(), key, value.substr(0, v_len));
    return status.ok();
}

string value_generator()
{
     return "SimpleValueExample";
}

enum RequestResult {
    in_memcached,
    in_rocksdb,
    not_found,
    unknown
};

RequestResult do_request_item(const char * key)
{
    string value;
    if (request_from_memcached(key, value)) {
        return in_memcached;
    }
    if (request_from_rocksdb(key, value)) {
        save_to_memcached(key, value, value.length());
        return in_rocksdb;
    }

    uint32_t v_len = (rand() % (maxLength / 2)) + maxLength / 2;
    assert(v_len >= maxLength / 2);
//    printf("%d\n", v_len);
    save_to_rocksdb(key, default_str, v_len);
    save_to_memcached(key, default_str, v_len);
    return not_found;
}

RequestResult request_item(const char * key)
{
    timeval start_time, end_time;
    gettimeofday(&start_time, NULL);
    RequestResult rr;
    rr = do_request_item(key);
    gettimeofday(&end_time, NULL);
    double time = (end_time.tv_sec - start_time.tv_sec) * 1000 + (end_time.tv_usec - start_time.tv_usec) / 1000.0; // ms
    counter[rr]++;
    timer[rr] += time;
    return rr;
}

int main()
{
    /* initialize connection of rocksdb & memcached */
    rocksDB = rocksdb_create();
    memc = memcached(config_string, strlen(config_string));
    if (!rocksDB) {
        cerr << "RocksDB initialization failed!" << std::endl;
        return 0;
    }
    if (!memc) {
        cerr << "Memcached initialization failed!" << std::endl;
        return 0;
    }
    /* generate default string */
    for (int i = 0; i < maxLength; i++) {
        default_str += rand() % 26 + 'a';
    }
    /* get trace */
    FILE * pFile;
//    pFile = fopen("traces/P12.lis", "r");
    pFile = fopen("traces/P6.lis", "r");
    if (pFile == NULL) {
        cerr << "File open failed!" << std::endl;
        return 0;
    }
    trace_line l;
    timeval start_time, end_time;

    gettimeofday(&start_time, NULL);
    while (fscanf(pFile, "%d %d %d %d\n",
                  &l.starting_block, &l.number_of_blocks, &l.ignore, &l.request_number) != EOF) {
        for (auto i = l.starting_block; i < (l.starting_block + l.number_of_blocks); ++i) {
            request_item(to_string(i).c_str());
            if ((counter[0] + counter[1] + counter[2]) % 10000 == 0) {
                gettimeofday(&end_time, NULL);
                double average_latency = (timer[0] + timer[1] + timer[2]) / (counter[0] + counter[1] + counter[2]);
                double mem_latency = counter[0] ? timer[0] / counter[0] : 0;
                double rdb_latency = counter[1] ? timer[1] / counter[1] : 0;
                double nf_latency = counter[2] ? timer[2] / counter[2] : 0;
                double total_time = (end_time.tv_sec - start_time.tv_sec) + (end_time.tv_usec - start_time.tv_usec) / 1000000.0; //s
                double throughput = (counter[0] + counter[1] + counter[2]) / total_time;
                double hit_ratio = (double) counter[0] / (counter[0] + counter[1] + counter[2]) * 100;
                printf("runtime: %.2fs "
                       "warming up: %d "
                       "average latency: %.6f "
                       "mem: %.6f "
                       "rdb: %.6f "
                       "nf: %.6f "
                       "tps: %.2f h_ratio: %.2f%% "
                       "mem:rdb:nf=%d:%d:%d\n",
                       total_time,
                       warming_up,
                       average_latency,
                       mem_latency, rdb_latency, nf_latency,
                       throughput, hit_ratio,
                       counter[0], counter[1], counter[2]);
                if (warming_up && total_time > warmup_seconds) {
                    printf("Warmup stage finish.\n");
                    warming_up = false;
                    gettimeofday(&start_time, NULL);
                    for (int i = 0; i < 3; i++) {
                        timer[i] = 0;
                        counter[i] = 0;
                    }
                }
            }
//            if (counter[0] + counter[1] + counter[2] == 3000000) {
//                break;
//            }
        }
//        if (counter[0] + counter[1] + counter[2] == 3000000) {
//            break;
//        }
    }

    delete rocksDB;
    delete memc;
//    assert(s.ok());
//    // 写key-value
//    s=db->Put(WriteOptions(),"key01","value");
//    assert(s.ok());
//
//    std::string value;
//    s=db->Get(ReadOptions(),"key01",&value);
//    assert(s.ok());
//    assert(value=="value");
//    // 管道，原子方式更新
//    {
//        WriteBatch batch;
//        batch.Delete("key01");
//        batch.Put("key02",value);
//        s=db->Write(WriteOptions(),&batch);
//    }
//    s=db->Get(ReadOptions(),"key01",&value);
//    assert(s.IsNotFound());
//    s=db->Get(ReadOptions(),"key02",&value);
//    assert(value=="value");
//
//    {
//        PinnableSlice pinnable_val;
//        // 列族方式读取
//        db->Get(ReadOptions(),db->DefaultColumnFamily(),"key02",&pinnable_val);
//        assert(pinnable_val=="value");
//    }
//
//    {
//        std::string string_val;
//        PinnableSlice pinnable_val(&string_val);
//        // 列族方式读取
//        db->Get(ReadOptions(),db->DefaultColumnFamily(),"key02",&pinnable_val);
//        assert(pinnable_val=="value");
//        assert(pinnable_val.IsPinned() || string_val == "value");
//    }
//
//    PinnableSlice pinnable_val;
//    s=db->Get(ReadOptions(),db->DefaultColumnFamily(),"key01",&pinnable_val);
//    assert(s.IsNotFound());
//
//    pinnable_val.Reset();
//    db->Get(ReadOptions(),db->DefaultColumnFamily(),"key02",&pinnable_val);
//    assert(pinnable_val=="value");
//    pinnable_val.Reset();



    return 0;
}