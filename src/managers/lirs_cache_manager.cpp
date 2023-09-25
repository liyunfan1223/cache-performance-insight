//
// Created by Clouds on 2023/9/20.
//
//#define LOG
#include "lirs_cache_manager.h"

RC LIRSCacheManager::get(const Key &key) {
    tot++;
#ifdef LOG
    if (tot % 20000 == 0) {
        std::cout << statics() << '\n';
        std::cout << used_size_ << '\n';
        printf("%d %d %d %d %ld\n", tot, c_lir, c_hir_s, c_hir_ns, s_.size());
    }
#endif
    if (map_.find(key) != map_.end()) { // find it
//        increase_hit_count();
        auto pnode = map_[key];
        if (!IS_VALID(pnode->value)) {
            ++ used_size_;
        }
        Get(key);

        return RC::SUCCESS;
    }
    increase_miss_count();
    if (used_size_ >= cache_size_ || q_.size() >= q_size_) { // 清理
        FreeOne();
    }

    // S is not FULL, so just input it as LIR
    lirs_node *p = new lirs_node(key, 0, s_.end(), q_.end());
    assert(p);
    Push(p, true);
    ++ used_size_;

    // S is FULL, so just input it as HIR
    if (used_size_ > s_size_) {
        //if (s_.size() > s_size_) {
        p->type = HIR;
        Push(p, false);

        hirs_.push_front(p);
        p->hirs = hirs_.begin();
    }
    return RC::SUCCESS;
}

RC LIRSCacheManager::put(const Key &key, const Value &value) { return RC::UNIMPLEMENT; }

std::string LIRSCacheManager::get_name() {
    return {"LIRS"};
}