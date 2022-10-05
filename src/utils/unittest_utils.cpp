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
        for (auto i = l.starting_block; i < (l.starting_block + l.number_of_blocks); ++i) {
            UnittestUtils::check_get(cacheManager.get(), i);
        }
    }
    std::cout << cacheManager->statics();
    return RC::SUCCESS;
}

RC UnittestUtils::check_get(CacheManager * cacheManager, Key &key) {
    cacheManager->get(key);
    RC status = cacheManager->check_consistency();
    return status;
}