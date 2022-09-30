cmake_minimum_required(VERSION 3.16)
project(cache_performance_insight)

set(CMAKE_CXX_STANDARD 14)

SET(CMAKE_COMMON_FLAGS  -coverage)

IF(DEBUG)
    MESSAGE("DEBUG has been set as TRUE ${DEBUG}")
    SET(CMAKE_COMMON_FLAGS "${CMAKE_COMMON_FLAGS} -O0 -g -DDEBUG")
    ADD_DEFINITIONS(-DENABLE_DEBUG)
ELSEIF(NOT DEFINED ENV{DEBUG})
    MESSAGE("Disable debug")
    SET(CMAKE_COMMON_FLAGS "${CMAKE_COMMON_FLAGS} -O2 -g")
ELSE()
    MESSAGE("Enable debug")
    SET(CMAKE_COMMON_FLAGS "${CMAKE_COMMON_FLAGS} -O0 -g -DDEBUG")
    ADD_DEFINITIONS(-DENABLE_DEBUG)
ENDIF()

MESSAGE("CMAKE_COMMON_FLAGS is " ${CMAKE_COMMON_FLAGS})
SET(CMAKE_CXX_FLAGS ${CMAKE_COMMON_FLAGS})
SET(CMAKE_C_FLAGS ${CMAKE_COMMON_FLAGS})
MESSAGE("CMAKE_CXX_FLAGS is " ${CMAKE_CXX_FLAGS})

ADD_SUBDIRECTORY(src)
ADD_SUBDIRECTORY(unittest)


enable_testing()
add_test(NAME lfu_test COMMAND lfu_test)
add_test(NAME lru_test COMMAND lru_test)

find_program(LCOV lcov REQUIRED)
find_program(GENHTML genhtml REQUIRED)

add_custom_target(coverage
        COMMAND ${LCOV} --directory . --capture --output-file coverage.info
        COMMAND ${LCOV} --extract coverage.info '*/src/*' --output-file coverage2.info
        COMMAND ${GENHTML} --demangle-cpp -o coverage coverage2.info)