//
// Created by MorphLing on 2023/5/23.
//

#include "rgc_cache_manager.h"

RC RGCCacheManager::get(const Key &key) {
    ts_++;
    if (replacer_r_.Access(key)) {
        increase_hit_count();
    } else {
        increase_miss_count();
    }
    replacer_s_.Access(key);
    if (ts_ % update_interval_ == 0) {
        int32_t r_mc, r_hc;
        int32_t s_mc, s_hc;
        replacer_r_.ReportAndClear(r_mc, r_hc);
        replacer_s_.ReportAndClear(s_mc, s_hc);
        double r_hr = (double) r_hc / (r_mc + r_hc);
        double s_hr = (double) s_hc / (s_mc + s_hc);
        double cur_half = replacer_r_.GetCurHalf();
        if (r_hr != 0 && s_hr != 0) {
            if (fabs(s_hr - r_hr) >= EPSILON) {
                stable_count_ = 0;
                if (s_hr > r_hr) {
                    double delta_ratio = (s_hr / r_hr - 1);
                    replacer_r_.UpdateHalf(cur_half / (1 + delta_ratio * lambda_));
                } else {
                    double delta_ratio = (r_hr / s_hr - 1);
                    replacer_r_.UpdateHalf(cur_half * (1 + delta_ratio * lambda_));
                }
            } else {
                stable_count_++;
                if (stable_count_ == 5) {
                    if (cur_half < init_half_) {
                        replacer_r_.UpdateHalf(cur_half * (1.1));
                    } else {
                        replacer_r_.UpdateHalf(cur_half / (1.1));
                    }
                    stable_count_ = 0;
                }
            }
        }
        replacer_s_.UpdateHalf(replacer_r_.GetCurHalf() / (1 + simulator_ratio_));
        printf("reality: %.2f simulator: %.2f r_cur_half: %.8f\n", r_hr * 100, s_hr * 100, replacer_r_.GetCurHalf());
        std::cout << statics() << '\n';
    }
    return RC::SUCCESS;
}

RC RGCCacheManager::put(const Key &key, const Value &value) {
    return RC::UNIMPLEMENT;
}

std::string RGCCacheManager::get_name() {
    return {"RGC"};
}
