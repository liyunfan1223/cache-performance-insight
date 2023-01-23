//
// Created by MorphLing on 2022/10/9.
//

#pragma once

#include "managers/cache_manager.h"
#include "data_structures/link_list.h"

class OPTCacheManager: public CacheManager {
public:
    explicit OPTCacheManager(int32_t bufferSize, std::vector<Key> & access_list)
    : CacheManager(bufferSize), access_list_(access_list)
    {
        int timeStamp = 0;
        for (auto key : access_list_) {
            key_access_u_map_[key].push_back(timeStamp++);
        }
    }
    ~OPTCacheManager(){}
    RC get(const Key &key) override;
    RC put(const Key &key, const Value &value) override;
    std::string get_name() override;
    RC check_consistency() override;

private:
    struct Status {
        Status(int32_t future_access_timestamp, Key key)
        : future_access_timestamp(future_access_timestamp), key(key) {}
        int32_t future_access_timestamp;
        Key key;
        bool operator < (const Status & rhs) const {
            return future_access_timestamp > rhs.future_access_timestamp;
        }
    };
    std::vector<Key> & access_list_;
    std::unordered_map<Key, LinkList<int32_t>> key_access_u_map_;
    std::unordered_map<Key, std::set<Status>::iterator> u_map_;
    std::set<Status> buffer_set_;
    int32_t timestamp_ = 0;
};

