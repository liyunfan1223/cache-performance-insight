//
// Created by MorphLing on 2022/10/25.
//

#pragma once

#include "managers/cache_manager.h"

class MRFCacheManager: public CacheManager {
public:
    MRFCacheManager(int32_t buffer_size, std::vector<Key> & access_list)
    : CacheManager(buffer_size), access_list_(access_list)
    {
        for (auto key : access_list_) {
            priorKeyFreq_[key]++;
        }
    }

    ~MRFCacheManager()
    {}
    RC get(const Key & key) override;
    RC put(const Key & key, const Value & value) override;
    std::string get_name() override;
    RC check_consistency() override;
private:
    struct Status {
        Status(int32_t residual_frequency, Key key)
                : residual_frequency(residual_frequency), key(key) {}
        int32_t residual_frequency;
        Key key;
        bool operator < (const Status & rhs) const {
            if (residual_frequency != rhs.residual_frequency) {
                return residual_frequency < rhs.residual_frequency;
            }
            return key < rhs.key;
        }
    };
    int32_t reserve_space_;
    std::vector<Key> & access_list_;
    std::unordered_map<Key, int32_t> priorKeyFreq_;
    std::unordered_map<Key, std::set<Status>::iterator> u_map_;
    std::set<Status> buffer_set_;
};

