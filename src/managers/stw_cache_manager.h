//
// Created by MorphLing on 2023/1/4.
//

#pragma once

#include "managers/cache_manager.h"

class STWCacheManager : public CacheManager {
public:
    explicit STWCacheManager(int32_t buffer_size, float window_size_ratio_to_buffer_ = 20)
    : CacheManager(buffer_size) {
        window_size_ = buffer_size * window_size_ratio_to_buffer_;
    }

    ~STWCacheManager() override = default;
    RC get(const Key & key) override;
    RC put(const Key & key, const Value & value) override;
    std::string get_name() override;
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
    std::unordered_map<Key, int32_t> short_term_freq_, long_term_freq_;
    std::list<Key> access_window_;
    int32_t window_size_;
    std::set<Status> buffer_set_;
    std::unordered_map<Key, std::set<Status>::iterator> u_map_;
    int32_t timestamp_ = 0;
};