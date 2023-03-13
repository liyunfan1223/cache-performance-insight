//
// Created by MorphLing on 2022/9/28.
//

#pragma once

#include "def.h"

class CacheManager {
public:
    explicit CacheManager(int32_t buffer_size): buffer_size_(buffer_size)
    {
        hit_count_ = 0;
        miss_count_ = 0;
        // is_count_started_ = false;
    }

    virtual ~CacheManager() = default;

    std::string statics()
    {
        std::stringstream s;
        s << get_name() << ":"
          <<" buffer_size:" << buffer_size_
          << " hit_count:" <<  hit_count_
          << " miss_count:" << miss_count_
          << " hit_rate:" << (float)hit_count_ / (float)(hit_count_ + miss_count_) * 100 << "\%"
          << std::endl;
        return s.str();
    }

    virtual RC get(const Key & key) = 0;
    virtual RC put(const Key & key, const Value &value) = 0;
    virtual std::string get_name() = 0;
    virtual std::string get_configuration() { return {""}; }
    virtual RC check_consistency() { return RC::DEFAULT; }
    int32_t hit_count() const { return hit_count_; }
    int32_t miss_count() const { return miss_count_; }
    int32_t increase_miss_count() { miss_count_ += 1; return miss_count_; }
    int32_t increase_hit_count() { hit_count_ += 1; return hit_count_; }
protected:
    const int32_t buffer_size_;
    int32_t hit_count_;
    int32_t miss_count_;
    // bool is_count_started_;
};

