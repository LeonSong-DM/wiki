# Author: LeonSong
# Email: le0n404@163.com
# Created: 2026-06-23 12:01:20
# """Description"""

# Collections

Collections 模块是对 Python 标准内建容器(list，dict, tuple, set)的补充, 它针对特定的使用场景丰富了内建容器类型的功能

用大白话说, collections 中的容器类型可以做到 Python 内建容器类型做不到的事情, 例如词频统计:

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
output

{'hello': 2, 'word': 2, 'nice': 1}
Counter({'hello': 2, 'word': 2, 'nice': 1})
```



标准内建类型在特定的场景下具有一定的局限性, 例如统计未知字段的数据时, 向字典中添加一个不存在的键会触发 KeyError, 但 collections.defaultdict 可以避免这个问题, 下面是一个统计词频的例子.


``` Python
sentence = "Woc Woc I access the final exam Woc !"
res = {}

for word in sentence.split():
    res[word] += 1  # 会触发 KeyError

print(res)
```


collections 中共有 9 个子类:

