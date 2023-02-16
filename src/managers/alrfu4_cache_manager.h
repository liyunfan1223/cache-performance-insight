//
// Created by MorphLing on 2023/2/15.
//
#include "cache_manager.h"
#include "data_structures/dynamic_decay_heap.h"
#include "data_structures/dynamic_decay_lru.h"

#ifndef CACHE_PERFORMANCE_INSIGHT_ALRFU4_CACHE_MANAGER_H
#define CACHE_PERFORMANCE_INSIGHT_ALRFU4_CACHE_MANAGER_H

class ALRFU4CacheManager: public CacheManager {
public:
    ALRFU4CacheManager(int32_t buffer_size, int32_t update_interval = 20000,
                       double cur_half = 5, double delta_ratio = 0.1, double lambda = 5, double store_ratio = 8,
                       double score_hit = 1, double score_miss = 4):
                       CacheManager(buffer_size), update_interval_(update_interval), store_lru_(store_ratio * buffer_size),
                       indicate_lru_(store_ratio * buffer_size), store_ratio_(store_ratio), score_hit_(score_hit), score_miss_(score_miss)
    {
        interval_hit_count_ = 0;
        interval_miss_count_ = 0;
        indicate_hit_count_ = 0;
        indicate_miss_count_ = 0;
        interval_count_ = 0;
        // default half life = 1 * buffer_size
        cur_half_ = cur_half;
        ori_half_ = cur_half;
        delta_ratio_ = delta_ratio;
        lambda_ = lambda;
//        cur_decay_ratio_exp_ = log(pow(0.5, (double)1.0 / (cur_half_ * buffer_size)));
        cur_decay_ratio_exp_ = log(0.5) / (cur_half_ * buffer_size);
        update_interval_ = update_interval;
    }

    ~ALRFU4CacheManager() override = default;

    RC get(const Key &key) override;

    RC put(const Key &key, const Value &value) override;

    std::string get_name() override;

    std::string get_configuration() override;

    RC check_consistency() override;

public:

private:
    void update_cur_decay_ratio();
    int32_t update_interval_;
    int32_t interval_hit_count_, interval_miss_count_, indicate_hit_count_, indicate_miss_count_, interval_count_;
    int32_t indicate_hit_count2_, indicate_miss_count2_;
    DDHeap dd_heap_, indicate_dd_heap_, store_heap_, indicate_store_heap_, indicate_dd_heap2_, indicate_store_heap2_;
    std::list<bool> access_status_, indicate_status_;
    int32_t ts_;
    double score_hit_, score_miss_;
    double cur_half_, ori_half_;
    double cur_decay_ratio_exp_;
    double lambda_ = 5;
    double delta_ratio_ = 0.1;
    double store_ratio_;
    int32_t stable_count_ = 0;
    int32_t debug_counter = 0;
    DDLru store_lru_, indicate_lru_;
    std::unordered_map<Key, double> score_, indicate_score_;
};


#endif //CACHE_PERFORMANCE_INSIGHT_ALRFU4_CACHE_MANAGER_H
