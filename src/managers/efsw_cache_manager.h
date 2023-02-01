//
// Created by Clouds on 2023/1/20.
//

#pragma once

#include "cache_manager.h"

class EFSWCacheManager: public CacheManager {
public:
    EFSWCacheManager(int32_t buffer_size,
                     double half_life_ratio = 1.0,
//                     int32_t window_size = 5,
                     double miss_score = 1,
                     double hit_score = 10):
        CacheManager(buffer_size)
    {
        exponential_decay_ratio_ = -log(0.5) / (half_life_ratio * (buffer_size));
        half_life_ratio_ = half_life_ratio;
        miss_score_ = miss_score;
        hit_score_ = hit_score;
    }

    ~EFSWCacheManager() override = default;

    RC get(const Key &key) override;

    RC put(const Key &key, const Value &value) override;

    std::string get_name() override;

    std::string get_configuration() override;

    RC check_consistency() override;

private:
    struct Status {
        Status(int32_t frequency, Key key, int32_t timestamp)
                : frequency(frequency), key(key), timestamp(timestamp) {}
        int32_t frequency, timestamp;
        Key key;
        bool operator < (const Status & rhs) const {
            if (frequency != rhs.frequency) {
                return frequency < rhs.frequency;
            } else if (timestamp != rhs.timestamp) return timestamp < rhs.timestamp;
            return key < rhs.key;
        }
    };
    std::unordered_map<Key, double> score_;
    std::unordered_map<Key, int32_t> last_access_;
    std::list<Key> access_window_;
//    int32_t window_size_;
    std::set<Status> buffer_set_;
    std::unordered_map<Key, std::set<Status>::iterator> u_map_;
    int32_t timestamp_ = 0;
    float exponential_decay_ratio_;
    double miss_score_, hit_score_, half_life_ratio_;
};
