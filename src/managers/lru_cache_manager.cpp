//
// Created by MorphLing on 2022/9/28.
//

#include <cassert>
#include "lru_cache_manager.h"

RC LRUCacheManager::get(const Key & key) {
    if (u_map_.count(key) == 0) {
        miss_count_ += 1;
        if (linkList_.size == buffer_size_) {
            assert(u_map_.count(linkList_.tail->key) != 0);
            u_map_.erase(linkList_.tail->key);
            linkList_.PopBack();
        }
    } else {
        hit_count_ += 1;
        linkList_.Remove(u_map_[key]);
    }
    linkList_.PushFront(key);
    u_map_[key] = linkList_.head;
    return RC::SUCCESS;
}

RC LRUCacheManager::put(const Key &key, const Value & value) {
    return RC::UNIMPLEMENT;
}

std::string LRUCacheManager::get_name()
{
    return std::string("LRU_CACHE_MANAGER");
}