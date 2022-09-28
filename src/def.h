//
// Created by MorphLing on 2022/9/28.
//

#pragma once

#include <cstdint>
#include <string>

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
    UNIMPLEMENT
};

typedef int32_t Key;
typedef std::string Value;


