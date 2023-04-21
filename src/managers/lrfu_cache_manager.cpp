//
// Created by MorphLing on 2023/2/9.
//

#include "lrfu_cache_manager.h"

RC LRFUCacheManager::get(const Key &key) {
    if (lu_heap_.InHeap(key)) {
        hit_count_++;
    } else {
        miss_count_++;
        if (lu_heap_.Size() == buffer_size_) {
            lu_heap_.Pop();
        }
    }
//    lu_heap_.Add(key, 1);
    lu_heap_store_.Add(key, 1);
    if (lu_heap_.InHeap(key)) {
        lu_heap_.Add(key, 1);
    } else {
        lu_heap_.Add(key, lu_heap_store_.GetValue(key));
    }
//    lu_heap_.Add(key, 1);
//     lu_heap_.Set(key, lu_heap_store_.GetValue(key));
    return RC::SUCCESS;
}

RC LRFUCacheManager::put(const Key &key, const Value &value) {
    return RC::UNIMPLEMENT;
}

std::string LRFUCacheManager::get_name() {
    return "LRFU";
}
