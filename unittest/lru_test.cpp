//
// Created by l50029536 on 2022/9/29.
//

#include <iostream>
#include <cassert>

#include "managers/lru_cache_manager.h"

int main() {
    CacheManager * cacheManager = new LRUCacheManager(100);
    int hit_count1 = 0, hit_count2 = 0;
    for (int i = 0; i < 100; i++) {
        cacheManager->get(i);
    }

    hit_count1 = cacheManager->hit_count();
    cacheManager->get(0);
    hit_count2 = cacheManager->hit_count();
    assert(hit_count1 + 1 == hit_count2);

    cacheManager->get(100);
    hit_count1 = cacheManager->hit_count();
    cacheManager->get(1);
    hit_count2 = cacheManager->hit_count();
    assert(hit_count1 == hit_count2);

    std::cout << "LRU TEST SUCCESS." << std::endl;
    return 0;
}