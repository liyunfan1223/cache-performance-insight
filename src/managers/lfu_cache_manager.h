//
// Created by l50029536 on 2022/9/29.
//

#pragma once

#include <set>
#include <unordered_map>
#include "managers/cache_manager.h"

struct Status {
    Status(int32_t freq, int32_t timestamp, Key key)
    : freq(freq), timestamp(timestamp), key(key) {}
    int32_t freq;
    int32_t timestamp;
    Key key;
    bool operator < (const Status & rhs) const {
        return freq != rhs.freq ?
            freq < rhs.freq :
            timestamp < rhs.timestamp;
    }
//    bool operator = (Status & rhs) const {
//        return 0;
//    }
//    bool operator >= (Status & rhs) const {
//        return 0;
//    }
};

class LFUCacheManager: public CacheManager {
public:
    LFUCacheManager(int32_t buffer_size): CacheManager(buffer_size)
    {
    }

    ~LFUCacheManager()
    {

    }
    RC get(const Key & key) override;
    RC put(const Key & key, const Value & value) override;
    std::string get_name() override;
private:
    std::set<Status> set_;
    std::unordered_map<Key, std::set<Status>::iterator> u_map_;
    int32_t timestamp_ = 0;
};
