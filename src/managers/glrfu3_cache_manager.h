//
// Created by MorphLing on 2023/3/13.
//

#ifndef CACHE_PERFORMANCE_INSIGHT_GLRFU3_CACHE_MANAGER_H
#define CACHE_PERFORMANCE_INSIGHT_GLRFU3_CACHE_MANAGER_H

#include "def.h"
#include "managers/cache_manager.h"
#include "data_structures/multi_lru.h"

struct iter_status {
    iter_status(){}
    iter_status(std::list<Key>::iterator iter, int insert_level, int insert_ts) {
        this->iter = iter;
        this->insert_level = insert_level;
        this->insert_ts = insert_ts;
    }
    std::list<Key>::iterator iter;
    int insert_level;
    int insert_ts;
};

class Ghost3ALRFUCacheManager : public CacheManager {
public:
    Ghost3ALRFUCacheManager(int32_t buffer_size, int32_t update_interval = 20000,
                           double cur_half = 5, double delta_ratio = 0.1, double lambda = 5, int start_level = 8, int count_level_bits = 10) : CacheManager(buffer_size),
                                                                                                                                               update_interval_(update_interval), cur_half_(cur_half), delta_ratio_(delta_ratio), lambda_(lambda),
                                                                                                                                               start_level_(start_level), count_level_bits(count_level_bits), count_level_(1 << count_level_bits)
    {
        ts_ = 0;
        next_decay_ts_ = cur_half * buffer_size;
        prev_decay_ts_ = -1;
        ori_half_ = cur_half;
        min_level_non_empty = count_level_ + 1;
        real_lru_.resize(count_level_);
        ghost_lru_.resize(count_level_);
    }

    ~Ghost3ALRFUCacheManager() override = default;

    RC get(const Key &key) override;

    RC put(const Key &key, const Value &value) override;

    std::string get_name() override;

    std::string get_configuration() override;

    RC check_consistency() override;


private:
    RC decay();
    RC self_adaptive();
    int get_cur_level(const iter_status &status);
    int update_interval_, start_level_, count_level_, count_level_bits;
    double cur_half_, delta_ratio_, lambda_;
    int ts_, next_decay_ts_, prev_decay_ts_, min_level_non_empty;
    std::vector<std::list<Key> > real_lru_, ghost_lru_;
    std::unordered_map<Key, iter_status> real_map_, ghost_map_;
    std::list<int> decay_ts;
    int stable_count_ = 0;
    double ori_half_;
    int interval_hit_count_ = 0;
    double ghost_score = 0;
    int ghost_hit_time = 0;
};

#endif //CACHE_PERFORMANCE_INSIGHT_GLRFU3_CACHE_MANAGER_H
