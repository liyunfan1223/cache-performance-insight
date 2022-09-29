cmake_minimum_required(VERSION 3.16)
PROJECT(unittest)

MESSAGE("UNITTEST CMAKE_COMMON_FLAGS ${CMAKE_COMMON_FLAGS}")
MESSAGE("PROJECT_SOURCE_DIR: ${PROJECT_SOURCE_DIR}")
#MESSAGE(${PROJECT_BINARY_DIR})

INCLUDE_DIRECTORIES(. ${PROJECT_SOURCE_DIR}/../src)

FILE(GLOB_RECURSE ALL_SRC *.cpp)
FILE(GLOB MAIN_SRC ../src/main.cpp)
MESSAGE(${ALL_SRC})

LINK_LIBRARIES(main_static)

FOREACH (F ${ALL_SRC})
    IF (NOT ${F} STREQUAL ${MAIN_SRC})
        get_filename_component(prjName ${F} NAME_WE)
        MESSAGE("Build ${prjName} according to ${F}")
        ADD_EXECUTABLE(${prjName} ${F})
    ENDIF()
ENDFOREACH (F)