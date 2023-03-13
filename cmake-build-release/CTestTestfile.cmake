# CMake generated Testfile for 
# Source directory: /home/ubuntu22/cache-performance-insight
# Build directory: /home/ubuntu22/cache-performance-insight/cmake-build-release
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(lru_test "/home/ubuntu22/cache-performance-insight/cmake-build-release/unittest/lru_test")
set_tests_properties(lru_test PROPERTIES  _BACKTRACE_TRIPLES "/home/ubuntu22/cache-performance-insight/CMakeLists.txt;31;add_test;/home/ubuntu22/cache-performance-insight/CMakeLists.txt;0;")
add_test(lfu_test "/home/ubuntu22/cache-performance-insight/cmake-build-release/unittest/lfu_test")
set_tests_properties(lfu_test PROPERTIES  _BACKTRACE_TRIPLES "/home/ubuntu22/cache-performance-insight/CMakeLists.txt;32;add_test;/home/ubuntu22/cache-performance-insight/CMakeLists.txt;0;")
add_test(arc_test "/home/ubuntu22/cache-performance-insight/cmake-build-release/unittest/arc_test")
set_tests_properties(arc_test PROPERTIES  _BACKTRACE_TRIPLES "/home/ubuntu22/cache-performance-insight/CMakeLists.txt;33;add_test;/home/ubuntu22/cache-performance-insight/CMakeLists.txt;0;")
add_test(opt_test "/home/ubuntu22/cache-performance-insight/cmake-build-release/unittest/opt_test")
set_tests_properties(opt_test PROPERTIES  _BACKTRACE_TRIPLES "/home/ubuntu22/cache-performance-insight/CMakeLists.txt;36;add_test;/home/ubuntu22/cache-performance-insight/CMakeLists.txt;0;")
add_test(mrf_test "/home/ubuntu22/cache-performance-insight/cmake-build-release/unittest/mrf_test")
set_tests_properties(mrf_test PROPERTIES  _BACKTRACE_TRIPLES "/home/ubuntu22/cache-performance-insight/CMakeLists.txt;37;add_test;/home/ubuntu22/cache-performance-insight/CMakeLists.txt;0;")
add_test(stw_test "/home/ubuntu22/cache-performance-insight/cmake-build-release/unittest/stw_test")
set_tests_properties(stw_test PROPERTIES  _BACKTRACE_TRIPLES "/home/ubuntu22/cache-performance-insight/CMakeLists.txt;38;add_test;/home/ubuntu22/cache-performance-insight/CMakeLists.txt;0;")
add_test(stw2_test "/home/ubuntu22/cache-performance-insight/cmake-build-release/unittest/stw2_test")
set_tests_properties(stw2_test PROPERTIES  _BACKTRACE_TRIPLES "/home/ubuntu22/cache-performance-insight/CMakeLists.txt;39;add_test;/home/ubuntu22/cache-performance-insight/CMakeLists.txt;0;")
add_test(srrip_test "/home/ubuntu22/cache-performance-insight/cmake-build-release/unittest/srrip_test")
set_tests_properties(srrip_test PROPERTIES  _BACKTRACE_TRIPLES "/home/ubuntu22/cache-performance-insight/CMakeLists.txt;40;add_test;/home/ubuntu22/cache-performance-insight/CMakeLists.txt;0;")
subdirs("src")
subdirs("unittest")
