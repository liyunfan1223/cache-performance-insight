# Cache Performance Insight ![](https://img.shields.io/badge/build-passing-brightgreen) ![](https://img.shields.io/badge/coverage-96%25-brightgreen)

> Cache Performance Insight is a framework designed to evaluate the performance of different cache policies with 
> different workloads and configurations.

## Build
```
mkdir build && cd build
cmake .. && make
```

## Usage
```
./src/main <buffer_size> <trace_file>
```

## Example
```
./src/main 65536 ../traces/P1.lis
LRU_CACHE_MANAGER:  buffer_size:65536 hit_count:11011495 miss_count:21043978 hit_rate:34.3514%
LFU_CACHE_MANAGER:  buffer_size:65536 hit_count:12421166 miss_count:19634307 hit_rate:38.749%
ARC_CACHE_MANAGER:  buffer_size:65536 hit_count:14268223 miss_count:17787250 hit_rate:44.511%
FF_CACHE_MANAGER:  buffer_size:65536 hit_count:20313683 miss_count:11741790 hit_rate:63.3704%
```

## Unittest & Coverage
```
ctest && make coverage
```
## TODO

### Cache policies
- [x] LRU
- [x] LFU
- [x] ARC
- [x] FF
- [ ] ARC-2
- [ ] hybrid LRU-LFU
- [ ] ...

### Features
- [x] cmake build
- [x] unittest & code coverage
- [ ] log
- [ ] more parameters (e.g. scales, policies, unique keys)
- [ ] test scripts
- [ ] ...

### Metrics
- [x] cache hit rate
- [ ] runtime
- [ ] actual memory allocation
- [ ] concurrency
- [ ] real time cache distribution
- [ ] ...
