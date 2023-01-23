//
// Created by Clouds on 2023/1/12.
//

#pragma once

#include "cache_manager.h"

class DRRIPCacheManager: public CacheManager {
public:
    explicit DRRIPCacheManager(int32_t buffer_size, int m = 3)
    : CacheManager(buffer_size) {
            for (int i = 0; i < (1 << m); i++) {
                index_sets_.push_back(new std::set<Key>());
            }
            evict_bitmap_ = (1 << m) - 1;
    }

    ~DRRIPCacheManager() override {
        for (auto &index_set : index_sets_) {
            delete index_set;
        }
        index_sets_.clear();
    }
    RC get(const Key & key) override;
    RC put(const Key & key, const Value & value) override;
    std::string get_name() override;
    RC check_consistency() override;
    struct Status {
        Status(Key key): key(key) {
        }
        Key key;
        bool operator < (const Status &rhs) const {
            return key < rhs.key;
        }
    };
private:
    std::unordered_map<Key, std::set<Key>::iterator> u_map_;
    std::vector<std::set<Key> *> index_sets_;
    int32_t evict_bitmap_;
};

