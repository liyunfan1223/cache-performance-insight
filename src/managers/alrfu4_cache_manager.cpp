//
// Created by MorphLing on 2023/2/13.
//
//#define LOG
#include "alrfu4_cache_manager.h"

RC ALRFU4CacheManager::get(const Key &key) {
    interval_count_++;
    double cur_score = 0;
    double indicate_score = 0;
    if (dd_heap_.InHeap(key)) {
        cur_score = score_hit_;
        hit_count_++;
        interval_hit_count_++;
//        access_status_.push_back(1);
    } else {
        cur_score = score_miss_;
        miss_count_++;
        interval_miss_count_++;
        if (dd_heap_.Size() == buffer_size_) {
            dd_heap_.Pop();
        }
    }

    if (indicate_dd_heap_.InHeap(key)) {
        indicate_score = score_hit_;
        indicate_hit_count_++;
    } else {
        indicate_score = score_miss_;
        indicate_miss_count_++;
        if (indicate_dd_heap_.Size() == buffer_size_) {
            indicate_dd_heap_.Pop();
        }
    }

    if (store_ratio_ > 0 && store_lru_.Size() >= store_ratio_ * buffer_size_) {
        store_lru_.Pop();
    }
    if (store_ratio_ > 0 && indicate_lru_.Size() >= store_ratio_ * buffer_size_) {
        indicate_lru_.Pop();
    }
    store_lru_.Add(key, cur_score, cur_decay_ratio_exp_);
    indicate_lru_.Add(key, indicate_score, cur_decay_ratio_exp_ * (1 + delta_ratio_));

    if (dd_heap_.InHeap(key)) {
        dd_heap_.Add(key, cur_score, cur_decay_ratio_exp_);
    } else {
        dd_heap_.Add(key, store_lru_.GetValue(key), cur_decay_ratio_exp_);
    }

    if (indicate_dd_heap_.InHeap(key)) {
        indicate_dd_heap_.Add(key, indicate_score, cur_decay_ratio_exp_ * (1 + delta_ratio_));
    } else {
        indicate_dd_heap_.Add(key, indicate_lru_.GetValue(key), cur_decay_ratio_exp_ * (1 + delta_ratio_));
    }

    if (interval_count_ % update_interval_ == 0) {
        update_cur_decay_ratio();
    }
    return RC::SUCCESS;
}

RC ALRFU4CacheManager::put(const Key &key, const Value &value) {
    return RC::DEFAULT;
}

std::string ALRFU4CacheManager::get_name() {
    return "ALRFU4";
}

std::string ALRFU4CacheManager::get_configuration() {
    return CacheManager::get_configuration();
}

RC ALRFU4CacheManager::check_consistency() {
    return CacheManager::check_consistency();
}

void ALRFU4CacheManager::update_cur_decay_ratio() {
    double cur_hit_ratio = (double)interval_hit_count_ / update_interval_;
    double ind_hit_ratio = (double)indicate_hit_count_ / update_interval_;
//    double ind_hit_ratio2 = (double)indicate_hit_count2_ / update_interval_;
    if (cur_hit_ratio != 0 && ind_hit_ratio != 0) {
        if (fabs(ind_hit_ratio - cur_hit_ratio) >= EPSILON) {
            stable_count_ = 0;
            if (ind_hit_ratio > cur_hit_ratio) {
                double delta_ratio = ind_hit_ratio / cur_hit_ratio - 1;
                cur_half_ /= 1 + delta_ratio * lambda_;
            } else {
                double delta_ratio = cur_hit_ratio / ind_hit_ratio - 1;
                cur_half_ *= 1 + delta_ratio * lambda_;
            }
        }
        else {
            stable_count_++;
            if (stable_count_ == 5) {
                if (cur_half_ < ori_half_) {
                    cur_half_ *= 1 + delta_ratio_;
                } else {
                    cur_half_ /= 1 + delta_ratio_;
                }
                stable_count_ = 0;
            }
        }
    }
    if (cur_half_ < (double)1 / buffer_size_) {
        cur_half_  = (double)1 / buffer_size_;
    }
    cur_decay_ratio_exp_ = log(0.5) / (cur_half_ * buffer_size_);
    interval_hit_count_ = 0;
    interval_miss_count_ = 0;
    indicate_hit_count_ = 0;
    indicate_miss_count_ = 0;
    interval_count_ = 0;
#ifdef LOG
    printf("%.10f %.10f %.10f %.2f\n", ind_hit_ratio, cur_hit_ratio, (double)cur_half_, (double)hit_count_ / (hit_count_ + miss_count_) * 100);
#endif
}