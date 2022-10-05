//
// Created by l50029536 on 2022/9/30.
//

#pragma once

#include <unordered_map>
#include "managers/cache_manager.h"
#include "data_structures/link_list.h"
#include "data_structures/lru_list.h"

class ARCCacheManager: public CacheManager {
public:
    ARCCacheManager(int32_t buffer_size): CacheManager(buffer_size)
    {
        p_ = 0;
    }

    ~ARCCacheManager()
    {}
    RC get(const Key & key) override;
    RC put(const Key & key, const Value & value) override;
    std::string get_name() override;
    RC check_consistency() override;
private:
    RC replace_(const Key & key);
    LRUList lruList_t1_, lruList_t2_, lruList_b1_, lruList_b2_;
    double p_;
};

