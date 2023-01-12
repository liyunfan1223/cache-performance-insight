//
// Created by MorphLing on 2022/10/25.
//

#include <iostream>

#include "managers/stw_cache_manager.h"
#include "utils/unittest_utils.h"

int main() {
    std::vector<Key> access_list;
    UnittestUtils::get_access_list("../../traces/P1.lis", access_list);
    UnittestUtils::make_test("../../traces/P1.lis", std::shared_ptr<CacheManager>(new STWCacheManager(65536)));
    return 0;
}