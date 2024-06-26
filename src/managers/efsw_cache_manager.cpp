//
// Created by Clouds on 2023/1/20.
//

#include "efsw_cache_manager.h"

RC EFSWCacheManager::get(const Key &key) {
    double score;
    if (luheap_.InHeap(key)) {
        score = hit_score_;
        hit_count_++;
    } else {
        score = miss_score_;
        luheap_store_.Add(key, miss_score_);
        miss_count_++;
        if (luheap_.Size() == buffer_size_) {
            luheap_.Pop();
        }
    }
    luheap_store_.Add(key, score);
    if (luheap_.InHeap(key)) {
        luheap_.Add(key, score);
    } else {
        luheap_.Add(key, luheap_store_.GetValue(key));
    }
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
           " hit score:" + std::to_string(hit_score_);
}

RC EFSWCacheManager::check_consistency() {
//    if (u_map_.size() > buffer_size_ || buffer_set_.size() > buffer_size_) {
//        return RC::FAILED;
//    }
    return RC::SUCCESS;
}
