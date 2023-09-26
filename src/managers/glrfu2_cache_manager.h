//
// Created by MorphLing on 2023/3/12.
//

#ifndef CACHE_PERFORMANCE_INSIGHT_GHOSTALRFU2CACHEMANAGER_H
#define CACHE_PERFORMANCE_INSIGHT_GHOSTALRFU2CACHEMANAGER_H

#include "def.h"
#include "managers/cache_manager.h"
#include "data_structures/multi_lru.h"


namespace glruf2 {
class GhostALRFU2Indicator;
    struct iter_status {
        iter_status() {}

        iter_status(std::list<Key>::iterator iter, int insert_level, int insert_ts) {
            this->iter = iter;
            this->insert_level = insert_level;
            this->insert_ts = insert_ts;
        }

        std::list<Key>::iterator iter;
        int insert_level;
        int insert_ts;
    };

    class GhostALRFU2CacheManager : public CacheManager {
    public:
        GhostALRFU2CacheManager(int32_t buffer_size, int32_t update_interval = 20000,
                                double cur_half = 5, double delta_ratio = 0.1, double lambda = 5, int start_level = 8,
                                int count_level_bits = 10, double ghost_ratio = 1, double delta_bound = 10000.0f) : CacheManager(buffer_size),
                                                                                     update_interval_(update_interval),
                                                                                     cur_half_(cur_half),
                                                                                     delta_ratio_(delta_ratio),
                                                                                     lambda_(lambda),
                                                                                     start_level_(start_level),
                                                                                     count_level_bits(count_level_bits),
                                                                                     count_level_(
                                                                                             1 << count_level_bits),
                                                                                     ghost_ratio_(ghost_ratio) {
            ts_ = 0;
            next_decay_ts_ = cur_half * buffer_size;
            prev_decay_ts_ = -1;
            ori_half_ = cur_half;
            min_level_non_empty = count_level_ + 1;
            min_level_non_empty_ghost = count_level_ + 1;
            real_lru_.resize(count_level_);
            ghost_lru_.resize(count_level_);
            // wrong...
            indicator = std::make_unique<GhostALRFU2Indicator>(buffer_size, update_interval,
                                                               cur_half / (1 + delta_ratio), delta_ratio, lambda,
                                                               start_level, count_level_bits, ghost_ratio);
        }

        ~GhostALRFU2CacheManager() override = default;

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
        int ts_, next_decay_ts_, prev_decay_ts_, min_level_non_empty, min_level_non_empty_ghost;
        std::vector<std::list<Key> > real_lru_, ghost_lru_;
        std::unordered_map<Key, iter_status> real_map_, ghost_map_;
        std::list<int> decay_ts;
        std::unique_ptr<GhostALRFU2Indicator> indicator;
        int stable_count_ = 0;
        double ori_half_, ghost_ratio_;
        int interval_hit_count_ = 0;
        double static_insert_lv = 0;
    };

    class GhostALRFU2Indicator {
    public:
        GhostALRFU2Indicator(int32_t buffer_size, int32_t update_interval = 20000,
                             double cur_half = 5, double delta_ratio = 0.1, double lambda = 5, int start_level = 8,
                             int count_level_bits = 10, double ghost_ratio = 1) :
                buffer_size_(buffer_size), update_interval_(update_interval), cur_half_(cur_half),
                delta_ratio_(delta_ratio), lambda_(lambda),
                start_level_(start_level), count_level_bits(count_level_bits), count_level_(1 << count_level_bits),
                ghost_ratio_(ghost_ratio) {
            ts_ = 0;
            next_decay_ts_ = cur_half * buffer_size;
            prev_decay_ts_ = -1;
            min_level_non_empty = count_level_ + 1;
            min_level_non_empty_ghost = count_level_ + 1;
            real_lru_.resize(count_level_);
            ghost_lru_.resize(count_level_);
            // indicator = std::make_unique<GhostALRFU2CacheManager>(buffer_size, update_interval, cur_half, delta_ratio, lambda, start_level, co)
        }

        RC get(const Key &key);

        int update_interval_, start_level_, count_level_, count_level_bits;
        double cur_half_, delta_ratio_, lambda_;
        int ts_, next_decay_ts_, prev_decay_ts_, min_level_non_empty, min_level_non_empty_ghost;
        std::vector<std::list<Key> > real_lru_, ghost_lru_;
        std::unordered_map<Key, iter_status> real_map_, ghost_map_;
        std::list<int> decay_ts;

        RC decay();

        int get_cur_level(const iter_status &status);

        int hit_count = 0;
        int mis_count = 0;
        int buffer_size_;
        double ghost_ratio_;

        void set_cur_half(double cur_half) {
            cur_half_ = cur_half;
            next_decay_ts_ = std::min(next_decay_ts_, (int) (ts_ + cur_half_ * buffer_size_));
        }
    };
}
#endif //CACHE_PERFORMANCE_INSIGHT_GHOSTALRFU2CACHEMANAGER_H
