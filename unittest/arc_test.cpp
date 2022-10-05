//
// Created by MorphLing on 2022/10/1.
//

#include <iostream>

#include "managers/arc_cache_manager.h"
#include "utils/unittest_utils.h"

int main() {
    UnittestUtils::make_test("../traces/P1.lis", std::shared_ptr<CacheManager>(new ARCCacheManager(100)));
    return 0;
}