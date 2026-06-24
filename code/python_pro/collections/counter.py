from collections import Counter

################# 初始化 #################
print(f"{' Initialize ':=^80}")

# 1. 传入可迭代对象
c1 = Counter("Hello")
print(c1)

# 2. 传入字典或关键字参数
c2 = Counter(cat=3, dog=4)
print(c2)

# 核心特性： 访问不存在的键时不会触发 keyError, 而是返回 0
print(c2["pig"])

"""
Counter 是 dict 的子类，也继承了 dict 的所有方法
"""

################# API #################
print(f"{' API ':=^80}")

words = ["hello", "hello", "nice", "nice", "nice", "bad"]

# 1. most_common(n: int) 返回频率最高的 Top n的列表，每个项是 (item, count) 的元组
c = Counter(words)
print(c.most_common(2))

# 2. elements() 返回一个迭代器，将里面的元素按照计数值重复输出，顺序不固定
for item in c.elements():
    print(item)

# 3. update subtract 计数的增与减
# update() 可以接收关键字参数或字典，会在原有计数器的基础上累加
# subtract() 只接收字典，在原有基础上扣减

c = Counter(a=3, b=4)
c.update(a=3)
c.update({"b": 10})
c.subtract({"b": 2})
print(c)

# 4. 计数器也支持运算符，可以直接对两个计数器进行加、减、交、并
print(f"{' Counter Operate ':=^80}")
c1 = Counter(a=3, b=1)
c2 = Counter(a=1, b=2, c=3)

print(c1 + c2)
print(c1 - c2)  # 只保留正数结果
print(c1 & c2)  # 取两者共同元素的最小值
print(c1 | c2)  # 取两者元素的最大值

# 5. 计算总计数值
sum_counter = Counter(a=3, b=5)
print(sum_counter.total())


"""
eg. 文本词频与高频词过滤
"""
print(f"{' Example ':=^80}")

text = "python is good python is standard python is powerful standard user"
words = text.split()

# 定义无意义词
stop_words = ["is", "user"]

# 过滤
filtered_count = Counter(word for word in words if word not in stop_words)

print(filtered_count)
