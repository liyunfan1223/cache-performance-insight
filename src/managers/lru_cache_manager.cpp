//
// Created by MorphLing on 2022/9/28.
//

#include "lru_cache_manager.h"

RC LRUCacheManager::get(const Key & key) {
    if (lruList_.count(key) == 0) {
        miss_count_ += 1;
        if (lruList_.size() == buffer_size_) {
            lruList_.pop_back();
        }
    } else {
        hit_count_ += 1;
        lruList_.remove(key);
    }
    lruList_.push_front(key);
    ts++;
    if (ts % 10000 == 0) {
        std::cerr << statics();
    }
    return RC::SUCCESS;
}

RC LRUCacheManager::put(const Key &key, const Value & value) { return RC::UNIMPLEMENT; }

std::string LRUCacheManager::get_name()
{
    return std::string("LRU");
}