//
// Created by l50029536 on 2022/9/29.
//

#include "lfu_cache_manager.h"

RC LFUCacheManager::get(const Key & key) {
    int32_t freq = 1;
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
        freq = item->freq + 1;
        u_map_.erase(item->key);
        buffer_set_.erase(item);
    }
    auto result = buffer_set_.insert(Status(freq, timestamp_++, key));
    u_map_[key] = result.first;
    if (timestamp_ % 10000 == 0) {
        std::cerr << statics();
    }
    return RC::SUCCESS;
}

RC LFUCacheManager::put(const Key &key, const Value & value) { return RC::UNIMPLEMENT; }

std::string LFUCacheManager::get_name()
{
    return std::string("LFU");
}