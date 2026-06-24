from collections import ChainMap

"""
将多个字典在逻辑上链接在一起，组成一个单一的视图，并非真正的合并
"""

baseline = {"theme": "light", "fontsize": 12, "show_sidebar": False}
user_config = {"theme": "dark", "fontsize": 13}

# 创建 ChainMap，优先读入前面的字典
settings = ChainMap(user_config, baseline)  # 传入顺序即优先级

# 查找时按照传入顺序获取，一旦找到立即返回
print(settings["theme"])
print(settings["fontsize"])
print(settings["show_sidebar"])

# 都不存在的键会触发 KeyError
try:
    print(settings["not_exist"])
except Exception as e:
    print(type(e))


print(f"{' Read & Write ':=^80}")

# ChainMap 的读操作是链式覆盖的，但写操作（增、删、改）只作用于第一个字典上, 即读写不对称
# 在实际开发中，该特性可以用于保护低优先级配置
dict1 = {"a": 1, "b": 2}
dict2 = {"a": 10, "b": 20}
chain = ChainMap(dict1, dict2)

# 修改 a 的值
chain["a"] = 9
print(dict1["a"])  # 被修改为 9
print(dict2["a"])

# 删除 b
del chain["b"]

print(dict1)
print(dict2)

# 添加 c = 30
chain["c"] = 30

print(dict1)
print(dict2)


print(f"{' Advanced API ':=^80}")

# 高级属性和方法
base = {"x": 1}
chain = ChainMap(base)

# 1. 使用 new_child() 进入一个 “子作用域”
# 返回一个新的 ChainMap 对象，里面包含除调用对象中第一个字典外的所有字典
local_scope = chain.new_child({"x": 2, "y": 3})
print(local_scope["x"])

# new_child() 会创建一个新的 ChainMap，并在最前面添加一个新的映射

# 2. 使用 parents 访问父级作用域
father_scope = local_scope.parents
print(father_scope["x"])

# 3. 通过 maps 属性在尾部追加字典
local_scope.maps.append({"z": 100})
print(local_scope["z"])

# maps 属性是一个可以读写的列表，里面按照顺序存放着所有底层的字典
print(local_scope.maps)


d1 = {"a": 1}
d2 = {"b": 2}
chain = ChainMap(d1, d2)

# 执行以下操作后，len(chain) 的结果是多少？
d1["a"] = 10
d2["c"] = 3

print(len(chain))

# 此时 len(chain) 是多少？如果执行 list(chain.keys()) 会看到什么？
print(list(chain.keys()))

# maps 属性中存放的是原始字典的引用，故它会随着原字典的改变实时改变


print(f"{' Test ':=^80}")

"""
Eg. 让用户指定的命令行参数优于默认配置
"""

import argparse
