//
// Created by MorphLing on 2023/9/24.
//

#ifndef CACHE_PERFORMANCE_INSIGHT_RGC2_CACHE_MANAGER_H
#define CACHE_PERFORMANCE_INSIGHT_RGC2_CACHE_MANAGER_H

#include "def.h"
#include "managers/cache_manager.h"
#include "data_structures/multi_lru.h"

//#define LAST_TIER_RATIO 4

class RGC2Replacer {
    struct RGCEntry {
        RGCEntry() = default;
        RGCEntry(std::list<Key>::iterator key_iter, int insert_level, int insert_ts, bool h_recency) {
            this->key_iter = key_iter;
            this->insert_level = insert_level;
            this->insert_ts = insert_ts;
            this->h_recency = h_recency;
        }

        std::list<Key>::iterator key_iter;
        int insert_level{};
        int insert_ts{};
        bool h_recency; // 高时近性 说明在顶层LRU中
    };
public:
    RGC2Replacer(int32_t size, double init_half,
                 double hit_points, int max_points_bits, double ghost_size_ratio, double top_ratio, double mru_ratio,
                 int32_t tiers):
            size_(size), init_half_(init_half), hit_points_(hit_points),
            max_points_bits_(max_points_bits), ghost_size_ratio_(ghost_size_ratio), top_ratio_(top_ratio),
            mru_ratio_(mru_ratio), tiers_(tiers)
    {
        cur_half_ = init_half_;
        max_points_ = (1 << max_points_bits_) - 1;
        ghost_size_ = size_ * ghost_size_ratio;
        min_level_non_empty_ = new int32_t [tiers_];
        min_level_non_empty_ghost_ = new int32_t [tiers_];
        real_lru_ = new std::vector<std::list<Key>>[tiers_];
        ghost_lru_ = new std::vector<std::list<Key>>[tiers_];
        for (int p = 0; p < tiers_; p++) {
            min_level_non_empty_[p] = max_points_;
            min_level_non_empty_ghost_[p] = max_points_;
            real_lru_[p].resize(max_points_);
            ghost_lru_[p].resize(max_points_);
        }
        UpdateHalf(init_half_);
        lru_size_ = std::max(1, (int)(top_ratio_ * size));
        rgc_size_ = size_ - lru_size_;
//        size_ = size_ - lru_size_;
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
                int p = GetCurrentPart(ghost_map_[key]);
                // erase key in ghost
                ghost_lru_[p][level].erase(hit_iter);
                ghost_map_.erase(key);
                while (ghost_lru_[p][min_level_non_empty_ghost_[p]].empty() && min_level_non_empty_ghost_[p] <= max_points_) {
                    min_level_non_empty_ghost_[p]++;
                }
                inserted_level += level;
            }
        } else {
            // hit
            interval_hit_count_++;
            if (!real_map_[key].h_recency) {
                std::list<Key>::iterator hit_iter = real_map_[key].key_iter;
                int level = GetCurrentLevel(real_map_[key]); // real_map_[key].second;
                int p = GetCurrentPart(real_map_[key]);
                // erase key in real, use level in real
                real_lru_[p][level].erase(hit_iter);
                real_map_.erase(key);
                inserted_level += level;
                while(real_lru_[p][min_level_non_empty_[p]].empty()) {
                    min_level_non_empty_[p]++;
                }
            } else {
                inserted_level += real_map_[key].insert_level;
                top_lru_.erase(real_map_[key].key_iter);
                real_map_.erase(key);
            }
        }
        inserted_level = std::min(inserted_level, max_points_ - 1);

        if (top_lru_.size() >= lru_size_) {
            Key key = top_lru_.back();
            int lvl = real_map_[key].insert_level;
            real_lru_[0][lvl].push_front(key);
            real_map_[key] = RGCEntry(real_lru_[0][lvl].begin(), lvl, cur_ts_, 0);
            if (lvl < min_level_non_empty_[0]) {
                min_level_non_empty_[0] = lvl;
            }
            top_lru_.pop_back();
        }
        top_lru_.push_front(key);
        real_map_[key] = RGCEntry(top_lru_.begin(), inserted_level, cur_ts_, 1);
        // real_lru_[inserted_level].push_front(key);
        // real_map_[key] = RGCEntry(real_lru_[inserted_level].begin(), inserted_level, cur_ts_);
        // if (inserted_level < min_level_non_empty_) {
        //     min_level_non_empty_ = inserted_level;
        // }
        cur_ts_++;
        if (cur_ts_ >= next_rolling_ts_) {
            Rolling();
        }
        return hit;
    }
    void Evict() {
        // evict key in real
        // churn resistance?
//        Key evict_key = real_lru_[min_level_non_empty_].back();
//        real_lru_[min_level_non_empty_].pop_back();
        Key evict_key;
        int evict_level;
        int mx_ts = 0, sum = 0;
        int sp = -1;
        int min_level = INT32_MAX;
        for (int p = 0; p < tiers_; p++) {
            min_level = std::min(min_level, min_level_non_empty_[p]);
        }
        for (int i = min_level; i < max_points_; i++) {
            for (int p = tiers_ - 1; p >= 0; p--) {
                if (real_lru_[p][i].empty()) {
                    continue;
                }
                // MRU
                if (real_map_[real_lru_[p][i].front()].insert_ts > mx_ts) {
                    mx_ts = real_map_[real_lru_[p][i].front()].insert_ts;
                    evict_key = real_lru_[p][i].front();
//                    assert(evict_key != 0);
                    evict_level = i;
                    sp = p;
                }
                sum += real_lru_[p][i].size();
                if (sum > mru_ratio_ * size_) {
                    break;
                }
            }
            if (sum > mru_ratio_ * size_) {
                break;
            }
        }
        real_lru_[sp][evict_level].pop_front();
//        } else {
//            evict_key = real_lru_[min_level_non_empty_].back();
//            real_lru_[min_level_non_empty_].pop_back();
//        }
        int inserted_lv = real_map_[evict_key].insert_level;
        int inserted_ts = real_map_[evict_key].insert_ts;
        real_map_.erase(evict_key);
        // move to ghost
        if (ghost_size_ != 0 && evict_level != 0) {
            // evict ghost
            if (ghost_map_.size() >= ghost_size_) {

                Key g_evict_key;
                int g_evict_level;
                int g_mx_ts = 0, g_sum = 0;
                int g_sp = 0;
                int g_min_level = INT32_MAX;
                for (int p = 0; p < tiers_; p++) {
                    g_min_level = std::min(g_min_level, min_level_non_empty_ghost_[p]);
                }

                for (int i = g_min_level ; i < max_points_; i++) {
                    for (int p = tiers_ - 1; p >= 0; p--) {
                        if (ghost_lru_[p][i].empty()) {
                            continue;
                        }
                        // MRU
                        if (ghost_map_[ghost_lru_[p][i].front()].insert_ts > g_mx_ts) {
                            g_mx_ts = ghost_map_[ghost_lru_[p][i].front()].insert_ts;
                            g_evict_key = ghost_lru_[p][i].front();
//                            assert(g_evict_key != 0);
                            g_evict_level = i;
                            g_sp = p;
                        }
                        g_sum += ghost_lru_[p][i].size();
                        if (g_sum > mru_ratio_ * size_) {
                            break;
                        }
                    }
                    if (g_sum > mru_ratio_ * size_) {
                        break;
                    }
                }
                ghost_lru_[g_sp][g_evict_level].pop_front();
                ghost_map_.erase(g_evict_key);
                while (ghost_lru_[g_sp][min_level_non_empty_ghost_[g_sp]].empty() && min_level_non_empty_ghost_[g_sp] < max_points_ + 1) {
                    min_level_non_empty_ghost_[g_sp]++;
                }
            }
            ghost_lru_[sp][evict_level].push_front(evict_key);
            ghost_map_[evict_key] = RGCEntry(ghost_lru_[sp][evict_level].begin(), inserted_lv, inserted_ts, 0);
            if (min_level_non_empty_ghost_[sp] > evict_level) {
                min_level_non_empty_ghost_[sp] = evict_level;
            }
        }
        while (real_lru_[sp][min_level_non_empty_[sp]].empty()) {
            min_level_non_empty_[sp]++;
        }
    }
    void Rolling() {
        int min_level = max_points_;
        for (int p = 0; p < tiers_; p++) {
            min_level = std::min(min_level, min_level_non_empty_[p]);
        }
        for (int p = tiers_ - 1; p >= 0; p--) {
            int t = p == tiers_ - 1 ? p : p + 1;
//            int r = p == tiers_ - 1 ? LAST_TIER_RATIO : 2;
            int r = 1 << p;
            for (int i = 1; i < max_points_; i++) {
                if (!real_lru_[p][i].empty()) {
                    real_lru_[t][i / r].splice(real_lru_[t][i / r].end(), real_lru_[p][i]);
                    min_level_non_empty_[t]  = std::min(min_level_non_empty_[t], i / r);
                }
                if (!ghost_lru_[p][i].empty()) {
                    ghost_lru_[t][i / r].splice(ghost_lru_[t][i / r].end(), ghost_lru_[p][i]);
                    min_level_non_empty_ghost_[t] = std::min(min_level_non_empty_ghost_[t], i / r);
                }
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
    void ReportAndClear(int32_t &miss_count, int32_t &hit_count/*, int32_t &hit_top*/) {
        miss_count = interval_miss_count_;
        hit_count = interval_hit_count_;
//        hit_top = interval_hit_top_;
        interval_miss_count_ = 0;
        interval_hit_count_ = 0;
        interval_hit_top_ = 0;
    }
    double GetCurHalf() const {
        return cur_half_;
    }
    int h1, h2; //debug
private:
    int32_t GetCurrentLevel(const RGCEntry &status) {
        int32_t est_level = status.insert_level;
        if (rolling_ts.empty()) {
            return est_level;
        }
        auto iter = rolling_ts.begin();
        int pos = 0;
        for (int i = 0; i < rolling_ts.size(); i++) {
            if (status.insert_ts < *iter) {
                est_level >>= pos;
                pos++;
                if (!est_level) {
                    break;
                }
//                int times = rolling_ts.size() - i;
//                est_level >>= times;
//                if (times <= tiers_ - 1) {
//                    est_level >>= times;
//                } else {
//                    est_level >>= (tiers_ - 1) + (times - (tiers_ - 1)) * (LAST_TIER_RATIO  == 2 ? 1 : 2);
//                }
//                break;
            }
            iter++;
        }
        return est_level;
    }
    int32_t GetCurrentPart(const RGCEntry &status) {
        int32_t est_level = 0;
        if (rolling_ts.empty()) {
            return est_level;
        }
        auto iter = rolling_ts.begin();
        for (int i = 0; i < rolling_ts.size(); i++) {
            if (status.insert_ts < *iter) {
                est_level = rolling_ts.size() - i;
                break;
            }
            iter++;
        }
        if (est_level >= tiers_) {
            est_level = tiers_ - 1;
        }
        return est_level;
    }
    int32_t size_;
    double init_half_; // 初始半衰期系数
    double cur_half_;
    double mru_ratio_;
private:
    // 当前半衰期系数
    int32_t lru_size_; // LRU部分大小
    int32_t rgc_size_; // RGC部分大小
    double hit_points_; // 命中后得分
    int32_t max_points_bits_; // 最高得分为 (1 << max_points_bits_) - 1
    int32_t max_points_; // 最高得分
    double ghost_size_ratio_; // 虚缓存大小比例
    int32_t ghost_size_;
    int32_t interval_hit_count_ = 0; // 统计区间命中次数
    int32_t interval_miss_count_ = 0; // 统计区间为命中次数
    int32_t interval_hit_top_ = 0; // 在top上命中次数
    int32_t next_rolling_ts_ = INT32_MAX; // 下一次滚动的时间戳
    int32_t cur_ts_ = 0; // 当前时间戳

    int32_t tiers_;
    std::vector<std::list<Key> > *real_lru_, *ghost_lru_;
    int32_t *min_level_non_empty_; // 当前最小的得分
    int32_t *min_level_non_empty_ghost_; // 虚缓存当前最小的得分

//    std::vector<std::list<Key> > lr_real_lru_, lr_ghost_lru_;
//    int32_t lr_min_level_non_empty_; // 当前最小的得分
//    int32_t lr_min_level_non_empty_ghost_; // 虚缓存当前最小的得分

    std::list<Key> top_lru_;
    std::unordered_map<Key, RGCEntry> real_map_, ghost_map_;
    std::list<int32_t> rolling_ts;
    double top_ratio_;
};

class RGC2CacheManager: public CacheManager {
public:
    RGC2CacheManager(int32_t buffer_size, double init_half = 20.0f,
                     double hit_point = 4.0f, int32_t max_points_bits = 10, double ghost_size_ratio = 4.0f,
                     double lambda = 1.0f, int32_t update_interval = 20000, double simulator_ratio = 0.25f, double top_ratio = 0.01f,
                     double mru_ratio = 0.01f, double delta_bound = 10000.0f):
            CacheManager(buffer_size),
            replacer_r_(buffer_size, init_half, hit_point, max_points_bits, ghost_size_ratio, top_ratio, mru_ratio, 3),
            replacer_s_(buffer_size, init_half / (1 + simulator_ratio), hit_point, max_points_bits, ghost_size_ratio, top_ratio, mru_ratio, 3),
            lambda_(lambda), update_interval_(update_interval), init_half_(init_half), simulator_ratio_(simulator_ratio), delta_bound_(delta_bound) {
    }
    RC get(const Key &key) override;

    RC put(const Key &key, const Value &value) override;

    std::string get_name() override;
private:
    RGC2Replacer replacer_r_;
    RGC2Replacer replacer_s_;
    double lambda_; // 学习率
    int32_t update_interval_; // 更新间隔
    int32_t ts_{};
    int32_t stable_count_{};
    double init_half_;
    double simulator_ratio_;
    double delta_bound_;
};

#endif //CACHE_PERFORMANCE_INSIGHT_RGC2_CACHE_MANAGER_H
