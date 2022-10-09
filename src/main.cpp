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
#include "managers/ff_cache_manager.h"

int main(int argc, char **argv) {
    std::vector<Key> access_list;
    UnittestUtils::get_access_list(argv[2], access_list);

//    UnittestUtils::make_test(argv[2],
//                             std::shared_ptr<CacheManager>(new LRUCacheManager(std::stoi(argv[1]))));
//    UnittestUtils::make_test(argv[2],
//                             std::shared_ptr<CacheManager>(new LFUCacheManager(std::stoi(argv[1]))));
    UnittestUtils::make_test(argv[2],
                             std::shared_ptr<CacheManager>(new ARCCacheManager(std::stoi(argv[1]))));
    UnittestUtils::make_test(argv[2],
                             std::shared_ptr<CacheManager>(new ARC2CacheManager(std::stoi(argv[1]), 0.02, access_list)));
//    UnittestUtils::make_test(argv[2],
//                             std::shared_ptr<CacheManager>(new FFCacheManager(std::stoi(argv[1]), access_list)));
    return 0;
}


