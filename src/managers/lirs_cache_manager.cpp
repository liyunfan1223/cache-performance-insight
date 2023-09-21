//
// Created by Clouds on 2023/9/20.
//

#include "lirs_cache_manager.h"

RC LIRSCacheManager::get(const Key &key) {
    if (map_.find(key) != map_.end()) { // find it
        hit_count();
        auto pnode = map_[key];
        if (!IS_VALID(pnode->value)) {
            ++ used_size_;
        }
        Get(key);

        return RC::SUCCESS;
    }
    miss_count();
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
    }
    return RC::SUCCESS;
}

RC LIRSCacheManager::put(const Key &key, const Value &value) { return RC::UNIMPLEMENT; }

std::string LIRSCacheManager::get_name() {
    return {"LIRS"};
}