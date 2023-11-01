//
// Created by MorphLing on 2023/5/23.
//

#include "rgc5_cache_manager.h"

RC RGC5CacheManager::get(const Key &key) {
    ts_++;
    if (replacer_r_.Access(key)) {
        increase_hit_count();
        hit_recorder.push_back(1);
        recorder_hit_count++;
    } else {
        increase_miss_count();
        hit_recorder.push_back(0);
    }

    if (hit_recorder.size() >= 500000) {
        if (hit_recorder.front() == 1) {
            recorder_hit_count--;
        }
        hit_recorder.pop_front();
    }

    replacer_s_.Access(key);
    if (ts_ % update_interval_ == 0) {
        int32_t r_mc, r_hc;
        int32_t s_mc, s_hc;
        replacer_r_.Report(r_mc, r_hc);
        replacer_s_.Report(s_mc, s_hc);
        double r_hr = (double) r_hc / (r_mc + r_hc);
        double s_hr = (double) s_hc / (s_mc + s_hc);
        double cur_half = replacer_r_.GetCurHalf();
        if (r_hr != 0 && s_hr != 0) {
            if (fabs(s_hr - r_hr) >= EPSILON) {
                stable_count_ = 0;
                if (s_hr > r_hr) {
                    double delta_ratio = (s_hr / r_hr - 1);
                    if (delta_ratio > delta_bound_) {
                        delta_ratio = delta_bound_;
                    }
                    replacer_r_.UpdateHalf(cur_half / (1 + delta_ratio * lambda_));
                } else {
                    double delta_ratio = (r_hr / s_hr - 1);
                    if (delta_ratio > delta_bound_) {
                        delta_ratio = delta_bound_;
                    }
                    replacer_r_.UpdateHalf(cur_half * (1 + delta_ratio * lambda_));
                }
            } else {
                stable_count_++;
                if (stable_count_ == 5) {
                    double delta_ratio = 0.1;
                    if (delta_ratio > delta_bound_) {
                        delta_ratio = delta_bound_;
                    }
                    if (cur_half < init_half_) {
                        replacer_r_.UpdateHalf(cur_half * (1 + delta_ratio * lambda_));
                    } else {
                        replacer_r_.UpdateHalf(cur_half / (1 + delta_ratio * lambda_));
                    }
                    stable_count_ = 0;
                }
            }
        }
        replacer_s_.UpdateHalf(replacer_r_.GetCurHalf() / (1 + simulator_ratio_));
//#ifdef LOG
//        report_ct++;
//        printf("ct: %d reality: %.2f simulator: %.2f r_cur_half: %.8f %d %d\n", report_ct, r_hr * 100, s_hr * 100, replacer_r_.GetCurHalf(), replacer_r_.h1, replacer_r_.h2);
////        std::cout << statics() << '\n';
//#endif
    }
#ifdef LOG
    if (ts_ % 100 == 0) {
        report_ct++;
        printf("ct: %d reality: %.8f simulator: %.8f r_cur_half: %.8f %d %d\n",
               report_ct,
               ((double) recorder_hit_count / hit_recorder.size()),
               (double)0, replacer_r_.GetCurHalf(), replacer_r_.h1, replacer_r_.h2);
    }
#endif

    return RC::SUCCESS;
}

RC RGC5CacheManager::put(const Key &key, const Value &value) {
    return RC::UNIMPLEMENT;
}

std::string RGC5CacheManager::get_name() {
    return {"RGC5"};
}
