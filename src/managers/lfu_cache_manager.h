//
// Created by l50029536 on 2022/9/29.
//

#pragma once

#include <set>
#include <unordered_map>
#include "managers/cache_manager.h"


class LFUCacheManager: public CacheManager {
public:
    LFUCacheManager(int32_t buffer_size): CacheManager(buffer_size)
    {}

    ~LFUCacheManager()
    {}
    RC get(const Key & key) override;
    RC put(const Key & key, const Value & value) override;
    std::string get_name() override;
private:
    struct Status {
        Status(int32_t freq, int32_t timestamp, Key key)
                : freq(freq), timestamp(timestamp), key(key) {}
        int32_t freq;
        int32_t timestamp;
        Key key;
        bool operator < (const Status & rhs) const {
            if (freq != rhs.freq) {
                return freq < rhs.freq;
            } else if (timestamp != rhs.timestamp) return timestamp < rhs.timestamp;
            return key < rhs.key;
        }
    };
    std::set<Status> buffer_set_;
    std::unordered_map<Key, std::set<Status>::iterator> u_map_;
    int32_t timestamp_ = 0;
};
