//
// Created by l50029536 on 2022/9/29.
//

#include <iostream>
#include <cassert>

#include "managers/lfu_cache_manager.h"
#include "utils/unittest_utils.h"

int main() {
    UnittestUtils::make_test("../traces/P1.lis", std::shared_ptr<CacheManager>(new LFUCacheManager(65536)));
    std::vector<int32_t> access_order = {1, 1, 2, 3, 4, 5, 6, 3, 7, 4};
//    UnittestUtils::make_test(access_order, std::shared_ptr<CacheManager>(new LFUCacheManager(5)));
    return 0;
}