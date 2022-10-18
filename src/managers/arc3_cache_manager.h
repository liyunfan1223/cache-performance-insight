//
// Created by l50029536 on 2022/10/13.
//

#pragma once

#include "managers/cache_manager.h"
#include "data_structures/link_list.h"
#include "data_structures/lru_list.h"


class ARC3CacheManager: public CacheManager {
public:
    ARC3CacheManager(int32_t buffer_size, int32_t reserve_space, std::vector<Key> & access_list)
    : CacheManager(buffer_size), access_list_(access_list), reserve_space_(reserve_space)
    {
        left_space_ = buffer_size_ - reserve_space_;
        p_ = 0;
        for (auto key : access_list_) {
            priorKeyFreq_[key]++;
        }
        std::vector<std::pair<int32_t, Key>> vec;
        for (auto pik : priorKeyFreq_) {
            vec.push_back(std::make_pair(pik.second, pik.first));
        }
        std::sort(vec.begin(), vec.end());
        std::reverse(vec.begin(), vec.end());
        for (int32_t i = 0; i < std::min(reserve_space_, (int32_t)vec.size()); i++) {
            hiFreqKey_.insert(vec[i].second);
        }
    }

    ~ARC3CacheManager()
    {}
    RC get(const Key & key) override;
    RC put(const Key & key, const Value & value) override;
    std::string get_name() override;
    RC check_consistency() override;
private:
    RC replace_(const Key & key);
    int32_t reserve_space_, left_space_;
    std::vector<Key> & access_list_;
    std::unordered_map<Key, int32_t> priorKeyFreq_;
    std::unordered_set<Key> hiFreqKey_, hiFreqSet_;
    LRUList<Key> lruList_t1_, lruList_t2_, lruList_b1_, lruList_b2_;
    double p_;
};