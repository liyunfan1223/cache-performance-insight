# Cache Performance Insight

Cache performance insight is a framework aim at evaluating performance on different 
cache policy with different workloads and configurations.

## Build
```
mkdir build
cd build
cmake ..
make
```

## Usage
```
./main <buffer_size> <trace_file>
```

## Example
```
./main 65536 ../../traces/P1.lis
LRU_CACHE_MANAGER buffer_size:65536 hit_count:11011495 miss_count:21043978 hit_rate:34.3514%
LFU_CACHE_MANAGER buffer_size:65536 hit_count:12421166 miss_count:19634307 hit_rate:38.749%
```

## TODO
### Cache policies
- [x] LRU
- [x] LFU
- [ ] ARC
- [ ] ...

### Features
- [x] cmake build
- [ ] unit tests
- [ ] log system
- [ ] parameters
- [ ] ...