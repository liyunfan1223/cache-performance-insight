//
// Created by lenovo on 2023/10/27.
//

#ifndef CACHE_PERFORMANCE_INSIGHT_RGC5_CACHE_MANAGER_H
#define CACHE_PERFORMANCE_INSIGHT_RGC5_CACHE_MANAGER_H

#include "def.h"
#include "managers/cache_manager.h"
#include "data_structures/multi_lru.h"

class RGC5Replacer {
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
        bool h_recency{}; // 高时近性 说明在顶层LRU中
    };
public:
    RGC5Replacer(int32_t size, double init_half,
                 double hit_points, int max_points_bits, double ghost_size_ratio, double top_ratio, double mru_ratio, int32_t mru_threshold, int32_t report_window_size):
            size_(size), init_half_(init_half), hit_points_(hit_points),
            max_points_bits_(max_points_bits), ghost_size_ratio_(ghost_size_ratio), top_ratio_(top_ratio),
            mru_ratio_(mru_ratio), mru_threshold_(mru_threshold), report_window_size_(report_window_size)
    {
        cur_half_ = init_half_;
        max_points_ = (1 << max_points_bits_) - 1;
        ghost_size_ = size_ * ghost_size_ratio;
        min_level_non_empty_ = max_points_ + 1;
        real_lru_.resize(max_points_ + 1);
        UpdateHalf(init_half_);
        lru_size_ = std::max(1, (int)(top_ratio_ * size));
        rgc_size_ = size_ - lru_size_;
        report_window_hits_ = 0;
    }
    int Access(Key key) {
        bool hit = true;
        int32_t inserted_level = hit_points_;
        if (report_window_.size() >= report_window_size_) {
            if (report_window_.front() == 1) {
                report_window_hits_--;
            }
            report_window_.pop_front();
        }
        if (real_map_.count(key) == 0) {
            // miss
            hit = false;
//            interval_miss_count_++;
            report_window_.push_back(0);
            if (real_map_.size() == size_) {
                Evict();
            }
            if (ghost_map_.count(key) != 0) {
                // use level in ghost
                std::list<Key>::iterator hit_iter = ghost_map_[key].key_iter;
                int level = GetCurrentLevel(ghost_map_[key]);
                // erase key in ghost
                ghost_lru_.erase(hit_iter);
                ghost_map_.erase(key);
                inserted_level += level;
            }
        } else {
            // hit
//            interval_hit_count_++;
            report_window_.push_back(1);
            report_window_hits_++;
            if (!real_map_[key].h_recency) {
                h1++;
                std::list<Key>::iterator hit_iter = real_map_[key].key_iter;
                int level = GetCurrentLevel(real_map_[key]); // real_map_[key].second;
                // erase key in real, use level in real
                real_lru_[level].erase(hit_iter);
                real_map_.erase(key);
                inserted_level += level;
                while(real_lru_[min_level_non_empty_].empty()) {
                    min_level_non_empty_++;
                }
            } else {
                h2++;
                inserted_level += real_map_[key].insert_level;
                top_lru_.erase(real_map_[key].key_iter);
                real_map_.erase(key);
            }
        }
        inserted_level = std::min(inserted_level, max_points_);

        if (top_lru_.size() >= lru_size_) {
            Key key = top_lru_.back();
            int lvl = real_map_[key].insert_level;
//            if (lvl != max_points_) {
                real_lru_[lvl].push_front(key);
                real_map_[key] = RGCEntry(real_lru_[lvl].begin(), lvl, cur_ts_, false);
//            } else {
//                real_lru_[lvl].push_back(key);
//                real_map_[key] = RGCEntry((--real_lru_[lvl].end()), lvl, cur_ts_, false);
//            }
            if (lvl < min_level_non_empty_) {
                min_level_non_empty_ = lvl;
            }
            top_lru_.pop_back();
        }
        top_lru_.push_front(key);
        real_map_[key] = RGCEntry(top_lru_.begin(), inserted_level, cur_ts_, true);
        cur_ts_++;
        if (cur_ts_ >= next_rolling_ts_) {
            Rolling();
        }
        return hit;
    }
    void Evict() {
        // evict key in real
        Key evict_key;
        int evict_level;
        int mx_ts = 0, sum = 0;
        bool front = false;
        if (min_level_non_empty_ <= mru_threshold_) {
            front = true;
            for (int i = min_level_non_empty_; i <= max_points_; i++) {
                if (real_lru_[i].empty()) {
                    continue;
                }
                // MRU
                if (real_map_[real_lru_[i].front()].insert_ts > mx_ts) {
                    mx_ts = real_map_[real_lru_[i].front()].insert_ts;
                    evict_key = real_lru_[i].front();
                    evict_level = i;
                }
                sum += real_lru_[i].size();
                if (sum > mru_ratio_ * size_) {
                    break;
                }
            }
//            real_lru_[evict_level].pop_front();
//        } else {
//            evict_key = real_lru_[min_level_non_empty_].back();
//            real_lru_[min_level_non_empty_].pop_back();
//        }
//            real_map_.erase(evict_key);
        } else {
            evict_key = real_lru_[min_level_non_empty_].back();
            evict_level = min_level_non_empty_;
//            real_lru_[min_level_non_empty_].pop_back();
//            real_map_.erase(evict_key);
        }
        if (front) {
            real_lru_[evict_level].pop_front();
        } else {
            real_lru_[evict_level].pop_back();
        }
        real_map_.erase(evict_key);
        // move to ghost
        if (ghost_size_ != 0 && evict_level != 0) {
            // evict ghost
            if (ghost_map_.size() >= ghost_size_) {
                Key evict_key = ghost_lru_.back();
                ghost_lru_.pop_back();
                ghost_map_.erase(evict_key);
//                while (ghost_lru_.empty() && min_level_non_empty_ghost_ < max_points_ + 1) {
//                    min_level_non_empty_ghost_++;
//                }
            }
            // min_level_non_empty_ == evict_key's level
            ghost_lru_.push_front(evict_key);
            ghost_map_[evict_key] = RGCEntry(ghost_lru_.begin(), evict_level, cur_ts_, 0);
//            if (min_level_non_empty_ghost_ > evict_level) {
//                min_level_non_empty_ghost_ = evict_level;
//            }
        }
        while (real_lru_[min_level_non_empty_].empty()) {
            min_level_non_empty_++;
        }
    }
    void Rolling() {
        for (int i = 1; i <= max_points_; i++) {
            if (!real_lru_[i].empty()) {
                if (mru_threshold_ != -1) {
                    real_lru_[i / 2].splice(real_lru_[i / 2].end(), real_lru_[i]);
                } else {
                    real_lru_[i / 2].splice(real_lru_[i / 2].begin(), real_lru_[i]);
                }
                if (!real_lru_[i / 2].empty()) {
                    min_level_non_empty_ = std::min(min_level_non_empty_, i / 2);
                }
            }
        }
        next_rolling_ts_ = cur_ts_ + cur_half_ * size_;
        prev_rolling_ts_ = cur_ts_;
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
        next_rolling_ts_ = prev_rolling_ts_ + (int)(cur_half_ * size_);
    }
    void Report(int32_t &miss_count, int32_t &hit_count) {
        miss_count = (int32_t)report_window_.size() - report_window_hits_;
        hit_count = report_window_hits_;
//        miss_count = interval_miss_count_;
//        hit_count = interval_hit_count_;
////        hit_top = interval_hit_top_;
//        interval_miss_count_ = 0;
//        interval_hit_count_ = 0;
//        interval_hit_top_ = 0;
    }
    double GetCurHalf() const {
        return cur_half_;
    }
    int h1{}, h2{}; //debug
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
    double mru_ratio_;
private:
    // 当前半衰期系数
    int32_t lru_size_; // LRU部分大小
    int32_t rgc_size_; // RGC部分大小
    double hit_points_; // 命中后得分
    int32_t max_points_bits_; // 最高得分为 (1 << max_points_bits_) - 1
    int32_t max_points_; // 最高得分
    int32_t min_level_non_empty_; // 当前最小的得分
    double ghost_size_ratio_; // 虚缓存大小比例
    int32_t ghost_size_;
//    int32_t interval_hit_count_ = 0; // 统计区间命中次数
//    int32_t interval_miss_count_ = 0; // 统计区间为命中次数
//    int32_t interval_hit_top_ = 0; // 在top上命中次数
    int32_t next_rolling_ts_ = INT32_MAX; // 下一次滚动的时间戳
    int32_t cur_ts_ = 0; // 当前时间戳
    int32_t prev_rolling_ts_ = 0;
    std::vector<std::list<Key> > real_lru_;
    std::list<Key> ghost_lru_;
    std::list<Key> top_lru_;
    std::unordered_map<Key, RGCEntry> real_map_, ghost_map_;
    std::list<int32_t> rolling_ts;
    double top_ratio_;
    int32_t mru_threshold_{};
    int32_t report_window_size_{};
    std::list<int32_t> report_window_;
    int32_t report_window_hits_{};
};

class RGC5CacheManager: public CacheManager {
public:
    RGC5CacheManager(int32_t buffer_size, double init_half = 20.0f,
                     double hit_point = 4.0f, int32_t max_points_bits = 10, double ghost_size_ratio = 4.0f,
                     double lambda = 1.0f, int32_t update_interval = 20000, double simulator_ratio = 0.5f, double top_ratio = 0.01f,
                     double mru_ratio = 0.01f, double delta_bound = 5.0f, bool update_equals_size = false, int32_t mru_threshold = 1024,
                     int32_t minimal_update_size = -1, double report_window_size_to_update = 20):
            CacheManager(buffer_size),
            lambda_(lambda),
            update_interval_(std::min(minimal_update_size != -1 ? minimal_update_size : INT32_MAX, std::max(100, buffer_size))),
            init_half_(init_half), simulator_ratio_(simulator_ratio), delta_bound_(delta_bound),
            replacer_r_(buffer_size, init_half, hit_point, max_points_bits, ghost_size_ratio, top_ratio, mru_ratio, mru_threshold, update_interval_ * report_window_size_to_update),
            replacer_s_(buffer_size, init_half / (1 + simulator_ratio), hit_point, max_points_bits, ghost_size_ratio, top_ratio, mru_ratio, mru_threshold, update_interval_ * report_window_size_to_update) {
//        if (update_equals_size) {
//            if (minimal_update_size != -1) {
//                update_interval_ = std::max(100, buffer_size);
//                update_interval_ = std::min(minimal_update_size, buffer_size);
//            }
//        }
    }
    RC get(const Key &key) override;

    RC put(const Key &key, const Value &value) override;

    std::string get_name() override;
private:
    int32_t update_interval_; // 更新间隔
    RGC5Replacer replacer_r_;
    RGC5Replacer replacer_s_;
    double lambda_; // 学习率
    int32_t ts_{};
    int32_t stable_count_{};
    double init_half_;
    double simulator_ratio_;
    double delta_bound_;
    int32_t report_ct{};
    std::list<int32_t> hit_recorder;
    int32_t recorder_hit_count{};
};


#endif //CACHE_PERFORMANCE_INSIGHT_RGC5_CACHE_MANAGER_H
