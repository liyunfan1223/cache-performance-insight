//
// Created by MorphLing on 2022/10/5.
//

#pragma once

#include "data_structures/link_list.h"
#include <unordered_map>

template<typename T>
class LRUList : public LinkList<T> {
public:
    RC push_front(Key key);
    RC pop_back();
    RC pop_back(Key & key);
    RC remove(const Key & key);
    int32_t count(const Key & key);
    int32_t size();
    std::unordered_map<Key, LinkNode<T> *> u_map;
};