//
// Created by MorphLing on 2022/9/28.
//

#pragma once

#include "def.h"
#include <memory>
#include <sstream>
#include <string>

class CacheManager {
public:
    CacheManager(int32_t buffer_size): buffer_size_(buffer_size)
    {
        hit_count_ = 0;
        miss_count_ = 0;
    }

    virtual ~CacheManager()
    {
    }

    std::string statics()
    {
        std::stringstream s;
        s << get_name() << ": "
          <<" buffer_size:" << buffer_size_
          << " hit_count:" <<  hit_count_
          << " miss_count:" << miss_count_
          << " hit_rate:" << float(hit_count_) / (hit_count_ + miss_count_) * 100 << "\%"
          << std::endl;
        return s.str();
    }

    virtual RC get(const Key & key) = 0;
    virtual RC put(const Key & key, const Value &value) = 0;
    virtual std::string get_name() = 0;
    int32_t hit_count() const { return hit_count_; }
    int32_t miss_count() const { return miss_count_; }

protected:
    int32_t buffer_size_;
    int32_t hit_count_;
    int32_t miss_count_;
};

