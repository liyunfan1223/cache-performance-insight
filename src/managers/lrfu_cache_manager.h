//
// Created by MorphLing on 2023/2/9.
//

#pragma once

#include "managers/cache_manager.h"
#include "data_structures/lazy_update_heap.h"

class LRFUCacheManager: public CacheManager {
public:
    LRFUCacheManager(int32_t buffer_size,
                     double lambda = 1e-4) : CacheManager(buffer_size),
                                             lu_heap_(pow(0.5, lambda)),
                                             lu_heap_store_(pow(0.5, lambda))
    {
        lambda_ = lambda;
    }

    RC get(const Key &key) override;

    RC put(const Key &key, const Value &value) override;

    std::string get_name() override;

private:
    LUHeap lu_heap_;
    LUHeap lu_heap_store_;
//    struct Status {
//        Status(double score, Key key, int32_t timestamp)
//                : score(score), key(key), timestamp(timestamp) {}
//        double score;
//        int32_t timestamp;
//        Key key;
//        bool operator < (const Status & rhs) const {
//            if (fabs(score - rhs.score) > EPSILON) {
//                return score < rhs.score;
//            } else if (timestamp != rhs.timestamp) return timestamp < rhs.timestamp;
//            return key < rhs.key;
//        }
//    };
//    double pow2(double p) {
//        return pow(0.5, p);
//    }
//    std::unordered_map<Key, double> score_;
//    std::unordered_map<Key, int32_t> last_calc_ts_;
//    std::set<Status> buffer_set_;
//    std::unordered_map<Key, std::set<Status>::iterator> u_map_;
//    int32_t ts_ = 0;
    double lambda_;
};
