//
// Created by MorphLing on 2023/1/4.
//

#include <iostream>

#include "managers/stw2_cache_manager.h"
#include "utils/unittest_utils.h"

int main() {
    std::vector<Key> access_list;
    UnittestUtils::make_test("../../traces/P1.lis", std::shared_ptr<CacheManager>(new STW2CacheManager(65536)));
    return 0;
}