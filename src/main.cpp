//
// Created by MorphLing on 2022/9/28.
//

#include <iostream>
#include <memory>

#include "def.h"
#include "utils/unittest_utils.h"
#include "managers/lru_cache_manager.h"
#include "managers/lfu_cache_manager.h"
#include "managers/arc_cache_manager.h"
#include "managers/arc2_cache_manager.h"
#include "managers/opt_cache_manager.h"
#include "managers/arc3_cache_manager.h"
#include "managers/mrf_cache_manager.h"
#include "managers/stw_cache_manager.h"
#include "managers/stw2_cache_manager.h"
#include "managers/srrip_cache_manager.h"

std::unordered_map<std::string, CachePolicy> cachePolicy = {
        {"LRU", CachePolicy::LRU},
        {"LFU", CachePolicy::LFU},
        {"ARC", CachePolicy::ARC},
        // {"ARC_2", CachePolicy::ARC_2},
        // {"ARC_3", CachePolicy::ARC_3},
        {"OPT", CachePolicy::OPT},
        {"MRF", CachePolicy::MRF},
        {"STW", CachePolicy::STW},
        {"STW2", CachePolicy::STW2},
        {"SRRIP", CachePolicy::SRRIP},
};

void usage() {
    std::cout << "usage: ./src/main" << " <cache_policy> <buffer_size> <trace_file> <param_0>\n"
              << "       <cache_policy> -- cache policy: [LRU, LFU, ARC, OPT, STW]\n"
              << "       <buffer_size>  -- buffer size\n"
              << "       <trace_file>   -- path of trace_file"
              << "       <param_0>      -- optimal, param_0 for specific cache policy"
              << std::endl;
}

int main(int argc, char **argv) {
    if (strcmp(argv[1], "-h") == 0 || strcmp(argv[1], "--help") == 0) {
        usage();
        return 0;
    }
    std::vector<Key> access_list;
    UnittestUtils::get_access_list(argv[3], access_list);

    std::string cache_policy(argv[1]);
    int32_t buffer_size = std::stoi(argv[2]);
    char * trace_file = argv[3];
    char * param_0 = argv[4];

    switch (cachePolicy.at(cache_policy)) {
        case CachePolicy::LRU:
            UnittestUtils::make_test(trace_file,std::make_shared<LRUCacheManager>(buffer_size));
            break;
        case CachePolicy::LFU:
            UnittestUtils::make_test(trace_file, std::make_shared<LFUCacheManager>(buffer_size));
            break;
        case CachePolicy::ARC:
            UnittestUtils::make_test(trace_file,std::make_shared<ARCCacheManager>(buffer_size));
            break;
        // case CachePolicy::ARC_2:
        //     UnittestUtils::make_test(trace_file,std::shared_ptr<CacheManager>(new ARC2CacheManager(
        //             buffer_size, std::stof(param_0), access_list)));
        //     break;
        // case CachePolicy::ARC_3:
        //     UnittestUtils::make_test(trace_file,std::shared_ptr<CacheManager>(new ARC3CacheManager(
        //             buffer_size, std::stoi(param_0), access_list)));
            // break;
        case CachePolicy::OPT:
            UnittestUtils::make_test(trace_file,std::make_shared<OPTCacheManager>(buffer_size, access_list));
            break;
        case CachePolicy::MRF:
            UnittestUtils::make_test(trace_file,std::make_shared<MRFCacheManager>(buffer_size, access_list));
            break;
        case CachePolicy::STW:
            if (argc <= BASIC_MAIN_ARG_NUM) {
                UnittestUtils::make_test(trace_file,
                                         std::make_shared<STWCacheManager>(buffer_size));
            } else {
                UnittestUtils::make_test(trace_file,
                                         std::make_shared<STWCacheManager>(buffer_size, std::stof(param_0)));
            }
            break;
        case CachePolicy::STW2:
            if (argc <= BASIC_MAIN_ARG_NUM) {
                UnittestUtils::make_test(trace_file,
                                         std::make_shared<STW2CacheManager>(buffer_size));
            } else {
                UnittestUtils::make_test(trace_file,
                                         std::make_shared<STW2CacheManager>(buffer_size, std::stof(param_0)));
            }
            break;
        case CachePolicy::SRRIP:
            if (argc <= BASIC_MAIN_ARG_NUM) {
                UnittestUtils::make_test(trace_file,
                                         std::make_shared<SRRIPCacheManager>(buffer_size));
            } else {
                UnittestUtils::make_test(trace_file,
                                         std::make_shared<SRRIPCacheManager>(buffer_size, std::stof(param_0)));
            }
            break;
        default:
            break;
    }
    return 0;
}


