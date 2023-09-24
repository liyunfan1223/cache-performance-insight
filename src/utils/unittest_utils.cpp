//
// Created by MorphLing on 2022/10/5.
//

#include "unittest_utils.h"

RC UnittestUtils::make_test(const char *filename, std::shared_ptr<CacheManager> cacheManager)
{
    FILE * pFile;
    pFile = fopen(filename, "r");
    if (pFile == NULL) {
        std::cerr << "can't not find trace_file" << std::endl;
        return RC::FAILED;
    }
    trace_line l;
    while (fscanf(pFile, "%d %d %d %d\n",
                  &l.starting_block, &l.number_of_blocks, &l.ignore, &l.request_number) != EOF) {
//        std::cerr << "a";
        for (auto i = l.starting_block; i < (l.starting_block + l.number_of_blocks); ++i) {\
//            std::cerr << b";
            UnittestUtils::check_get(cacheManager.get(), i);
//            assert(UnittestUtils::check_get(cacheManager.get(), i) != RC::FAILED);
        }
    }
    std::cout << cacheManager->statics();
    return RC::SUCCESS;
}

RC UnittestUtils::make_test(std::vector<int32_t> access_order, std::shared_ptr<CacheManager> cacheManager) {
    for (int i : access_order) {
        assert(UnittestUtils::check_get(cacheManager.get(), i) != RC::FAILED);
    }
    std::cout << cacheManager->statics();
    return RC::SUCCESS;
}

RC UnittestUtils::check_get(CacheManager * cacheManager, Key &key) {
    cacheManager->get(key);
    RC status = cacheManager->check_consistency();
    return status;
}

RC UnittestUtils::get_access_list(const char * filename, std::vector<Key> & access_list) {
    FILE * pFile;
    pFile = fopen(filename, "r");
    if (pFile == NULL) {
        std::cerr << "can't not find trace_file" << std::endl;
        return RC::FAILED;
    }
    trace_line l;
    while (fscanf(pFile, "%d %d %d %d\n",
                  &l.starting_block, &l.number_of_blocks, &l.ignore, &l.request_number) != EOF) {
        for (auto i = l.starting_block; i < (l.starting_block + l.number_of_blocks); ++i) {
            access_list.push_back(i);
        }
    }
    printf("Access size: %ld\n", access_list.size());
    return RC::SUCCESS;
}


RC UnittestUtils::get_access_list(const char * filename, std::vector<Key> & access_list, int32_t &unique_key_nums) {
    FILE * pFile;
    pFile = fopen(filename, "r");
    if (pFile == NULL) {
        std::cerr << "can't not find trace_file" << std::endl;
        return RC::FAILED;
    }
    trace_line l;
    std::unordered_set<int32_t> unique_key_set;
    while (fscanf(pFile, "%d %d %d %d\n",
                  &l.starting_block, &l.number_of_blocks, &l.ignore, &l.request_number) != EOF) {
        for (auto i = l.starting_block; i < (l.starting_block + l.number_of_blocks); ++i) {
            unique_key_set.insert(i);
            access_list.push_back(i);
        }
    }
    unique_key_nums = unique_key_set.size();
    printf("Unique keys: %ld\n", unique_key_set.size());
    printf("Access size: %ld\n", access_list.size());
    return RC::SUCCESS;
}


