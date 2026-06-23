import collections

from collections import Counter

print(collections.__all__)


words = ["hello", "word", "nice", "hello", "word"]

res = {}

# 利用内建数据容器
for word in words:
    res[word] = res.get(word, 0) + 1

print(res)


# 利用 collections.Counter()

cnt = Counter()

for word in words:
    cnt[word] += 1

print(cnt)
