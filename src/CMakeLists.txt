cmake_minimum_required(VERSION 3.16)
PROJECT(main)

SET(CMAKE_COMMON_FLAGS  -coverage)
MESSAGE("MAIN CMAKE_COMMON_FLAGS ${CMAKE_COMMON_FLAGS}")

INCLUDE_DIRECTORIES(.)
INCLUDE_DIRECTORIES(./data_structures)

FILE(GLOB_RECURSE ALL_SRC *.cpp *.c)
FILE(GLOB MAIN_SRC main.cpp)
MESSAGE("MAIN SRC: " ${MAIN_SRC})
FOREACH (F ${ALL_SRC})
    IF (NOT ${F} STREQUAL ${MAIN_SRC})
        SET(LIB_SRC ${LIB_SRC} ${F}
                managers/rgc3_cache_manager.cpp
                managers/rgc3_cache_manager.h
                data_structures/deque_dict.hpp
                managers/dlirs_cache_manager.cpp
                managers/dlirs_cache_manager.h)
    ENDIF()
    MESSAGE("Use " ${F})
ENDFOREACH (F)

MESSAGE("LIB_SRC: ${LIB_SRC}")
ADD_EXECUTABLE(main ${ALL_SRC})
#SET_TARGET_PROPERTIES(
#        main  PROPERTIES COMPILE_FLAGS "-coverage"
#)
MESSAGE("CMAKE_INSTALL_PREFIX ${CMAKE_INSTALL_PREFIX}")

ADD_LIBRARY(main_static STATIC ${LIB_SRC})