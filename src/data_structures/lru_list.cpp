//
// Created by MorphLing on 2022/10/5.
//

#include "lru_list.h"

RC LRUList::push_front(Key key) {
    LinkList::push_front(key);
    u_map[key] = LinkList::head;
     assert(u_map.size() == LinkList::size);
    return RC::SUCCESS;
}

Key LRUList::pop_back() {
    LinkNode * old_tail = tail;
    Key key = old_tail->key;
    u_map.erase(key);
    LinkList::pop_back();
    assert(u_map.size() == LinkList::size);
    return key;
}

RC LRUList::remove(const Key &key) {
    LinkList::remove(u_map.at(key));
    u_map.erase(key);
     assert(u_map.size() == LinkList::size);
    return RC::SUCCESS;
}

int32_t LRUList::count(const Key & key) {
    return u_map.count(key);
}

int32_t LRUList::size() {
    return LinkList::size;
}