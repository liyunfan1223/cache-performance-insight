//
// Created by MorphLing on 2022/9/28.
//

#include <iostream>
#include <memory>

#include "def.h"
#include "managers/lru_cache_manager.h"
#include "managers/lfu_cache_manager.h"

int32_t make_test(const char * filename,
                  std::shared_ptr<CacheManager> cacheManager)
{
    FILE * pFile;
    pFile = fopen(filename, "r");
    if (pFile == NULL) {
        std::cerr << "can't not find trace_file" << std::endl;
        return -1;
    }
    trace_line l;
    while (fscanf(pFile, "%d %d %d %d\n",
                  &l.starting_block, &l.number_of_blocks, &l.ignore, &l.request_number) != EOF) {
        for (auto i = l.starting_block; i < (l.starting_block + l.number_of_blocks); ++i) {
            cacheManager->get(i);
        }
    }
    std::cout << cacheManager->statics();
    return 0;
}

int main(int argc, char **argv) {
    make_test(argv[2], std::shared_ptr<CacheManager>(new LRUCacheManager(std::stoi(argv[1]))));
    make_test(argv[2], std::shared_ptr<CacheManager>(new LFUCacheManager(std::stoi(argv[1]))));
    return 0;
}


