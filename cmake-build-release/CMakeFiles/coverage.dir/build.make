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

# Utility rule file for coverage.

# Include any custom commands dependencies for this target.
include CMakeFiles/coverage.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/coverage.dir/progress.make

CMakeFiles/coverage:
	/usr/bin/lcov --directory . --capture --output-file coverage.info
	/usr/bin/lcov --extract coverage.info '*/src/*' --output-file coverage2.info
	/usr/bin/genhtml --demangle-cpp -o coverage coverage2.info

coverage: CMakeFiles/coverage
coverage: CMakeFiles/coverage.dir/build.make
.PHONY : coverage

# Rule to build all files generated by this target.
CMakeFiles/coverage.dir/build: coverage
.PHONY : CMakeFiles/coverage.dir/build

CMakeFiles/coverage.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/coverage.dir/cmake_clean.cmake
.PHONY : CMakeFiles/coverage.dir/clean

CMakeFiles/coverage.dir/depend:
	cd /home/ubuntu22/cache-performance-insight/cmake-build-release && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/ubuntu22/cache-performance-insight /home/ubuntu22/cache-performance-insight /home/ubuntu22/cache-performance-insight/cmake-build-release /home/ubuntu22/cache-performance-insight/cmake-build-release /home/ubuntu22/cache-performance-insight/cmake-build-release/CMakeFiles/coverage.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/coverage.dir/depend
