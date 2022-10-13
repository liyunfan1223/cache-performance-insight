# Cache Policies

## LRU
Least Recently Used

## LFU
Least Frequently Used

## ARC
Adaptive Replacement Cache

**Reference:** 
- Paper: [ARC: A SELF-TUNING, LOW OVERHEAD REPLACEMENT CACHE](https://www.usenix.org/conference/fast-03/arc-self-tuning-low-overhead-replacement-cache)
- Notes: [Adaptive Replacement Cache(ARC) 缓存淘汰算法](https://zhuanlan.zhihu.com/p/522306900)

## FF

Farthest in Future

**Reference:**
- Introduction & Proof of Optimality: [算法复习笔记：贪心求最优Caching策略](https://blog.macromogic.xyz/2020/06/15/ff-cache/)

## ARC2
ARC based. With prior frequency.

If key frequency over the bound, always move to T2 directly when cache miss occurs.

## ARC3
ARC based. With prior frequency.

Reverse some place for high frequency key.