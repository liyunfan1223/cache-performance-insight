//
// Created by MorphLing on 2023/5/23.
//

#ifndef CACHE_PERFORMANCE_INSIGHT_RGC_CACHE_MANAGER_H
#define CACHE_PERFORMANCE_INSIGHT_RGC_CACHE_MANAGER_H

#include "def.h"
#include "managers/cache_manager.h"
#include "data_structures/multi_lru.h"

class RGCReplacer {
    struct RGCEntry {
        RGCEntry() = default;
        RGCEntry(std::list<Key>::iterator key_iter, int insert_level, int insert_ts) {
            this->key_iter = key_iter;
            this->insert_level = insert_level;
            this->insert_ts = insert_ts;
        }

        std::list<Key>::iterator key_iter;
        int insert_level{};
        int insert_ts{};
    };
public:
    RGCReplacer(int32_t size, double init_half,
                double hit_point, int max_points_bits, double ghost_size_ratio):
                size_(size), init_half_(init_half), hit_points_(hit_point),
                max_points_bits_(max_points_bits), ghost_size_ratio_(ghost_size_ratio)
    {
        cur_half_ = init_half_;
        max_points_ = (1 << max_points_bits_) - 1;
        ghost_size_ = size_ * ghost_size_ratio;
        min_level_non_empty_ = max_points_;
        min_level_non_empty_ghost_ = max_points_;
        real_lru_.resize(max_points_);
        ghost_lru_.resize(max_points_);
        UpdateHalf(init_half_);
    }
    int Access(Key key) {
        bool hit = true;
        int32_t inserted_level = hit_points_;
        if (real_map_.count(key) == 0) {
            // miss
            hit = false;
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
                while (ghost_lru_[min_level_non_empty_ghost_].empty() && min_level_non_empty_ghost_ <= max_points_) {
                    min_level_non_empty_ghost_++;
                }
//                inserted_level += level * 2;
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
//            inserted_level += level * 2;
            inserted_level += level;
            while(real_lru_[min_level_non_empty_].empty()) {
                min_level_non_empty_++;
            }
        }
        inserted_level = std::min(inserted_level, max_points_ - 1);
        real_lru_[inserted_level].push_front(key);
        real_map_[key] = RGCEntry(real_lru_[inserted_level].begin(), inserted_level, cur_ts_);
        if (inserted_level < min_level_non_empty_) {
            min_level_non_empty_ = inserted_level;
        }
        cur_ts_++;
        if (cur_ts_ >= next_rolling_ts_) {
            Rolling();
        }
        return hit;
    }
    void Evict() {
        // evict key in real
        Key evict_key = real_lru_[min_level_non_empty_].back();
        real_lru_[min_level_non_empty_].pop_back();
        real_map_.erase(evict_key);
        // move to ghost
        if (ghost_size_ != 0 && min_level_non_empty_ != 0) {
            // evict ghost
            if (ghost_map_.size() >= ghost_size_) {
                Key evict_key = ghost_lru_[min_level_non_empty_ghost_].back();
                ghost_lru_[min_level_non_empty_ghost_].pop_back();
                ghost_map_.erase(evict_key);
                while (ghost_lru_[min_level_non_empty_ghost_].empty() && min_level_non_empty_ghost_ < max_points_ + 1) {
                    min_level_non_empty_ghost_++;
                }
            }
            // min_level_non_empty_ == evict_key's level
            ghost_lru_[min_level_non_empty_].push_front(evict_key);
            ghost_map_[evict_key] = RGCEntry(ghost_lru_[min_level_non_empty_].begin(), min_level_non_empty_, cur_ts_);
            if (min_level_non_empty_ghost_ > min_level_non_empty_) {
                min_level_non_empty_ghost_ = min_level_non_empty_;
            }
        }
        while (real_lru_[min_level_non_empty_].empty()) {
            min_level_non_empty_++;
        }
    }
    void Rolling() {
        for (int i = 1; i < max_points_; i++) {
            if (!real_lru_[i].empty()) {
                real_lru_[i / 2].splice(real_lru_[i / 2].begin(), real_lru_[i]);
                if (!real_lru_[i / 2].empty()) {
                    min_level_non_empty_ = std::min(min_level_non_empty_, i / 2);
                }
            }
            ghost_lru_[i / 2].splice(ghost_lru_[i / 2].begin(), ghost_lru_[i]);
            if (!ghost_lru_[i / 2].empty()) {
                min_level_non_empty_ghost_ = std::min(min_level_non_empty_ghost_, i / 2);
            }
        }
        next_rolling_ts_ = cur_ts_ + cur_half_ * size_;
        rolling_ts.push_back(cur_ts_);
        if (rolling_ts.size() > max_points_bits_) {
            rolling_ts.pop_front();
        }
    }
    void UpdateHalf(double cur_half) {
        cur_half_ = cur_half;
        if (cur_half_ < (double)1 / size_) {
            cur_half_  = (double)1 / size_;
        }
        if (cur_half_ > 1e14 / size_) {
            cur_half_  = 1e14 / size_;
        }
        next_rolling_ts_ = std::min(next_rolling_ts_, cur_ts_ + (int)(cur_half_ * size_));
    }
    void ReportAndClear(int32_t &miss_count, int32_t &hit_count) {
        miss_count = interval_miss_count_;
        hit_count = interval_hit_count_;
        interval_miss_count_ = 0;
        interval_hit_count_ = 0;
    }
    double GetCurHalf() const {
        return cur_half_;
    }
private:
    int32_t GetCurrentLevel(const RGCEntry &status) {
        int32_t est_level = status.insert_level;
        if (rolling_ts.empty()) {
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
    double cur_half_;
private:
    // 当前半衰期系数
    double hit_points_; // 命中后得分
    int32_t max_points_bits_; // 最高得分为 (1 << max_points_bits_) - 1
    int32_t max_points_; // 最高得分
    int32_t min_level_non_empty_; // 当前最小的得分
    int32_t min_level_non_empty_ghost_; // 虚缓存当前最小的得分
    double ghost_size_ratio_; // 虚缓存大小比例
    int32_t ghost_size_;
    int32_t interval_hit_count_ = 0; // 统计区间命中次数
    int32_t interval_miss_count_ = 0; // 统计区间为命中次数
    int32_t next_rolling_ts_ = INT32_MAX; // 下一次滚动的时间戳
    int32_t cur_ts_ = 0; // 当前时间戳
    std::vector<std::list<Key> > real_lru_, ghost_lru_;
    std::unordered_map<Key, RGCEntry> real_map_, ghost_map_;
    std::list<int32_t> rolling_ts;
};

class RGCCacheManager: public CacheManager {
public:
    RGCCacheManager(int32_t buffer_size, double init_half = 10000.0f,
                    double hit_point = 1.0f, int32_t max_points_bits = 16, double ghost_size_ratio = 8.0f,
                    double lambda = 0.1f, int32_t update_interval = 20000, double simulator_ratio = 30.0f):
        CacheManager(buffer_size),
        replacer_r_(buffer_size, init_half, hit_point, max_points_bits, ghost_size_ratio),
        replacer_s_(buffer_size, init_half / (1 + simulator_ratio), hit_point, max_points_bits, ghost_size_ratio),
        lambda_(lambda), update_interval_(update_interval), init_half_(init_half), simulator_ratio_(simulator_ratio) {
    }
    RC get(const Key &key) override;

    RC put(const Key &key, const Value &value) override;

    std::string get_name() override;
private:
    RGCReplacer replacer_r_;
    RGCReplacer replacer_s_;
    double lambda_; // 学习率
    int32_t update_interval_; // 更新间隔
    int32_t ts_{};
    int32_t stable_count_{};
    double init_half_;
    double simulator_ratio_;
};


#endif //CACHE_PERFORMANCE_INSIGHT_RGC_CACHE_MANAGER_H
