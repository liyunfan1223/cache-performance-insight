//
// Created by MorphLing on 2022/10/25.
//

#include "mrf_cache_manager.h"


RC MRFCacheManager::get(const Key &key) {
    priorKeyFreq_[key]--;
    if (u_map_.count(key) == 0) {
        miss_count_++;
        if (buffer_set_.size() >= buffer_size_) {
            auto item = buffer_set_.begin();
            u_map_.erase(item->key);
            buffer_set_.erase(item);
        }
    } else {
        hit_count_++;
        buffer_set_.erase(u_map_[key]);
    }
    auto result = buffer_set_.insert(Status(priorKeyFreq_[key], key));
    u_map_[key] = result.first;
    return RC::SUCCESS;
}

RC MRFCacheManager::put(const Key &key, const Value &value) { return RC::DEFAULT; }

std::string MRFCacheManager::get_name() {
    return std::string("MRFCacheManager");
}

RC MRFCacheManager::check_consistency() {
    return CacheManager::check_consistency();
}
