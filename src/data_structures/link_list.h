//
// Created by MorphLing on 2022/9/28.
//

#pragma once

#include <def.h>

struct LinkNode;
class LinkList;

struct LinkNode {
    LinkNode(){}
    LinkNode(Key key): key(key) {}
    LinkNode(Key key, LinkList * belong): key(key), belong(belong) {}
    LinkList * belong = nullptr;
    LinkNode * pred = nullptr;
    LinkNode * next = nullptr;
    Key key;
    Value value;
};

class LinkList {
public:
    LinkList(){}
    ~LinkList();
    RC push_front(Key key);
    RC pop_back();
    RC remove(LinkNode * node);

    LinkNode * head = nullptr;
    LinkNode * tail = nullptr;
    int32_t size = 0;
};

