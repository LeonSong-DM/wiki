# Collections

Collections 模块是对 Python 标准内建容器 (list，dict, tuple, set) 的补充, 它针对特定的使用场景丰富了内建容器类型的功能

用大白话说, collections 中的容器类型在完成某些功能的实现时会比使用 Python 内建容器更加便捷



``` Python
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
```

```
output:

{'hello': 2, 'word': 2, 'nice': 1}
Counter({'hello': 2, 'word': 2, 'nice': 1})
```

collections 中共有 9 个子类:

