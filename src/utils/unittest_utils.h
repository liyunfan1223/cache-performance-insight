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
    static RC get_access_list(const char * filename, std::vector<Key> & access_list);
    const char * DEFAULT_TRACE_PATH = "../traces/P1.lis";
    const int32_t DEFAULT_BUFFER_SIZE = 65536;
};
