# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.22

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/ubuntu22/cache-performance-insight

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/ubuntu22/cache-performance-insight/cmake-build-release

# Include any dependencies generated for this target.
include unittest/CMakeFiles/lru_test.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include unittest/CMakeFiles/lru_test.dir/compiler_depend.make

# Include the progress variables for this target.
include unittest/CMakeFiles/lru_test.dir/progress.make

# Include the compile flags for this target's objects.
include unittest/CMakeFiles/lru_test.dir/flags.make

unittest/CMakeFiles/lru_test.dir/lru_test.cpp.o: unittest/CMakeFiles/lru_test.dir/flags.make
unittest/CMakeFiles/lru_test.dir/lru_test.cpp.o: ../unittest/lru_test.cpp
unittest/CMakeFiles/lru_test.dir/lru_test.cpp.o: unittest/CMakeFiles/lru_test.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/ubuntu22/cache-performance-insight/cmake-build-release/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object unittest/CMakeFiles/lru_test.dir/lru_test.cpp.o"
	cd /home/ubuntu22/cache-performance-insight/cmake-build-release/unittest && /usr/bin/clang++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT unittest/CMakeFiles/lru_test.dir/lru_test.cpp.o -MF CMakeFiles/lru_test.dir/lru_test.cpp.o.d -o CMakeFiles/lru_test.dir/lru_test.cpp.o -c /home/ubuntu22/cache-performance-insight/unittest/lru_test.cpp

unittest/CMakeFiles/lru_test.dir/lru_test.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/lru_test.dir/lru_test.cpp.i"
	cd /home/ubuntu22/cache-performance-insight/cmake-build-release/unittest && /usr/bin/clang++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/ubuntu22/cache-performance-insight/unittest/lru_test.cpp > CMakeFiles/lru_test.dir/lru_test.cpp.i

unittest/CMakeFiles/lru_test.dir/lru_test.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/lru_test.dir/lru_test.cpp.s"
	cd /home/ubuntu22/cache-performance-insight/cmake-build-release/unittest && /usr/bin/clang++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/ubuntu22/cache-performance-insight/unittest/lru_test.cpp -o CMakeFiles/lru_test.dir/lru_test.cpp.s

# Object files for target lru_test
lru_test_OBJECTS = \
"CMakeFiles/lru_test.dir/lru_test.cpp.o"

# External object files for target lru_test
lru_test_EXTERNAL_OBJECTS =

unittest/lru_test: unittest/CMakeFiles/lru_test.dir/lru_test.cpp.o
unittest/lru_test: unittest/CMakeFiles/lru_test.dir/build.make
unittest/lru_test: src/libmain_static.a
unittest/lru_test: unittest/CMakeFiles/lru_test.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/ubuntu22/cache-performance-insight/cmake-build-release/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable lru_test"
	cd /home/ubuntu22/cache-performance-insight/cmake-build-release/unittest && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/lru_test.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
unittest/CMakeFiles/lru_test.dir/build: unittest/lru_test
.PHONY : unittest/CMakeFiles/lru_test.dir/build

unittest/CMakeFiles/lru_test.dir/clean:
	cd /home/ubuntu22/cache-performance-insight/cmake-build-release/unittest && $(CMAKE_COMMAND) -P CMakeFiles/lru_test.dir/cmake_clean.cmake
.PHONY : unittest/CMakeFiles/lru_test.dir/clean

unittest/CMakeFiles/lru_test.dir/depend:
	cd /home/ubuntu22/cache-performance-insight/cmake-build-release && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/ubuntu22/cache-performance-insight /home/ubuntu22/cache-performance-insight/unittest /home/ubuntu22/cache-performance-insight/cmake-build-release /home/ubuntu22/cache-performance-insight/cmake-build-release/unittest /home/ubuntu22/cache-performance-insight/cmake-build-release/unittest/CMakeFiles/lru_test.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : unittest/CMakeFiles/lru_test.dir/depend

