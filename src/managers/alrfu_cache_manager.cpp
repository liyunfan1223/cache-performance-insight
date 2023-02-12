////
//// Created by MorphLing on 2023/2/7.
////
//
#include "alrfu_cache_manager.h"

RC ALRFUCacheManager::get(const Key &key) {
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
//        access_status_.push_back(0);
    }
//    if (access_status_.size() >= update_interval_) {
//        if (access_status_.front() == 1) {
//            interval_hit_count_--;
//        } else {
//            interval_miss_count_--;
//        }
//        access_status_.pop_front();
//    }

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
//    if (indicate_status_.size() >= update_interval_) {
//        if (indicate_status_.front() == 1) {
//            indicate_hit_count_--;
//        } else {
//            indicate_miss_count_--;
//        }
//        indicate_status_.pop_front();
//    }

//    if (indicate_dd_heap2_.InHeap(key)) {
//        // hit_count_++;
//        indicate_hit_count2_++;
//    } else {
//        // miss_count_++;
//        indicate_miss_count2_++;
//        if (indicate_dd_heap2_.Size() == buffer_size_) {
//            indicate_dd_heap2_.Pop();
//        }
//    }

    store_heap_.Add(key, 1, cur_decay_ratio_exp_);
    indicate_store_heap_.Add(key, 1, cur_decay_ratio_exp_ * (1 + delta_ratio_));
//    indicate_store_heap2_.Add(key, 1, cur_decay_ratio_exp_ * (1 - delta_ratio_));

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

//    if (indicate_dd_heap2_.InHeap(key)) {
//        indicate_dd_heap2_.Add(key, 1, cur_decay_ratio_exp_ * (1 - delta_ratio_));
//    } else {
//        indicate_dd_heap2_.Add(key, indicate_store_heap2_.GetValue(key), cur_decay_ratio_exp_ * (1 - delta_ratio_));
//    }

    if (interval_count_ % update_interval_ == 0) {
        update_cur_decay_ratio();
    }
    return RC::SUCCESS;
}

RC ALRFUCacheManager::put(const Key &key, const Value &value) {
    return RC::DEFAULT;
}

std::string ALRFUCacheManager::get_name() {
    return "ALRFU";
}

std::string ALRFUCacheManager::get_configuration() {
    return CacheManager::get_configuration();
}

RC ALRFUCacheManager::check_consistency() {
    return CacheManager::check_consistency();
}

void ALRFUCacheManager::lazy_update_score(Key key) {
}

void ALRFUCacheManager::update_cur_decay_ratio() {
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
//    indicate_hit_count2_ = 0;
//    indicate_miss_count2_ = 0;
    interval_count_ = 0;
    dd_heap_.deep_copy(indicate_dd_heap_);
    store_heap_.deep_copy(indicate_store_heap_);

//    debug_counter++;
//    if (debug_counter % update_interval_ == 0)
//    printf("%.4f %.4f %.10f %.4f\n", ind_hit_ratio, cur_hit_ratio, (double)cur_half_, (double)hit_count_ / (hit_count_ + miss_count_));
}

void ALRFUCacheManager::maintain(DDHeap &heap, Key key) {

}