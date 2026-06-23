from collections import Counter

"""

"""


# 统计列表中单词的个数
words = ["red", "blue", "red", "black", "blue", "blue"]
counter = Counter()

for word in words:
    counter[word] += 1

print(counter)
