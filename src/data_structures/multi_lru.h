////
//// Created by MorphLing on 2023/3/13.
////
//
//#ifndef CACHE_PERFORMANCE_INSIGHT_MULTI_LRU_H
//#define CACHE_PERFORMANCE_INSIGHT_MULTI_LRU_H
//
//#include "def.h"
//#include "data_structures/lru_list.h"
//
//struct MLRUNode : public LinkNode<Key> {
//public:
//    MLRUNode(Key key, int insert_ts, int insert_level) : LinkNode<Key>(key) {
//        this->insert_ts = insert_ts;
//        this->insert_level = insert_level;
//    }
//    int level_for_header = -1;
//    int insert_ts, insert_level;
//};
//
//class DecayMultiLRUList {
//public:
//    DecayMultiLRUList(int count_level_bits, int decay_interval) : count_level(1 << count_level_bits) {
//        lru_.resize(count_level);
//        headers_.resize(count_level);
//        // decay_ts_records.reserve(count_level_bits);
//        min_level_non_empty = INT32_MAX;
//        next_decay_ts = decay_interval;
//        this->count_level_bits = count_level_bits;
//    }
//    void Push(Key key, int level);
//    void Erase(Key key);
//    int GetEstLevel(Key key);
//    Key Pop(int *level= nullptr);
//    void Decay();
//    bool Exists(Key key) { return mapper_.count(key) > 0;}
//    int Size() { return mapper_.size(); }
//private:
//    std::vector<LinkList<Key> > lru_;
//    std::vector<MLRUNode*> headers_;
//    std::unordered_map<Key, MLRUNode*> mapper_;
//    int min_level_non_empty, count_level, decay_interval, next_decay_ts, last_decay_ts, count_level_bits;
//    std::list<int> decay_ts_records;
//};
//
//
//#endif //CACHE_PERFORMANCE_INSIGHT_MULTI_LRU_H
