//
// Created by MorphLing on 2022/9/28.
//

#include <iostream>

#include "def.h"
#include "managers/lru_cache_manager.h"

#include "test_class/test_class.h"

int32_t make_test(int32_t buffer_size, const char * filename)
{
    FILE * pFile;
    pFile = fopen(filename, "r");
    if (pFile == NULL) {
        std::cerr << "can't not find trace_file" << std::endl;
        return -1;
    }
    trace_line l;
    LRUCacheManager lruCacheManager(buffer_size);
    while (fscanf(pFile, "%d %d %d %d\n",
                  &l.starting_block, &l.number_of_blocks, &l.ignore, &l.request_number) != EOF) {
        for (auto i = l.starting_block; i < (l.starting_block + l.number_of_blocks); ++i) {
            lruCacheManager.get(i);
        }
    }
    std::cout << lruCacheManager.statics();
    return 0;
}

int main(int argc, char **argv) {
    make_test(std::stoi(argv[1]), argv[2]);
//    make_test(1000, "../traces/P1.lis");
//    make_test(10000, "../traces/P1.lis");
//    make_test(100000, "../traces/P1.lis");
//    make_test(1000000, "../traces/P1.lis");
    return 0;
}


