# Pathlib

`pathlib` 是 Python 中处理路径最推荐的标准库之一

- 核心思路是把“路径”抽象成对象, 而不是来回拼字符串
- 同时覆盖路径拼接、文件判断、目录遍历、文件读写等常见操作
- 写脚本、做数据处理、整理工程目录时都很好用

> 本质上可以理解为: 面向对象版的 `os.path` + 一部分文件系统操作接口

---

## pathlib 概览

日常开发里, 如果还在频繁写 `os.path.join()`、`os.path.exists()`、`open()` 组合, 基本都可以考虑换成 `pathlib`
`patlib`重载了`/`运算符, 在这里代表的是路径拼接运算符

```python
from pathlib import Path

p = Path("data") / "users" / "info.json"
print(p)
print(type(p))

""" output

windows:
	data\users\info.json
	<class 'pathlib._local.WindowsPath'>
	
linux:
	data/users/leonsong
	<class 'pathlib.PosixPath'>

"""
```

**使用场景**

- 脚本里拼接路径
- 判断文件和目录是否存在
- 递归查找文件
- 读写文本、配置、日志文件

**注意事项**

- `Path` 对象本身不是字符串, 但大多数场景都可以直接使用
- 需要字符串时再用 `str(path)`

---

## Path 对象

### Path 和 PurePath

`pathlib` 里最核心的两个概念是 `PurePath` 和 `Path`

- `PurePath`: 只做路径计算, 不直接访问文件系统
- `Path`: 可以操作真实文件和目录, 比如判断存在、创建目录、打开文件

```python
from pathlib import Path, PurePath

p1 = PurePath("docs", "note.md")
p2 = Path("docs") / "note.md"

print(p1)
print(p2)
print(type(p1))
print(type(p2))
```

**使用场景**

- `PurePath` 适合只做路径推导
- `Path` 适合真实文件操作

**注意事项**

- `Path()` 会根据当前系统自动创建 `PosixPath` 或 `WindowsPath`
- 跨平台代码里尽量不要手写 `\` 或 `/` 去拼路径

### 常用属性

路径对象提供了很多拆解路径的属性, 这一点比字符串切分顺手很多

```python
from pathlib import Path

p = Path("project/data/report.csv")

print(p.name)       # report.csv	 获取文件名
print(p.stem)       # report	     文件名(无拓展名)
print(p.suffix)     # .csv		     文件拓展名(只取最后一个)
print(p.suffixes)   # ['.csv']	      所有文件拓展名(列表)
print(p.parent)     # project/data    父目录
print(p.parts)      # ('project', 'data', 'report.csv')   
```

**注意事项**

- `stem` 只去掉最后一个后缀
- 多重后缀文件如 `archive.tar.gz` 需要看 `suffixes`

---

## 路径拼接

`pathlib` 最常见的写法就是用 `/` 拼路径, 可读性很好

```python
from pathlib import Path

base = Path("data")
file_path = base / "images" / "cat.png"

print(file_path)	# data/images/cat.png
```

也可以使用 `joinpath()`

```python
from pathlib import Path

p = Path("data").joinpath("images", "cat.png")
print(p)	# data/images/cat.png
```

**使用场景**

- 组合项目路径
- 拼接输入输出目录
- 构建配置文件路径

**注意事项**

- 推荐优先使用 `/`, 更直观
- 如果后面拼进来的是绝对路径, 前面的部分会被覆盖, 这一点和 `os.path.join()` 一样

---

## 相对路径和绝对路径

### 判断是否为绝对路径

```python
from pathlib import Path

print(Path("/tmp/test").is_absolute())
print(Path("tmp/test").is_absolute())
```



### resolve()

`resolve()` 会把路径转成绝对路径, 并尽量消除 `.`、`..`, 同时解析符号链接

```python
from pathlib import Path

p = Path(".")
print(p.resolve())
```

**注意事项**

- 某些版本或场景下, 路径不存在时可能抛异常, 用之前最好明确当前路径是否有效



### relative_to()

`relative_to()` 用于计算相对某个基路径的结果, 即文件路径`file_path`对于项目路径`project_path`的相对路径

```python
from pathlib import Path

file_path = Path("/home/user/project/data/file.txt")
project_path = Path("/home/user/project")

print(file_path.relative_to(project_path))	

# output:
# data/file.txt
```

**注意事项**

- `relative_to()` 不是“自动求相对路径”
- 如果当前路径不是以基路径开头, 会直接抛 `ValueError`



---

## 文件和目录判断

`Path` 提供了很多直接判断的方法, 基本不用再回到 `os.path`

```python
from pathlib import Path

p = Path("example.txt")

print(p.exists())
print(p.is_file())
print(p.is_dir())
print(p.is_symlink())
```

**注意事项**

- `exists()` 只回答“在不在”
- `is_file()` 和 `is_dir()` 更适合做分支判断
- 不存在时, `is_file()` 和 `is_dir()` 一般返回 `False`

如果还需要文件详细信息, 可以配合 `stat()`

```python
from pathlib import Path

p = Path("example.txt")
if p.exists():
    stat = p.stat()
    print(stat.st_size)
```

---

## 目录操作

### mkdir()

创建目录是 `pathlib` 的高频操作之一

```python
from pathlib import Path

output_dir = Path("output/images")
output_dir.mkdir(parents=True, exist_ok=True)
print(output_dir.exists())
```

**参数 **

- `parents=True` 表示父目录不存在时一并创建
- `exist_ok=True` 表示目录已存在时不报错



### iterdir()

`iterdir()` 用来遍历当前目录的直接子项, 用于遍历某个目录下的文件(一级目录扫描), 只遍历当前层, 并且返回的是`Path`对象

```python
from pathlib import Path

p = Path(".")

for child in p.iterdir():
    print(child)
```



---

## glob 和遍历

### glob()

`glob()` 用模式匹配查找文件, 非递归时非常常用,  匹配范围是当前目录及模式指定的层级, 返回值仍然是 `Path` 对象

```python
from pathlib import Path

p = Path(".")

for file in p.glob("*.md"):
    print(file)
```



### rglob()

`rglob()` 相当于递归版 `glob()`, 可以递归扫描整个项目

```python
from pathlib import Path

p = Path(".")

for file in p.rglob("*.py"):
    print(file)
```



### match()

如果你已经拿到一个路径对象, 只想判断它是否符合某种 glob 模式, 可以用 `match()`

```python
from pathlib import PurePath

p = PurePath("src/app/main.py")
print(p.match("*.py"))
print(p.match("app/*.py"))
```

---



## 文件读写

### open()

`Path.open()` 本质上就是对象化的 `open()`

```python
from pathlib import Path

p = Path("demo.txt")

with p.open("w", encoding="utf-8") as f:
    f.write("hello pathlib")

with p.open("r", encoding="utf-8") as f:
    print(f.read())
```





### read_text() / write_text()

这两个是最顺手的便捷方法, 写学习脚本和小工具非常舒服, 二进制文件应使用 `read_bytes()` 和 `write_bytes()`

```python
from pathlib import Path

p = Path("note.txt")
p.write_text("pathlib makes path handling easier", encoding="utf-8")

content = p.read_text(encoding="utf-8")
print(content)
```





---

## 文件和路径修改

### touch()

用 `touch()`创建一个空文件

```python
from pathlib import Path

p = Path("empty.txt")
p.touch(exist_ok=True)
print(p.exists())
```



### rename() 和 replace()

```python
from pathlib import Path

src = Path("old.txt")
src.write_text("hello", encoding="utf-8")

dst = Path("new.txt")
src.rename(dst)

print(dst.read_text(encoding="utf-8"))
```

`replace()` 和 `rename()` 很像, 但如果目标已存在, `replace()` 会直接覆盖, 覆盖类操作要小心, 特别是生产脚本里



### unlink() 和 rmdir()

`unlink`删除文件或符号链接, `rmdir`只能删除空目录

```python
from pathlib import Path

file_path = Path("temp.txt")
file_path.write_text("temporary", encoding="utf-8")
file_path.unlink()

dir_path = Path("temp_dir")
dir_path.mkdir(exist_ok=True)
dir_path.rmdir()
```



---



## 路径格式转换

有时候需要把路径转成别的表示形式, 其中`as_uri()` 只能用于绝对路径, 否则会报错

```python
from pathlib import Path

p = Path("docs/readme.md")

print(str(p))
print(p.as_posix())			# 统一输出为 / 风格路径
print(p.resolve().as_uri())	 # 生成 file:// URI
```



## 常见技巧

### 获取当前工作目录

```python
from pathlib import Path

print(Path.cwd())
```

这在调试路径问题时很常用, 尤其是脚本和 Notebook 混着跑的时候

### 基于当前文件定位项目路径

```python
from pathlib import Path

current_file = Path(__file__).resolve()
project_root = current_file.parent
print(project_root)
```

这种写法适合定位脚本所在目录, 比直接依赖当前工作目录更稳

### 批量处理某类文件

```python
from pathlib import Path

for file in Path(".").rglob("*.txt"):
    print(file.name, file.suffix)
```

这种场景在数据清洗、日志处理、批量重命名里很常见

---

## pathlib vs os.path

`pathlib` 和 `os.path` 都能做路径处理, 但 `pathlib` 更适合现在的 Python 代码

- `os.path` 偏函数式, 经常要在字符串之间来回切换
- `pathlib` 偏对象式, 一个 `Path` 对象可以一路往下操作
- 代码可读性通常更好, 尤其是路径拼接和遍历部分

```python
import os
from pathlib import Path

p1 = os.path.join("data", "train", "a.txt")
p2 = Path("data") / "train" / "a.txt"

print(p1)
print(p2)
```

如果是新项目或者重构旧脚本, 我更倾向于直接使用 `pathlib`

---

## 小结

`pathlib` 最值得掌握的点其实不多, 但非常高频

- 用 `Path()` 创建路径对象
- 用 `/` 做路径拼接
- 用 `exists()`、`is_file()`、`is_dir()` 做判断
- 用 `iterdir()`、`glob()`、`rglob()` 做遍历
- 用 `open()`、`read_text()`、`write_text()` 做读写
- 用 `resolve()`、`relative_to()` 处理绝对路径和相对路径

