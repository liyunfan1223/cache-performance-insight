//
// Created by MorphLing on 2022/9/28.
//
//#define LOG

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
#include "managers/drrip_cache_manager.h"
#include "managers/efsw_cache_manager.h"
#include "managers/lrfu_cache_manager.h"
#include "managers/alrfu_cache_manager.h"
#include "managers/alrfu2_cache_manager.h"
#include "managers/alrfu3_cache_manager.h"
#include "managers/alrfu4_cache_manager.h"
#include "managers/alrfu5_cache_manager.h"
#include "managers/glrfu_cache_manager.h"
#include "managers/glrfu2_cache_manager.h"
#include "managers/glrfu3_cache_manager.h"
#include "managers/glrfu4_cache_manager.h"
#include "managers/lirs_cache_manager.h"
#include "managers/dlirs_cache_manager.h"
#include "managers/rgc_cache_manager.h"
#include "managers/rgc2_cache_manager.h"
#include "managers/rgc3_cache_manager.h"
#include "managers/cacheus_cache_manager.h"

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
        {"DRRIP", CachePolicy::DRRIP},
        {"EFSW", CachePolicy::EFSW},
        {"LRFU", CachePolicy ::LRFU},
        {"ALRFU", CachePolicy::ALRFU},
        {"ALRFU2", CachePolicy::ALRFU2},
        {"ALRFU3", CachePolicy::ALRFU3},
        {"ALRFU4", CachePolicy::ALRFU4},
        {"ALRFU5", CachePolicy::ALRFU5},
        {"GLRFU", CachePolicy::GLRFU},
        {"GLRFU2", CachePolicy::GLRFU2},
        {"GLRFU3", CachePolicy::GLRFU3},
        {"GLRFU4", CachePolicy::GLRFU4},
        {"LIRS", CachePolicy::LIRS},
        {"DLIRS", CachePolicy::DLIRS},
        {"RGC", CachePolicy::RGC},
        {"RGC2", CachePolicy::RGC2},
        {"RGC3", CachePolicy::RGC3},
        {"CACHEUS", CachePolicy::CACHEUS},
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
    int unique_key_nums;
    UnittestUtils::get_access_list(argv[3], access_list, unique_key_nums);

    std::string cache_policy(argv[1]);

    float buffer_param = std::stof(argv[2]);
    int32_t buffer_size = buffer_param > 1 ? std::stoi(argv[2]) : std::max(1, (int)(buffer_param * unique_key_nums));
    char* trace_file = argv[3];
    char* param_0 = argv[4];
    char* param_1 = argv[5];
    char* param_2 = argv[6];
    char* param_3 = argv[7];
    char* param_4 = argv[8];
    char* param_5 = argv[9];
    char* param_6 = argv[10];
    char* param_7 = argv[11];
    char* param_8 = argv[12];
    char* param_9 = argv[13];
    char* param_10 = argv[14];
    char* param_11 = argv[15];
    timeval start_time;
    gettimeofday(&start_time, NULL);
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
        case CachePolicy::DRRIP:
            if (argc <= BASIC_MAIN_ARG_NUM) {
                UnittestUtils::make_test(trace_file,
                                         std::make_shared<DRRIPCacheManager>(buffer_size));
            } else {
                UnittestUtils::make_test(trace_file,
                                         std::make_shared<DRRIPCacheManager>(buffer_size, std::stof(param_0)));
            }
            break;
        case CachePolicy::EFSW:
            if (argc <= BASIC_MAIN_ARG_NUM) {
                UnittestUtils::make_test(trace_file,
                                         std::make_shared<EFSWCacheManager>(buffer_size));
            } else {
                UnittestUtils::make_test(trace_file,
                                         std::make_shared<EFSWCacheManager>(buffer_size, std::stof(param_0),
                                                                             std::stof(param_1),std::stof(param_2)));
            }
            break;
        case CachePolicy::LRFU:
            if (argc <= BASIC_MAIN_ARG_NUM) {
                UnittestUtils::make_test(trace_file,
                                         std::make_shared<LRFUCacheManager>(buffer_size));
            } else {
                UnittestUtils::make_test(trace_file,
                                         std::make_shared<LRFUCacheManager>(buffer_size, std::stof(param_0)));
            }
            break;
        case CachePolicy::ALRFU:
            if (argc <= BASIC_MAIN_ARG_NUM) {
                UnittestUtils::make_test(trace_file,
                                         std::make_shared<ALRFUCacheManager>(buffer_size));
            } else {
                UnittestUtils::make_test(trace_file,
                                         std::make_shared<ALRFUCacheManager>(buffer_size,
                                                                             std::stof(param_0),
                                                                             std::stof(param_1),
                                                                             std::stof(param_2),
                                                                             std::stof(param_3)));
            }
            break;
        case CachePolicy::ALRFU2:
            if (argc <= BASIC_MAIN_ARG_NUM) {
                UnittestUtils::make_test(trace_file,
                                         std::make_shared<ALRFU2CacheManager>(buffer_size));
            } else {
                UnittestUtils::make_test(trace_file,
                                         std::make_shared<ALRFU2CacheManager>(buffer_size,
                                                                             std::stof(param_0),
                                                                             std::stof(param_1),
                                                                             std::stof(param_2),
                                                                             std::stof(param_3)));
            }
            break;
        case CachePolicy::ALRFU3:
            if (argc <= BASIC_MAIN_ARG_NUM) {
                UnittestUtils::make_test(trace_file,
                                         std::make_shared<ALRFU3CacheManager>(buffer_size));
            } else {
                UnittestUtils::make_test(trace_file,
                                         std::make_shared<ALRFU3CacheManager>(buffer_size,
                                                                              std::stof(param_0),
                                                                              std::stof(param_1),
                                                                              std::stof(param_2),
                                                                              std::stof(param_3)));
            }
            break;
        case CachePolicy::ALRFU4:
            if (argc <= BASIC_MAIN_ARG_NUM) {
                UnittestUtils::make_test(trace_file,
                                         std::make_shared<ALRFU4CacheManager>(buffer_size));
            } else {
                UnittestUtils::make_test(trace_file,
                                         std::make_shared<ALRFU4CacheManager>(buffer_size,
                                                                              std::stof(param_0),
                                                                              std::stof(param_1),
                                                                              std::stof(param_2),
                                                                              std::stof(param_3),
                                                                              std::stof(param_4),
                                                                              std::stof(param_5),
                                                                               std::stof(param_6)));
            }
            break;
        case CachePolicy::ALRFU5:
            if (argc <= BASIC_MAIN_ARG_NUM) {
                UnittestUtils::make_test(trace_file,
                                         std::make_shared<ALRFU5CacheManager>(buffer_size));
            } else {
                UnittestUtils::make_test(trace_file,
                                         std::make_shared<ALRFU5CacheManager>(buffer_size,
                                                                              std::stof(param_0),
                                                                              std::stof(param_1),
                                                                              std::stof(param_2),
                                                                              std::stof(param_3),
                                                                              std::stof(param_4),
                                                                              std::stof(param_5),
                                                                              std::stof(param_6)));
            }
            break;
        case CachePolicy::GLRFU:
            if (argc <= BASIC_MAIN_ARG_NUM) {
                UnittestUtils::make_test(trace_file,
                                         std::make_shared<GhostALRFUCacheManager>(buffer_size));
            }else {
                UnittestUtils::make_test(trace_file,
                                         std::make_shared<GhostALRFUCacheManager>(buffer_size,
                                                                              std::stof(param_0),
                                                                              std::stof(param_1),
                                                                              std::stof(param_2),
                                                                              std::stof(param_3),
                                                                              std::stof(param_4),
                                                                              std::stof(param_5)));
            }
            break;
        case CachePolicy::GLRFU2:
            if (argc <= BASIC_MAIN_ARG_NUM) {
                UnittestUtils::make_test(trace_file,
                                         std::make_shared<glruf2::GhostALRFU2CacheManager>(buffer_size));
            } else {
                UnittestUtils::make_test(trace_file,
                                         std::make_shared<glruf2::GhostALRFU2CacheManager>(buffer_size,
                                                                                  std::stof(param_0),
                                                                                  std::stof(param_1),
                                                                                  std::stof(param_2),
                                                                                  std::stof(param_3),
                                                                                  std::stof(param_4),
                                                                                  std::stof(param_5),
                                                                                  std::stof(param_6)));
            }
            break;
        case CachePolicy::GLRFU3:
            if (argc <= BASIC_MAIN_ARG_NUM) {
                UnittestUtils::make_test(trace_file,
                                         std::make_shared<glrfu3::GhostALRFU3CacheManager>(buffer_size));
            } else {
                UnittestUtils::make_test(trace_file,
                                         std::make_shared<glrfu3::GhostALRFU3CacheManager>(buffer_size,
                                                                                           std::stof(param_0),
                                                                                           std::stof(param_1),
                                                                                           std::stof(param_2),
                                                                                           std::stof(param_3),
                                                                                           std::stof(param_4),
                                                                                           std::stof(param_5),
                                                                                           std::stof(param_6),
                                                                                           std::stof(param_7)));
            }
            break;
        case CachePolicy::GLRFU4:
            if (argc <= BASIC_MAIN_ARG_NUM) {
                UnittestUtils::make_test(trace_file,
                                         std::make_shared<glrfu4::GhostALRFU4CacheManager>(buffer_size));
            } else {
                UnittestUtils::make_test(trace_file,
                                         std::make_shared<glrfu4::GhostALRFU4CacheManager>(buffer_size,
                                                                                           std::stof(param_0),
                                                                                           std::stof(param_1),
                                                                                           std::stof(param_2),
                                                                                           std::stof(param_3),
                                                                                           std::stof(param_4),
                                                                                           std::stof(param_5),
                                                                                           std::stof(param_6),
                                                                                           std::stof(param_7)));
            }
            break;
        case CachePolicy::LIRS:
            if (argc <= BASIC_MAIN_ARG_NUM) {
                UnittestUtils::make_test(trace_file,
                                         std::make_shared<LIRSCacheManager>(buffer_size));
            } else {
                UnittestUtils::make_test(trace_file,
                                         std::make_shared<LIRSCacheManager>(buffer_size, std::stof(param_0)));
            }
            break;
        case CachePolicy::DLIRS:
            if (argc <= BASIC_MAIN_ARG_NUM) {
                UnittestUtils::make_test(trace_file,
                                         std::make_shared<DLIRSCacheManager>(buffer_size));
            } else {
                UnittestUtils::make_test(trace_file,
                                         std::make_shared<DLIRSCacheManager>(buffer_size, std::stof(param_0)));
            }
            break;
        case CachePolicy::RGC:
            if (argc <= BASIC_MAIN_ARG_NUM) {
                UnittestUtils::make_test(trace_file,
                                         std::make_shared<RGCCacheManager>(buffer_size));
            }else {
                UnittestUtils::make_test(trace_file,
                                         std::make_shared<RGCCacheManager>(buffer_size,
                                                                                           std::stof(param_0),
                                                                                           std::stof(param_1),
                                                                                           std::stof(param_2),
                                                                                           std::stof(param_3),
                                                                                           std::stof(param_4),
                                                                                           std::stof(param_5),
                                                                                           std::stof(param_6),
                                                                                           std::stof(param_7),
                                                                                           std::stof(param_8),
                                                                                           std::stof(param_9),
                                                                                           std::stof(param_10),
                                                                                           std::stof(param_11)));
            }
            break;
        case CachePolicy::RGC2:
            if (argc <= BASIC_MAIN_ARG_NUM) {
                UnittestUtils::make_test(trace_file,
                                         std::make_shared<RGC2CacheManager>(buffer_size));
            }else {
                UnittestUtils::make_test(trace_file,
                                         std::make_shared<RGC2CacheManager>(buffer_size,
                                                                           std::stof(param_0),
                                                                           std::stof(param_1),
                                                                           std::stof(param_2),
                                                                           std::stof(param_3),
                                                                           std::stof(param_4),
                                                                           std::stof(param_5),
                                                                           std::stof(param_6),
                                                                           std::stof(param_7),
                                                                           std::stof(param_8),
                                                                           std::stof(param_9)
                                                                            ));
            }
            break;
        case CachePolicy::RGC3:
            if (argc <= BASIC_MAIN_ARG_NUM) {
                UnittestUtils::make_test(trace_file,
                                         std::make_shared<RGC3CacheManager>(buffer_size));
            }else {
                UnittestUtils::make_test(trace_file,
                                         std::make_shared<RGC3CacheManager>(buffer_size,
                                                                            std::stof(param_0),
                                                                            std::stof(param_1),
                                                                            std::stof(param_2),
                                                                            std::stof(param_3),
                                                                            std::stof(param_4),
                                                                            std::stof(param_5),
                                                                            std::stof(param_6),
                                                                            std::stof(param_7),
                                                                            std::stof(param_8),
                                                                            std::stof(param_9),
                                                                            std::stof(param_10),
                                                                            std::stof(param_11)
                                         ));
            }
            break;
        case CachePolicy::CACHEUS:
            UnittestUtils::make_test(trace_file,
                                     std::make_shared<CacheusCacheManager>(buffer_size));
            break;
        default:
            break;
    }
    timeval end_time;
    gettimeofday(&end_time, NULL);
#ifdef LOG
    std::cerr << (end_time.tv_sec - start_time.tv_sec) + (end_time.tv_usec - start_time.tv_usec) / 1000000.0 << std::endl;
#endif
    return 0;
}


