//
// Created by MorphLing on 2023/2/12.
//
//#define LOG
#include "alrfu2_cache_manager.h"
RC ALRFU2CacheManager::get(const Key &key) {
    interval_count_++;

    if (dd_heap_.InHeap(key)) {
        hit_count_++;
        interval_hit_count_++;
//        access_status_.push_back(1);
    } else {
        miss_count_++;
        interval_miss_count_++;
        if (dd_heap_.Size() == buffer_size_) {
            dd_heap_.Pop();
        }
    }

    if (indicate_dd_heap_.InHeap(key)) {
        // hit_count_++;
        indicate_hit_count_++;
        indicate_status_.push_back(1);
    } else {
        // miss_count_++;
        indicate_miss_count_++;
        if (indicate_dd_heap_.Size() == buffer_size_) {
            indicate_dd_heap_.Pop();
        }
        indicate_status_.push_back(0);
    }

    store_heap_.Add(key, 1, cur_decay_ratio_exp_);
    indicate_store_heap_.Add(key, 1, cur_decay_ratio_exp_ * (1 + delta_ratio_));

    if (dd_heap_.InHeap(key)) {
        dd_heap_.Add(key, 1, cur_decay_ratio_exp_);
    } else {
        dd_heap_.Add(key, store_heap_.GetValue(key), cur_decay_ratio_exp_);
    }

    if (indicate_dd_heap_.InHeap(key)) {
        indicate_dd_heap_.Add(key, 1, cur_decay_ratio_exp_ * (1 + delta_ratio_));
    } else {
        indicate_dd_heap_.Add(key, indicate_store_heap_.GetValue(key), cur_decay_ratio_exp_ * (1 + delta_ratio_));
    }

    if (interval_count_ % update_interval_ == 0) {
        update_cur_decay_ratio();
    }
    return RC::SUCCESS;
}

RC ALRFU2CacheManager::put(const Key &key, const Value &value) {
    return RC::DEFAULT;
}

std::string ALRFU2CacheManager::get_name() {
    return "ALRFU2";
}

std::string ALRFU2CacheManager::get_configuration() {
    return CacheManager::get_configuration();
}

RC ALRFU2CacheManager::check_consistency() {
    return CacheManager::check_consistency();
}

void ALRFU2CacheManager::lazy_update_score(Key key) {
}

void ALRFU2CacheManager::update_cur_decay_ratio() {
    double cur_hit_ratio = (double)interval_hit_count_ / update_interval_;
    double ind_hit_ratio = (double)indicate_hit_count_ / update_interval_;
//    double ind_hit_ratio2 = (double)indicate_hit_count2_ / update_interval_;
    if (cur_hit_ratio != 0 && ind_hit_ratio != 0 && fabs(ind_hit_ratio - cur_hit_ratio) >= EPSILON) {
        if (ind_hit_ratio > cur_hit_ratio) {
            double delta_ratio = ind_hit_ratio / cur_hit_ratio - 1;
            cur_half_ /= 1 + delta_ratio * lambda_;
        } else {
            double delta_ratio = cur_hit_ratio / ind_hit_ratio - 1;
            cur_half_ *= 1 + delta_ratio * lambda_;
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
    printf("%.4f %.4f %.10f %.4f\n", ind_hit_ratio, cur_hit_ratio, (double)cur_half_, (double)hit_count_ / (hit_count_ + miss_count_));
#endif
}

void ALRFU2CacheManager::maintain(DDHeap &heap, Key key) {

}