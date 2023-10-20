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
#include <sys/time.h>

// defined for LIRS
#define NEED_PRUNING(n) ((n)->type != LIR)
#define NONEVALUE ((long long)-11)
#define INVALID (NONEVALUE)
#define IS_VALID(value) ((value) != NONEVALUE && (value) != INVALID)
enum lirs_type {
    LIR = 101,
    HIR,
    NHIR,
};
// end
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
    DRRIP,
    EFSW,
    LRFU,
    ALRFU,
    ALRFU2,
    ALRFU3,
    ALRFU4,
    ALRFU5,
    GLRFU,
    GLRFU2,
    GLRFU3,
    GLRFU4,
    LIRS,
    DLIRS,
    RGC,
    RGC2,
    RGC3,
    RGC4,
    CACHEUS,
    UNKNOWN,
};

typedef int32_t Key;
typedef std::string Value;

typedef int32_t PageId;
typedef int32_t FrameId;

const int32_t BASIC_MAIN_ARG_NUM = 4;
const double EPSILON = 1e-10;
