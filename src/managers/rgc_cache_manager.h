//
// Created by MorphLing on 2023/5/23.
//

#ifndef CACHE_PERFORMANCE_INSIGHT_RGC_CACHE_MANAGER_H
#define CACHE_PERFORMANCE_INSIGHT_RGC_CACHE_MANAGER_H

#include "def.h"
#include "managers/cache_manager.h"
#include "data_structures/multi_lru.h"

class RGCReplacer {
    struct RGCFrameStatus {
        RGCFrameStatus() {}

        RGCFrameStatus(std::list<Key>::iterator key_iter, int insert_level, int insert_ts) {
            this->key_iter = key_iter;
            this->insert_level = insert_level;
            this->insert_ts = insert_ts;
        }

        std::list<Key>::iterator key_iter;
        int insert_level;
        int insert_ts;
    };
public:
    RGCReplacer(int32_t size, double init_half, double lambda,
                double hit_point, int max_points_bits, double ghost_size_ratio):
                size_(size), init_half_(init_half), lambda_(lambda), hit_points_(hit_point),
                max_points_bits_(max_points_bits), ghost_size_ratio_(ghost_size_ratio)
    {
        max_points_ = (1 << max_points_bits_) - 1;
        cur_half_ = init_half_;
    }
    void Access(Key key) {
        int32_t inserted_level = hit_points_;
        if (real_map_.count(key) == 0) {
            // miss
            interval_miss_count_++;
            if (real_map_.size() == size_) {
                Evict();
            }
            if (ghost_map_.count(key) != 0) {
                // use level in ghost
                std::list<Key>::iterator hit_iter = ghost_map_[key].key_iter;
                int level = GetCurrentLevel(ghost_map_[key]);
                // erase key in ghost
                ghost_lru_[level].erase(hit_iter);
                ghost_map_.erase(key);
                while (ghost_lru_[min_level_non_empty_ghost_].size() == 0 && min_level_non_empty_ghost_ <= max_points_) {
                    min_level_non_empty_ghost_++;
                }
                inserted_level += level;
            }
        } else {
            // hit
            interval_hit_count_++;
            std::list<Key>::iterator hit_iter = real_map_[key].key_iter;
            int level = GetCurrentLevel(real_map_[key]); // real_map_[key].second;
            // erase key in real, use level in real
            real_lru_[level].erase(hit_iter);
            real_map_.erase(key);
            inserted_level += level;
            while(real_lru_[min_level_non_empty_].size() == 0) {
                min_level_non_empty_++;
            }
        }
        inserted_level = std::min(inserted_level, max_points_ - 1);
        real_lru_[inserted_level].push_front(key);
        real_map_[key] = RGCFrameStatus(real_lru_[inserted_level].begin(), inserted_level, cur_ts_);
        if (inserted_level < min_level_non_empty_) {
            min_level_non_empty_ = inserted_level;
        }
        cur_ts_++;
        if (cur_ts_ == next_rolling_ts_) {
            Rolling();
        }
    }
    void Evict() {
        // evict key in real
        Key evict_key = real_lru_[min_level_non_empty_].back();
        real_lru_[min_level_non_empty_].pop_back();
        real_map_.erase(evict_key);
        // move to ghost
        if (ghost_size_ratio_ != 0 && min_level_non_empty_ != 0) {
            // evict ghost
            if (ghost_map_.size() >= ghost_size_ratio_ * size_) {
                Key evict_key = ghost_lru_[min_level_non_empty_ghost_].back();
                ghost_lru_[min_level_non_empty_ghost_].pop_back();
                ghost_map_.erase(evict_key);
                while (ghost_lru_[min_level_non_empty_ghost_].size() == 0 && min_level_non_empty_ghost_ < max_points_ + 1) {
                    min_level_non_empty_ghost_++;
                }
            }
            ghost_lru_[min_level_non_empty_].push_front(evict_key);
            ghost_map_[evict_key] = RGCFrameStatus(ghost_lru_[min_level_non_empty_].begin(), min_level_non_empty_, cur_ts_);
            if (min_level_non_empty_ghost_ > min_level_non_empty_) {
                min_level_non_empty_ghost_ = min_level_non_empty_;
            }
        }
        while (real_lru_[min_level_non_empty_].size() == 0) {
            min_level_non_empty_++;
        }
    }
    void Rolling() {
        for (int i = 1; i < max_points_; i++) {
            if (real_lru_[i].size() != 0) {
                real_lru_[i / 2].splice(real_lru_[i / 2].begin(), real_lru_[i]);
                if (real_lru_[i / 2].size()) {
                    min_level_non_empty_ = std::min(min_level_non_empty_, i / 2);
                }
            }
            ghost_lru_[i / 2].splice(ghost_lru_[i / 2].begin(), ghost_lru_[i]);
            if (ghost_lru_[i / 2].size()) {
                min_level_non_empty_ghost_ = std::min(min_level_non_empty_ghost_, i / 2);
            }
        }
        next_rolling_ts_ = cur_ts_ + cur_half_ * size_;
        rolling_ts.push_back(cur_ts_);
        if (rolling_ts.size() > max_points_bits_) {
            rolling_ts.pop_front();
        }
    }
    void UpdateHalf(double cur_half);

private:
    int32_t GetCurrentLevel(const RGCFrameStatus &status) {
        int32_t est_level = status.insert_level;
        if (rolling_ts.size() == 0) {
            return est_level;
        }
        auto iter = rolling_ts.begin();
        for (int i = 0; i < rolling_ts.size(); i++) {
            if (status.insert_ts < *iter) {
                est_level >>= rolling_ts.size() - i;
                break;
            }
            iter++;
        }
        return est_level;
    }
    int32_t size_;
    double init_half_; // 初始半衰期系数
    double cur_half_; // 当前半衰期系数
    double lambda_; // 学习率
    double hit_points_; // 命中后得分
    int32_t max_points_bits_; // 最高得分为 (1 << max_points_bits_) - 1
    int32_t max_points_; // 最高得分
    int32_t min_level_non_empty_; // 当前最小的得分
    int32_t min_level_non_empty_ghost_; // 虚缓存当前最小的得分
    double ghost_size_ratio_; // 虚缓存大小比例
    int32_t interval_hit_count_; // 统计区间命中次数
    int32_t interval_miss_count_; // 统计区间为命中次数
    int32_t next_rolling_ts_; // 下一次滚动的时间戳
    int32_t cur_ts_; // 当前时间戳
    std::vector<std::list<Key> > real_lru_, ghost_lru_;
    std::unordered_map<Key, RGCFrameStatus> real_map_, ghost_map_;
    std::list<int32_t> rolling_ts;
};

class RGCCacheManager: public CacheManager {

};


#endif //CACHE_PERFORMANCE_INSIGHT_RGC_CACHE_MANAGER_H
