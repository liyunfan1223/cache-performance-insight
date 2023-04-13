//
// Created by MorphLing on 2023/3/12.
//

#include "glrfu4_cache_manager.h"

using namespace glrfu4;

RC GhostALRFU4CacheManager::get(const Key &key) {
    int inserted_level = start_level_;
    int base_freq = 1;
    if (real_map_.count(key) == 0) {
        // miss
        increase_miss_count();
        if (real_map_.size() == buffer_size_) {
            // evict key in real
            Key evict_key = real_lru_[min_level_non_empty].back();
            real_lru_[min_level_non_empty].pop_back();
            int freq = real_map_[evict_key].insert_freq;
            real_map_.erase(evict_key);
            static_cache_lv -= min_level_non_empty;
            if (min_level_non_empty != 0) {
                // move to ghost
                if (ghost_map_.size() >= ghost_ratio_ * buffer_size_) {
                    Key evict_key = ghost_lru_[min_level_non_empty_ghost].back();
                    ghost_lru_[min_level_non_empty_ghost].pop_back();
//                    Key evict_key = ghost_lru_[min_level_non_empty_ghost].front();
//                    ghost_lru_[min_level_non_empty_ghost].pop_front();
                    ghost_map_.erase(evict_key);
                    while (ghost_lru_[min_level_non_empty_ghost].size() == 0 && min_level_non_empty_ghost < count_level_ + 1) {
                        min_level_non_empty_ghost++;
                    }
                }
                ghost_lru_[min_level_non_empty].push_front(evict_key);
                ghost_map_[evict_key] = iter_status(ghost_lru_[min_level_non_empty].begin(), min_level_non_empty, ts_, freq);
                if (min_level_non_empty_ghost > min_level_non_empty) {
                    min_level_non_empty_ghost = min_level_non_empty;
                }
                // std::make_pair(ghost_lru_[min_level_non_empty].begin(), min_level_non_empty);
            }
            while (real_lru_[min_level_non_empty].size() == 0) {
                min_level_non_empty++;
            }
        }
        if (ghost_map_.count(key) != 0) {
            // use level in ghost
            std::list<Key>::iterator hit_iter = ghost_map_[key].iter;

            int ts = ghost_map_[key].insert_ts;
            ref_interval += (ts_ + 1) - ts;

            int level = get_cur_level(ghost_map_[key]);
            // erase key in ghost
            ghost_lru_[level].erase(hit_iter);
            ghost_map_.erase(key);
            while (ghost_lru_[min_level_non_empty_ghost].size() == 0 && min_level_non_empty_ghost < count_level_ + 1) {
                min_level_non_empty_ghost++;
            }
            inserted_level = level + start_level_;

        } else {
            ref_interval += ghost_ratio_ * buffer_size_;
        }
        miss_level += inserted_level;
        miss_count ++;
    } else {
        // hit
        increase_hit_count();
        interval_hit_count_++;
        std::list<Key>::iterator hit_iter = real_map_[key].iter;
        // static_insert_lv += real_map_[key].insert_level;
        int level = get_cur_level(real_map_[key]); // real_map_[key].second;
        // erase key in real, use level in real
        real_lru_[level].erase(hit_iter);
        static_cache_lv -= level;
        real_map_.erase(key);
        base_freq += real_map_[key].insert_freq;
        ref_interval += (ts_ + 1) - real_map_[key].insert_ts;
        base_freq = std::min(base_freq, count_level_ / start_level_);
        inserted_level = level + start_level_;
        while(real_lru_[min_level_non_empty].size() == 0) {
            min_level_non_empty++;
        }
        hit_level += inserted_level;
        hit_count ++;
    }
    inserted_level = std::min(inserted_level, count_level_ - 1);
    real_lru_[inserted_level].push_front(key);
    real_map_[key] = iter_status(real_lru_[inserted_level].begin(), inserted_level, ts_, base_freq);
    if (inserted_level < min_level_non_empty) {
        min_level_non_empty = inserted_level;
    }
    ts_++;
//    if (ts_ % 10000 == 0) {
//        std::cerr << statics();
//    }

    if (ts_ == next_decay_ts_) {
        decay();
    }
    static_insert_fq += base_freq - 1;
    static_cache_lv += inserted_level;
    static_insert_lv += inserted_level - start_level_;
    if (ts_ % update_interval_ == 0) {
        self_adaptive();
    }
    return RC::SUCCESS;
}

RC GhostALRFU4CacheManager::put(const Key &key, const Value &value) {
    return RC::DEFAULT;
}

std::string GhostALRFU4CacheManager::get_name() {
    return {"G-LRFU4"};
}

std::string GhostALRFU4CacheManager::get_configuration() {
    return CacheManager::get_configuration();
}

RC GhostALRFU4CacheManager::check_consistency() {
    return CacheManager::check_consistency();
}

RC GhostALRFU4CacheManager::decay() {
    for (int i = 1; i < count_level_; i++) {
        if (real_lru_[i].size() != 0) {
            static_cache_lv -= i * real_lru_[i].size();
            static_cache_lv += i / 2 * real_lru_[i].size();
            real_lru_[i / 2].splice(real_lru_[i / 2].begin(), real_lru_[i]);
            if (real_lru_[i / 2].size()) {
                min_level_non_empty = std::min(min_level_non_empty, i / 2);
            }
        }
        ghost_lru_[i / 2].splice(ghost_lru_[i / 2].begin(), ghost_lru_[i]);
        if (ghost_lru_[i / 2].size()) {
            min_level_non_empty_ghost = std::min(min_level_non_empty_ghost, i / 2);
        }
    }
    next_decay_ts_ = ts_ + cur_half_ * buffer_size_;
    prev_decay_ts_ = ts_;
    decay_ts.push_back(ts_);
    if (decay_ts.size() > count_level_bits) {
        decay_ts.pop_front();
    }
//    static_cache_lv /= 2;
    return RC::SUCCESS;
}

int GhostALRFU4CacheManager::get_cur_level(const iter_status & status) {
    int est_level = status.insert_level;
    if (decay_ts.size() == 0) {
        return est_level;
    }
    auto iter = decay_ts.begin();
    for (int i = 0; i < decay_ts.size(); i++) {
        if (status.insert_ts < *iter) {
            est_level >>= decay_ts.size() - i;
            break;
        }
        iter++;
    }
    return est_level;
}

RC GhostALRFU4CacheManager::self_adaptive() {
    double avg_lv = (double) static_insert_lv / update_interval_;
    double avg_fq = (double) static_insert_fq / update_interval_;
    double avg_cache = (double) static_cache_lv / real_map_.size();

    double avg_lv_hit = hit_count != 0 ? (double)hit_level / hit_count : start_level_ * 4;
    double avg_lv_mis = miss_count != 0 ? (double)miss_level / miss_count : 0;
    double re_ref_interval = (double) ref_interval / update_interval_;
    double ratio = (double) hit_count / update_interval_;
    std::cerr << cur_half_ << " " << avg_lv << " " << avg_cache << " " << avg_fq * start_level_ << " " << avg_lv_hit << " " << avg_lv_mis << " " << re_ref_interval << " " << statics();
//    expect_lv_ = prev_static_lv;
//    expect_lv_ = 256;
//    expect_lv_ = 1;
    double a = avg_lv_hit;
    double b = avg_lv_mis * 2;
    if (a > b) {
        cur_half_ /= 1 + (a - b) / count_level_;
    } else {
        cur_half_ *= 1 + (b - a) / count_level_;
    }
    if (cur_half_ < (double)2000 / buffer_size_) {
        cur_half_  = (double)2000 / buffer_size_;
    }
    if (cur_half_ > 1e8 / buffer_size_) {
        cur_half_  = 1e8 / buffer_size_;
    }
    prev_static_lv = avg_lv;
    // update_counter
    next_decay_ts_ = std::min(next_decay_ts_, (int)(ts_ + cur_half_ * buffer_size_));
    next_decay_ts_ = std::max(next_decay_ts_, ts_ + 1);
    static_insert_lv = 0;
    static_insert_fq = 0;
    hit_level = miss_level = 0;
    hit_count = miss_count = 0;
    ref_interval = 0;
    return RC::SUCCESS;
}
