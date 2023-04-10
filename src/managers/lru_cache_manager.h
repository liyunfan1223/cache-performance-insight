//
// Created by MorphLing on 2022/9/28.
//

#pragma once

#include <unordered_map>

#include "def.h"
#include "cache_manager.h"
#include "data_structures/link_list.h"
#include "data_structures/lru_list.h"

class LRUCacheManager: public CacheManager {
public:
    LRUCacheManager(int32_t buffer_size): CacheManager(buffer_size)
    {}

    ~LRUCacheManager()
    {}
    RC get(const Key & key) override;
    RC put(const Key & key, const Value & value) override;
    std::string get_name() override;
private:
    LRUList<Key> lruList_;
    int ts = 0;
};
