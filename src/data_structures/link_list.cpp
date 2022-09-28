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

RC LinkList::PushFront(Key key)
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

RC LinkList::PushFront(Key key, Value value)
{
    LinkNode * new_node = new LinkNode(key, value);
    head->pred = new_node;
    new_node->next = head;
    if (tail == nullptr) {
        tail = new_node;
    }
    head = new_node;
    size++;
    return RC::SUCCESS;
}

RC LinkList::PopBack()
{
    LinkNode * old_tail = tail;
    tail = tail->pred;
    if (tail->next != nullptr) {
        tail->next = nullptr;
    }
    size--;
    delete old_tail;
    return RC::SUCCESS;
}

RC LinkList::Remove(LinkNode * node)
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