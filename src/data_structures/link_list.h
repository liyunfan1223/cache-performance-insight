//
// Created by MorphLing on 2022/9/28.
//

#pragma once

#include <def.h>

struct LinkNode {
    LinkNode(){}
    LinkNode(Key key): key(key)
    {}
//    LinkNode(Key key, Value value): key(key), value(value)
//    {}
    LinkNode * pred = nullptr;
    LinkNode * next = nullptr;
    Key key;
    Value value;
};

class LinkList {
public:
    LinkList(){}
    ~LinkList();
    RC PushFront(Key key);
//    RC PushFront(Key key, Value value);
    RC PopBack();
    RC Remove(LinkNode * node);

    LinkNode * head = nullptr;
    LinkNode * tail = nullptr;
    int32_t size = 0;
};

