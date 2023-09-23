//
// Created by MorphLing on 2023/1/4.
//
#define LOG
#include "stw2_cache_manager.h"

RC STW2CacheManager::get(const Key &key)
{
//    tot++;
    timestamp_++;
#ifdef LOG
    if (timestamp_ % 20000 == 0) {
        std::cout << statics() << '\n';
    }
#endif
    long_term_freq_[key]++;
    short_term_freq_[key]++;
    timestamp_++;
    if (u_map_.size() != buffer_set_.size()) {
        timestamp_++;
    }
    if (access_window_.size() == window_size_) {
        Key &front = access_window_.front();
        short_term_freq_[front]--;
        if (u_map_.find(front) != u_map_.end()) {
            auto item = u_map_.find(front);
            buffer_set_.erase(item->second);
            buffer_set_.insert(Status(calculate_score_for_key(front), front, item->second->timestamp));
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
    auto result = buffer_set_.insert(Status(calculate_score_for_key(key), key, timestamp_));
    u_map_[key] = result.first;
    return RC::SUCCESS;
}

RC STW2CacheManager::put(const Key &key, const Value &value) { return RC::UNIMPLEMENT; }

std::string STW2CacheManager::get_name()
{
    return {"STW2"};
}

RC STW2CacheManager::check_consistency() { return RC::UNIMPLEMENT; }

double STW2CacheManager::calculate_score_for_key(Key key) {
//    return ((double)long_term_freq_[key] / timestamp_)
//    / (EPSILON + 2);
//    return (long_term_freq_[key] * long_term_freq_[key]) / (long_term_freq_[key] + long_term_freq_[key]) / timestamp_;
//    return ((double)long_term_freq_[key] / timestamp_);
    return long_term_freq_[key];
}


// 2 spaces

// 12