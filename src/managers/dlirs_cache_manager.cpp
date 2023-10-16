//
// Created by Clouds on 2023/9/20.
//
//#define LOG
#include "dlirs_cache_manager.h"

RC DLIRSCacheManager::get(const Key &key) {
    time++;
#ifdef LOG
    if (time % 20000 == 0) {
        std::cout << statics() << '\n';
    }
#endif
    bool miss = false;
    if (lirs.Contain(key)) {
        auto x = lirs.Get(key);
        if (x.is_lir) {
            hitLIR(key);
        } else {
            miss = hitHIRinLIRS(key);
        }
    } else if (q.Contain(key)) {
        hitHIRinQ(key);
    } else {
        miss = true;
        Miss(key);
    }
    if (miss) {
        increase_miss_count();
    } else {
        increase_hit_count();
    }
    return RC::SUCCESS;
}

RC DLIRSCacheManager::put(const Key &key, const Value &value) { return RC::UNIMPLEMENT; }

std::string DLIRSCacheManager::get_name() {
    return {"DLIRS"};
}