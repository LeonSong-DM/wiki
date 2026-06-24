"""deque 双端队列
double-ended queue
"""

from collections import deque

# 初始化
dq = deque([1, 2, 3, 4], maxlen=20)

print(dq)

# API - 添加元素
print(f"{' Add Element ':=^80}")

# 1. 从右端添加数据
dq.append(5)
print(dq)

# 2. 从左端添加数据
dq.appendleft(0)
print(dq)

# 3. 从右侧拓展 iterable 参数中的元素
dq.extend([6, 7])
dq.extendleft([-1, -2])
print(dq)

# 4. 在指定位置插入值，如果超出 maxlen 触发 IndexError
dq.insert(0, -3)
print(dq)


# API - 获取元素
print(f"{' Get Element ':=^80}")

# 1. 取出最右侧元素
r = dq.pop()
print(r)
print(dq)

# 2. 取出最左侧元素
l = dq.popleft()
print(l)
print(dq)

# 3. 移除找到的第一个 value， 没找到触发 ValueError
dq.remove(-2)

try:
    dq.remove(100)
except Exception as e:
    print(type(e))


# 4. 将 deque 逆序排列并返回 None
res = dq.reverse()
assert res is None
print(dq)

# 5. 向左/右循环移动 n 步，用正负控制方向， 正方向向右
# 向右循环1步 => dq.appendleft(dq.pop())
# 向左循环1步 => dq.append(dq.popleft())
dq.rotate(1)
print(dq)

dq.rotate(-1)
print(dq)


# 查找指定值的元素索引，可以指定查找范围
print(dq.index(4, 0, 5))


# Deque - 属性
print(f"{' Deque 属性 ':=^80}")
print(dq.maxlen)
