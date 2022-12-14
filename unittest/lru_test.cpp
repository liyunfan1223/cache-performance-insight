//
// Created by l50029536 on 2022/9/29.
//

#include <iostream>
#include <cassert>

#include "managers/lru_cache_manager.h"
#include "utils/unittest_utils.h"

int main() {
    UnittestUtils::make_test("../traces/P1.lis", std::shared_ptr<CacheManager>(new LRUCacheManager(65536)));
    return 0;
}