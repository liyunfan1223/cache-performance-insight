//
// Created by MorphLing on 2022/10/9.
//

#pragma once

#include "managers/cache_manager.h"
#include "data_structures/link_list.h"
#include "data_structures/lru_list.h"


class ARC2CacheManager: public CacheManager{
public:
    ARC2CacheManager(int32_t buffer_size, float hi_freq_scale, std::vector<Key> & access_list)
    : CacheManager(buffer_size), access_list_(access_list)
    {
        p_ = 0;
        for (auto key : access_list_) {
            priorKeyFreq_[key]++;
        }
        std::vector<std::pair<int32_t, Key>> vec;
        for (auto pik : priorKeyFreq_) {
            vec.push_back(std::make_pair(pik.second, pik.first));
        }
        std::sort(vec.begin(), vec.end());
        for (int32_t i = (int)(vec.size() * (1 - hi_freq_scale)); i < vec.size(); i++) {
            hiFreqKey_.insert(vec[i].second);
        }
    }

    ~ARC2CacheManager()
    {}
    RC get(const Key & key) override;
    RC put(const Key & key, const Value & value) override;
    std::string get_name() override;
    RC check_consistency() override;
private:
    RC replace_(const Key & key);
    std::vector<Key> & access_list_;
    std::unordered_map<Key, int32_t> priorKeyFreq_;
    std::unordered_set<Key> hiFreqKey_;
    LRUList<Key> lruList_t1_, lruList_t2_, lruList_b1_, lruList_b2_;
    double p_;
};