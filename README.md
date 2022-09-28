## Cache Performance Insight

Cache performance insight is a framework aim at evaluating performance on different 
cache policy with different workloads and configurations.

## build
```
mkdir build
cd build
cmake ..
make
```

## run
```
./main <buffer_size> <trace_file>
```

## example
```
./main 100000 ../traces/P1.lis
lru_cache buffer_size:100000 hit_count:15407418 miss_count:16648055 hit_rate:48.0649%
```
