//
// Created by MorphLing on 2023/2/7.
//

// Adaptive LRFU
#pragma once

#include "managers/cache_manager.h"
#include "data_structures/dynamic_decay_heap.h"

class ALRFUCacheManager : public CacheManager {
public:
    ALRFUCacheManager(int32_t buffer_size, int32_t update_interval = 20000,
                      double cur_half = 5, double delta_ratio = 0.1, double lambda = 5): CacheManager(buffer_size),
    update_interval_(update_interval)
    {
        interval_hit_count_ = 0;
        interval_miss_count_ = 0;
        indicate_hit_count_ = 0;
        indicate_miss_count_ = 0;
        interval_count_ = 0;
        // default half life = 1 * buffer_size
        cur_half_ = cur_half;
        delta_ratio_ = delta_ratio;
        lambda_ = lambda;
//        cur_decay_ratio_exp_ = log(pow(0.5, (double)1.0 / (cur_half_ * buffer_size)));
        cur_decay_ratio_exp_ = log(0.5) / (cur_half_ * buffer_size);
        update_interval_ = update_interval;
    }

    ~ALRFUCacheManager() override = default;

    RC get(const Key &key) override;

    RC put(const Key &key, const Value &value) override;

    std::string get_name() override;

    std::string get_configuration() override;

    RC check_consistency() override;

public:

private:
    void lazy_update_score(Key key);
    void update_cur_decay_ratio();
    void maintain(DDHeap &heap, Key key);
    int32_t update_interval_;
    int32_t interval_hit_count_, interval_miss_count_, indicate_hit_count_, indicate_miss_count_, interval_count_;
    int32_t indicate_hit_count2_, indicate_miss_count2_;
    DDHeap dd_heap_, indicate_dd_heap_, store_heap_, indicate_store_heap_, indicate_dd_heap2_, indicate_store_heap2_;
    std::unordered_map<Key, std::pair<double, int>> score_;
    std::list<bool> access_status_, indicate_status_;
    int32_t ts_;
    double cur_half_;
    double cur_decay_ratio_exp_;
    double lambda_ = 5;
    double delta_ratio_ = 0.1;
    int32_t debug_counter = 0;
};