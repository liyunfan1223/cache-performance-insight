//
// Created by Clouds on 2023/9/20.
//

#ifndef CACHE_PERFORMANCE_INSIGHT_LIRS_CACHE_MANAGER_H
#define CACHE_PERFORMANCE_INSIGHT_LIRS_CACHE_MANAGER_H


#include <list>
#include <iostream>
#include <unordered_map>
#include <map>
#include <assert.h>
#include <stdio.h>
#include <managers/cache_manager.h>

#define NEED_PRUNING(n) ((n)->type != LIR)
#define NONE ((long long)-11)
#define INVALID (NONE)
#define IS_VALID(value) ((value) != NONE && (value) != INVALID)
struct lirs_node;
typedef std::list<lirs_node*>::iterator lirs_iterator;

enum lirs_type {
    LIR = 101,
    HIR,
    NHIR,
};

struct lirs_node {
    long long key;
    long long value;

    lirs_type type;
    lirs_iterator s;
    lirs_iterator q;

    lirs_node(long long _key, long long _value, lirs_iterator ends, lirs_iterator endq)
            : key(_key), value(_value), s(ends), q(endq), type(LIR) {}
    lirs_node(long long _key, long long _value, lirs_iterator ends, lirs_iterator endq, lirs_type _type)
            : key(_key), value(_value), s(ends), q(endq), type(_type) {}

    void Set(lirs_type _type) { type = _type;}
};

class LIRSCacheManager: public CacheManager {
public:
    LIRSCacheManager(int32_t buffer_size) : CacheManager(buffer_size), cache_size_(buffer_size), used_size_(0) {
        q_size_ = std::max(1, (int)(0.01 * buffer_size));
//        q_size_ = 1;
        s_size_ = buffer_size - q_size_;
    }

    RC get(const Key &key) override;

    RC put(const Key &key, const Value &value) override;

    std::string get_name() override;

    ~LIRSCacheManager() {
        for (auto it = map_.begin(); it != map_.end(); ++it) {
            //std::cout << "key: " << it->second->key << std::endl;
            delete (it->second);
        }
//        printf("%d %d %d %d\n", tot, c_lir, c_hir_s, c_hir_ns);
    }

    void FreeOne() {
        assert(!q_.empty());

        auto pnode = q_.back();
        q_.pop_back();
        pnode->q = q_.end();

        if (IS_VALID(pnode->value)) {
            pnode->value = INVALID;
            -- used_size_;
        }

        if (pnode->s != s_.end()) {
            pnode->type = NHIR;
        } else {
            //std::cout << "Free Pnode" << std::endl;
            map_.erase(pnode->key);
            delete pnode;
        }
    }

    bool Add(long long key, long long value) {
        //Print();
        if (map_.find(key) != map_.end()) { // find it
            auto pnode = map_[key];
            if (!IS_VALID(pnode->value)) {
                ++ used_size_;
            }
            Get(key, value);

            return true;
        }

        if (used_size_ >= cache_size_ || q_.size() >= q_size_) { // 清理
            FreeOne();
        }

        // S is not FULL, so just input it as LIR
        lirs_node *p = new lirs_node(key, value, s_.end(), q_.end());
        assert(p);
        Push(p, true);
        ++ used_size_;

        // S is FULL, so just input it as HIR
        if (used_size_ > s_size_) {
            //if (s_.size() > s_size_) {
            p->type = HIR;
            Push(p, false);
        }

        return true;
    }

    long long Get(long long key, long long value = 10) {
        if (map_.find(key) == map_.end()) {
            return NONE;
        }
        auto p = map_[key];

        if (p->type == LIR) {
            increase_hit_count();
            assert(p->s != s_.end());
            MoveTop(p);
            c_lir++;
        }
        else if (p->type == HIR && IS_VALID(p->value)) {
            increase_hit_count();
            c_hir_s++;
            assert(p->q != q_.end());
            if (p->s != s_.end()) {
                p->type = LIR;

                MoveTop(p);
                Pop(p, false);
                Bottom();
            } else {
                Push(p, true);
                MoveTop(p, false);
            }
        }
//            }
        else {
            increase_miss_count();
            c_hir_ns++;
            assert(p->type == NHIR);
            FreeOne();
            p->value = value;

            if (p->s != s_.end()) {
                p->type = LIR;
                MoveTop(p);
                Bottom();
            } else {
                assert(p->q == q_.end());
                p->type = HIR;
                Push(p, true);
                Push(p, false);
            }
        }
        Pruning();

        return p->value;
    }

    long long Peek(long long key) {
        long long value = NONE;
        if (map_.find(key) != map_.end()) {
            value = map_[key]->value;
        }

//        sta_.Hit(value);
        return value;
    }

    void Pruning() {
        while (!s_.empty() && NEED_PRUNING(s_.back())) {
            s_.back()->s = s_.end();
            s_.pop_back();
        }
    }

//    void Print(bool flag = false) {
//        if (! flag) {
//            for (auto pit = s_.begin(); pit != s_.end(); ++pit) {
//                auto it = *pit;
//                std::cout << "[" << it->key << ":" << it->value << " " << it->type << "]";
//            }
//            std::cout << std::endl;
//
//            for (auto pit = q_.begin(); pit != q_.end(); ++pit) {
//                auto it = *pit;
//                std::cout << "[" << it->key << ":" << it->value << " " << it->type << "]";
//            }
//            std::cout << std::endl;
//        }
//
//        sta_.Print();
//        std::cout << "{" << s_.size() << ":" << q_.size() << "}"
//                  << "{" << used_size_ << ":" << s_size_ << ":" << q_size_  << "}" << std::endl;
//    }

private:
    int c_lir{}, c_hir_s{}, c_hir_ns{}, tot{};
    void Bottom() {
        auto bottom = s_.back();
        if (bottom->type == LIR) {
            bottom->type = HIR;
            if (bottom->q != q_.end()) {
                Pop(bottom, false);
            }
            Push(bottom, false);
        }
    }
    // true to S, false to Q
    void Push(lirs_node *p, bool toS) {
        if (toS) {
            s_.push_front(p);
            p->s = s_.begin();
        } else {
            q_.push_front(p);
            p->q = q_.begin();
        }

        if (map_.find(p->key) == map_.end()) {
            map_[p->key] = p;
        }
    }

    void Pop(lirs_node *p, bool fromS) {
        if (fromS) {
            assert(p->s != s_.end());
            s_.erase(p->s);
            p->s = s_.end();
        } else {
            assert(p->q != q_.end());
            q_.erase(p->q);
            p->q = q_.end();
        }
    }

    void MoveTop(lirs_node *p, bool toS = true) {
        Pop(p, toS);
        Push(p, toS);
    }

    // front -- top  back  -- bottom
    std::list<lirs_node*> s_, q_;
    std::map<long long, lirs_node*> map_;

    long long cache_size_, used_size_;
    long long s_size_;
    long long q_size_;

//    statistic sta_;
};

#endif //CACHE_PERFORMANCE_INSIGHT_LIRS_CACHE_MANAGER_H
