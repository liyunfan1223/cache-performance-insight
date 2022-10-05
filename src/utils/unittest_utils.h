//
// Created by MorphLing on 2022/10/5.
//

#pragma once
#include "def.h"
#include "managers/cache_manager.h"

class UnittestUtils {
public:
    static RC make_test(const char * filename,
                      std::shared_ptr<CacheManager> cacheManager);
    static RC check_get(CacheManager * cacheManager, Key & key);

};
