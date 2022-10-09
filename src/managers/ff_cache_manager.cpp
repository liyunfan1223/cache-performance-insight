//
// Created by MorphLing on 2022/10/9.
//

#include "ff_cache_manager.h"

RC FFCacheManager::get(const Key &key) {
    key_access_u_map_[key].pop_front();
    if (u_map_.count(key) == 0) {
        miss_count_++;
        if (buffer_set_.size() >= buffer_size_) {
            auto item = buffer_set_.begin();
            u_map_.erase(item->key);
            buffer_set_.erase(item);
        }
    } else {
        hit_count_++;
        auto item = u_map_[key];
        buffer_set_.erase(item);
    }
    int32_t future_access_timestamp = key_access_u_map_[key].size ? key_access_u_map_[key].head->key : INT32_MAX;
    auto result = buffer_set_.insert(Status(future_access_timestamp, key));
    u_map_[key] = result.first;
    return RC::UNIMPLEMENT;
}

RC FFCacheManager::put(const Key &key, const Value &value) { return RC::UNIMPLEMENT; }

std::string FFCacheManager::get_name() {
    return std::string("FF_CACHE_MANAGER");
}

RC FFCacheManager::check_consistency() {
    return CacheManager::check_consistency();
}
