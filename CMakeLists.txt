cmake_minimum_required(VERSION 3.16)
project(cache_performance_insight)

set(CMAKE_CXX_STANDARD 14)

INCLUDE_DIRECTORIES(src/)

FILE(GLOB_RECURSE ALL_SRC src/*.cpp src/*.c)
FILE(GLOB MAIN_SRC src/main.cpp)
MESSAGE("MAIN SRC: " ${MAIN_SRC})
FOREACH (F ${ALL_SRC})

    IF (NOT ${F} STREQUAL ${MAIN_SRC})
        SET(LIB_SRC ${LIB_SRC} ${F})
    ENDIF()

    MESSAGE("Use " ${F})

ENDFOREACH (F)

ADD_EXECUTABLE(main ${ALL_SRC})