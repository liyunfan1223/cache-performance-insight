//
// Created by Clouds on 2023/1/20.
//

#include "efsw_cache_manager.h"

RC EFSWCacheManager::get(const Key &key) {

    timestamp_++;
//    if (access_window_.size() == window_size_) {
//        Key &front = access_window_.front();
//        short_term_freq_[front]--;
//        if (u_map_.count(front) != 0) {
//            auto item = u_map_.find(front);
//            buffer_set_.erase(item->second);
//            buffer_set_.insert(Status(short_term_freq_[front], front, item->second->timestamp));
//        }
//        access_window_.pop_front();
//    }
//    access_window_.push_back(key);
    int32_t last_access_time_stamp = last_access_.find(key) != last_access_.end() ? last_access_[key] : -1;
    score_[key] *= exp(-exponential_decay_ratio_ * (timestamp_ - last_access_time_stamp));
    last_access_[key] = timestamp_;
    if (u_map_.count(key) != 0) {
        hit_count_++;
        score_[key] += hit_score_;
        auto item = u_map_.at(key);
        u_map_.erase(item->key);
        buffer_set_.erase(item);
    } else {
        miss_count_++;
        score_[key] += miss_score_;
        if (u_map_.size() == buffer_size_) {
            auto item = buffer_set_.begin();
            u_map_.erase(item->key);
            buffer_set_.erase(item);
        }
    }
    auto result = buffer_set_.insert(Status(score_[key], key, timestamp_));
    u_map_[key] = result.first;
    return RC::SUCCESS;
}

RC EFSWCacheManager::put(const Key &key, const Value &value) {
    return RC::UNIMPLEMENT;
}

std::string EFSWCacheManager::get_name() {
    return std::string("EFSW") + get_configuration();
}

std::string EFSWCacheManager::get_configuration() {
    return " half life ratio:" + std::to_string(half_life_ratio_) +
           " miss score:" + std::to_string(miss_score_) +
           " hit score:" + std::to_string(hit_count_);
}

RC EFSWCacheManager::check_consistency() {
    if (u_map_.size() > buffer_size_ || buffer_set_.size() > buffer_size_) {
        return RC::FAILED;
    }
    return RC::SUCCESS;
}
