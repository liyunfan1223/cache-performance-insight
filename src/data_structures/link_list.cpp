//
// Created by MorphLing on 2022/9/28.
//


#include "link_list.h"

LinkList::~LinkList()
{
    while (head != nullptr) {
        auto old = head;
        head = head->next;
        delete old;
    }
}

RC LinkList::push_front(Key key)
{
    LinkNode * new_node = new LinkNode(key);
    if (head != nullptr) {
        head->pred = new_node;
    }
    new_node->next = head;
    if (tail == nullptr) {
        tail = new_node;
    }
    head = new_node;
    size++;
    return RC::SUCCESS;
}

RC LinkList::pop_back()
{
    return remove(tail);
}

RC LinkList::remove(LinkNode * node)
{
    if (head == node) {
        head = node->next;
    }
    if (tail == node) {
        tail = node->pred;
    }
    if (node->pred != nullptr)
    {
        node->pred->next = node->next;
    }
    if (node->next != nullptr)
    {
        node->next->pred = node->pred;
    }
    size--;
    delete node;
    return RC::SUCCESS;
}