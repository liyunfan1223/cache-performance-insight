//
// Created by MorphLing on 2023/3/12.
//

#include "glrfu_cache_manager.h"

RC GhostALRFUCacheManager::get(const Key &key) {
    int inserted_level = start_level_;
    if (real_map_.count(key) == 0) {
        // miss
        increase_miss_count();
        if (real_map_.size() == buffer_size_) {
            // evict key in real
            Key evict_key = real_lru_[min_level_non_empty].back();
            real_lru_[min_level_non_empty].pop_back();
            real_map_.erase(evict_key);
            if (min_level_non_empty != 0) {
                // move to ghost
                ghost_lru_[min_level_non_empty].push_front(evict_key);
                ghost_map_[evict_key] = iter_status(ghost_lru_[min_level_non_empty].begin(), min_level_non_empty, ts_);
                // std::make_pair(ghost_lru_[min_level_non_empty].begin(), min_level_non_empty);
            }
            while (real_lru_[min_level_non_empty].size() == 0) {
                min_level_non_empty++;
            }
        }
        if (ghost_map_.count(key) != 0) {
            // use level in ghost
            std::list<Key>::iterator hit_iter = ghost_map_[key].iter;

            int level = get_cur_level(ghost_map_[key]);
            // erase key in ghost
            ghost_lru_[level].erase(hit_iter);
            ghost_map_.erase(key);
            inserted_level = level + start_level_;
        }
    } else {
        // hit
        increase_hit_count();
        interval_hit_count_++;
        std::list<Key>::iterator hit_iter = real_map_[key].iter;
        int level = get_cur_level(real_map_[key]); // real_map_[key].second;
        // erase key in real, use level in real
        real_lru_[level].erase(hit_iter);
        real_map_.erase(key);
        inserted_level = level + start_level_;
        while(real_lru_[min_level_non_empty].size() == 0) {
            min_level_non_empty++;
        }
    }
    inserted_level = std::min(inserted_level, count_level_ - 1);
    real_lru_[inserted_level].push_front(key);
    real_map_[key] = iter_status(real_lru_[inserted_level].begin(), inserted_level, ts_);
    if (inserted_level < min_level_non_empty) {
        min_level_non_empty = inserted_level;
    }
    indicator->get(key);
    ts_++;
    if (ts_ == next_decay_ts_) {
        decay();
    }
    if (ts_ % update_interval_ == 0) {
        self_adaptive();
    }
    return RC::SUCCESS;
}

RC GhostALRFUCacheManager::put(const Key &key, const Value &value) {
    return RC::DEFAULT;
}

std::string GhostALRFUCacheManager::get_name() {
    return {"G-LRFU"};
}

std::string GhostALRFUCacheManager::get_configuration() {
    return CacheManager::get_configuration();
}

RC GhostALRFUCacheManager::check_consistency() {
    return CacheManager::check_consistency();
}

RC GhostALRFUCacheManager::decay() {
    for (int i = 1; i < count_level_; i++) {
        if (real_lru_[i].size() != 0) {
            real_lru_[i / 2].splice(real_lru_[i / 2].begin(), real_lru_[i]);
            if (real_lru_[i / 2].size()) {
                min_level_non_empty = std::min(min_level_non_empty, i / 2);
            }
        }
        ghost_lru_[i / 2].splice(ghost_lru_[i / 2].begin(), ghost_lru_[i]);
    }
    next_decay_ts_ = ts_ + cur_half_ * buffer_size_;
    prev_decay_ts_ = ts_;
    decay_ts.push_back(ts_);
    if (decay_ts.size() > count_level_bits) {
        decay_ts.pop_front();
    }
    return RC::SUCCESS;
}

int GhostALRFUCacheManager::get_cur_level(const iter_status & status) {
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

RC GhostALRFUCacheManager::self_adaptive() {
    double cur_hit_ratio = (double)interval_hit_count_ / update_interval_;
    double ind_hit_ratio = (double)indicator->hit_count / update_interval_;
//    double cur_miss_ratio = (double)interval_miss_count_ / update_interval_;
//    double ind_miss_ratio = (double)indicate_miss_count_ / update_interval_;
//    double ind_hit_ratio2 = (double)indicate_hit_count2_ / update_interval_;
//    std::cerr << cur_half_ << " " << cur_hit_ratio << " " << ind_hit_ratio << " " << (double)hit_count() / ts_ << std::endl;
    if (cur_hit_ratio != 0 && ind_hit_ratio != 0) {
        if (fabs(ind_hit_ratio - cur_hit_ratio) >= EPSILON) {
            stable_count_ = 0;
            if (ind_hit_ratio > cur_hit_ratio) {
                double delta_ratio = (ind_hit_ratio / cur_hit_ratio - 1);
                cur_half_ /= 1 + delta_ratio * lambda_;
            } else {
                double delta_ratio = (cur_hit_ratio / ind_hit_ratio - 1);
                cur_half_ *= 1 + delta_ratio * lambda_;
            }
        }
        else {
            stable_count_++;
            if (stable_count_ == 5) {
                if (cur_half_ < ori_half_) {
                    cur_half_ *= 1 + 0.1;
                } else {
                    cur_half_ /= 1 + 0.1;
                }
                stable_count_ = 0;
            }
        }
    }
    if (cur_half_ < (double)1 / buffer_size_) {
        cur_half_  = (double)1 / buffer_size_;
    }
//    if (cur_half_ > 100) {
//        cur_half_  = 100;
//    }
    next_decay_ts_ = std::min(next_decay_ts_, (int)(ts_ + cur_half_ * buffer_size_));
    indicator->set_cur_half(cur_half_ / (1 + delta_ratio_));
    interval_hit_count_ = 0;
    indicator->hit_count = 0;
    indicator->mis_count = 0;
    return RC::SUCCESS;
}

RC GhostALRFUIndicator::decay() {
    for (int i = 1; i < count_level_; i++) {
        if (real_lru_[i].size() == 0) {
            continue;
        }
        real_lru_[i / 2].splice(real_lru_[i / 2].begin(), real_lru_[i]);
        if (real_lru_[i / 2].size()) {
            min_level_non_empty = std::min(min_level_non_empty, i / 2);
        }
        ghost_lru_[i / 2].splice(ghost_lru_[i / 2].begin(), ghost_lru_[i]);
    }
    next_decay_ts_ = ts_ + cur_half_ * buffer_size_;
    prev_decay_ts_ = ts_;
    decay_ts.push_back(ts_);
    if (decay_ts.size() > count_level_bits) {
        decay_ts.pop_front();
    }
    return RC::SUCCESS;
}

int GhostALRFUIndicator::get_cur_level(const iter_status & status) {
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

RC GhostALRFUIndicator::get(const Key &key) {
    int inserted_level = start_level_;
    if (real_map_.count(key) == 0) {
        // miss
        mis_count++;
        if (real_map_.size() == buffer_size_) {
            // evict key in real
            Key evict_key = real_lru_[min_level_non_empty].back();
            real_lru_[min_level_non_empty].pop_back();
            real_map_.erase(evict_key);
            // move to ghost
            if (min_level_non_empty != 0) {
                // move to ghost

                ghost_lru_[min_level_non_empty].push_front(evict_key);
                ghost_map_[evict_key] = iter_status(ghost_lru_[min_level_non_empty].begin(), min_level_non_empty, ts_);
                // std::make_pair(ghost_lru_[min_level_non_empty].begin(), min_level_non_empty);
            }
            while (real_lru_[min_level_non_empty].size() == 0) {
                min_level_non_empty++;
            }
        }
        if (ghost_map_.count(key) != 0) {
            // use level in ghost
            std::list<Key>::iterator hit_iter = ghost_map_[key].iter;

            int level = get_cur_level(ghost_map_[key]);
            // erase key in ghost
            ghost_lru_[level].erase(hit_iter);
            ghost_map_.erase(key);
            inserted_level = level + start_level_;
        }
    } else {
        // hit
        hit_count++;
        std::list<Key>::iterator hit_iter = real_map_[key].iter;
        int level = get_cur_level(real_map_[key]); // real_map_[key].second;
        // erase key in real, use level in real
        real_lru_[level].erase(hit_iter);
        real_map_.erase(key);
        inserted_level = level + start_level_;
        while(real_lru_[min_level_non_empty].size() == 0) {
            min_level_non_empty++;
        }
    }
    inserted_level = std::min(inserted_level, count_level_ - 1);
    real_lru_[inserted_level].push_front(key);
    real_map_[key] = iter_status(real_lru_[inserted_level].begin(), inserted_level, ts_);
    if (inserted_level < min_level_non_empty) {
        min_level_non_empty = inserted_level;
    }
    ts_++;
    if (ts_ == next_decay_ts_) {
        decay();
    }
    return RC::SUCCESS;
}