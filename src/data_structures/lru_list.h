//
// Created by MorphLing on 2022/10/5.
//

#pragma once

#include "data_structures/link_list.h"
#include <unordered_map>

class LRUList : public LinkList {
public:
    RC push_front(Key key);
//    RC push_front(Key key, Value value);
    Key pop_back();
    RC remove(const Key & key);
    int32_t count(const Key & key);
    int32_t size();
    std::unordered_map<Key, LinkNode *> u_map;
};