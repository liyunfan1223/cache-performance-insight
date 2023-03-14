////
//// Created by MorphLing on 2023/3/13.
////
//
//#include "multi_lru.h"
//
//void DecayMultiLRUList::Push(Key key, int level) {
//    lru_[level].p
//}
//
//void DecayMultiLRUList::Erase(Key key) {
//
//}
//
//Key DecayMultiLRUList::Pop(int *level) {
//    return 0;
//}
//
//void DecayMultiLRUList::Decay() {
//
//}
//
//int DecayMultiLRUList::GetEstLevel(Key key) {
//    assert(mapper_.count(key));
//    int est_level = mapper_[key]->insert_level;
//    auto iter = decay_ts_records.begin();
//    for (int i = 0; i < decay_ts_records.size(); i++) {
//        if (mapper_[key]->insert_ts <= *iter) {
//            est_level >>= decay_ts_records.size() - i;
//            break;
//        }
//        iter++;
//    }
//    return est_level;
//}