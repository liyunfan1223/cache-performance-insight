//
// Created by MorphLing on 2023/1/4.
//

#include "stw_cache_manager.h"

RC STWCacheManager::get(const Key &key)
{
    long_term_freq_[key]++;
    short_term_freq_[key]++;
    timestamp_++;
    if (access_window_.size() == window_size_) {
        Key &front = access_window_.front();
        short_term_freq_[front]--;
        if (u_map_.count(front) != 0) {
            auto item = u_map_.find(front);
            buffer_set_.erase(item->second);
            buffer_set_.insert(Status(short_term_freq_[front], front, item->second->timestamp));
        }
        access_window_.pop_front();
    }
    access_window_.push_back(key);

    if (u_map_.count(key) != 0) {
        hit_count_++;
        auto item = u_map_.at(key);
        u_map_.erase(item->key);
        buffer_set_.erase(item);
    } else {
        miss_count_++;
        if (u_map_.size() == buffer_size_) {
            auto item = buffer_set_.begin();
            u_map_.erase(item->key);
            buffer_set_.erase(item);
        }
    }
    auto result = buffer_set_.insert(Status(short_term_freq_[key], key, timestamp_));
    u_map_[key] = result.first;
    return RC::SUCCESS;
}

RC STWCacheManager::put(const Key &key, const Value &value) { return RC::UNIMPLEMENT; }

std::string STWCacheManager::get_name()
{
    return {"STW"};
}

RC STWCacheManager::check_consistency()
{
    if (u_map_.size() > buffer_size_ || buffer_set_.size() > buffer_size_) {
        return RC::FAILED;
    }
    return RC::SUCCESS;
}

