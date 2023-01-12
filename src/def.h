//
// Created by MorphLing on 2022/9/28.
//

#pragma once

#include <cstdint>
#include <string>
#include <sstream>
#include <iostream>
#include <cassert>
#include <memory>
#include <vector>
#include <map>
#include <list>
#include <unordered_map>
#include <set>
#include <unordered_set>
#include <algorithm>
#include <cstring>
#include <cmath>

struct trace_line {
    int starting_block;
    int number_of_blocks;
    int ignore;
    int request_number;
};

enum class RC {
    DEFAULT,
    SUCCESS,
    HIT,
    MISS,
    FAILED,
    UNIMPLEMENT,
};

enum class CachePolicy {
    LRU,
    LFU,
    ARC,
    ARC_2,
    ARC_3,
    OPT,
    MRF,
    STW,
    STW2,
    SRRIP,
    UNKNOWN,
};

typedef int32_t Key;
typedef std::string Value;

const int32_t BASIC_MAIN_ARG_NUM = 4;
const double EPSILON = 1e-10;
