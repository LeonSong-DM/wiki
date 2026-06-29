# 数字 日期 时间

------




## 数字操作

### 1.四舍五入
对于简单的舍入运算，使用内置的`round(value, ndigits)` 函数即可, `ndigits`代表保留小数的位数
值得注意的是:当一个值刚好在两个边界的中间的时候， `round `函数返回离它最近的偶数。


传给` round() `函数的` ndigits `参数可以是负数，这种情况下， 舍入运算会作用在十位、百位、千位等上面。比如：

``` python
>>> a = 1627731
>>> round(a, -1)
1627730
>>> round(a, -2)
1627700
>>> round(a, -3)
1628000
```


### 2.精确的浮点数运算
并不能精确的表示十进制数,即使是最简单的数学运算也会产生小的误差，比如：
``` python
>>> a = 4.2
>>> b = 2.1
>>> a + b
6.300000000000001
>>> (a + b) == 6.3
False
>>>
```
Python的浮点数据类型使用底层表示存储数据，因此你没办法去避免这样的误差。如果你想更加精确(并能容忍一定的性能损耗)，你可以使用`decimal`模块：

``` python
>>> from decimal import Decimal
>>> a = Decimal('4.2')
>>> b = Decimal('2.1')
>>> a + b
Decimal('6.3')
>>> print(a + b)
6.3
>>> (a + b) == Decimal('6.3')
True
```

`decimal`模块的一个主要特征是允许你控制计算的每一方面，包括数字位数和四舍五入运算, 不过得创建一个本地上下文并更改它的设置

``` python
from decimal import Decimal
from decimal import localcontext

a = Decimal("4.3")
b = Decimal("2.1")

with localcontext() as ctx:
    print(a / b)    # 2.047619047619047619047619048
    ctx.prec = 3
    print(a / b)    # 2.05
```



### 3.数字的格式化输出

格式化输出单个数字的时候，可以使用内置的`format()`函数，比如：

``` python
>>> x = 1234.56789

>>> # 精确到小数点后两位
>>> format(x, '0.2f')
'1234.57'

>>> # 右对齐10个字符，一位数精度
>>> format(x, '>10.1f')
'    1234.6'

>>> # 左对齐
>>> format(x, '<10.1f')
'1234.6    '

>>> # 居中
>>> format(x, '^10.1f')
'  1234.6  '

>>> # 包含千位分隔符
>>> format(x, ',')
'1,234.56789'

>>> # 用0填充宽度
>>> format(x, '0,.10f')
'1,234.5678900000'
>>>

```
同时指定宽度和精度的一般格式是`[<>^]?width[,]?(.digits)?`, 其中`width` 和 `digits` 为整数，`？`代表可选部分。 同样的格式也被用在字符串的 `format() `方法中, 解释为对齐方式, 宽度, 是否包含分隔符, 保留几位小数



### 4.字节到大整数的打包与解包

有时需要把字节字符串解压成一个整数, 或将一个大整数转换为一个字节字符串. 将字节字符串转为整数使用`int.from_byte()`方法, 将一个大整数转位一个字节字符串使用`int.to_byte()`方法, 并指定字节顺序:
``` python

>>> 字节字符串转大整数
>>> len(data)
16
>>> int.from_bytes(data, 'little')
69120565665751139577663547927094891008
>>> int.from_bytes(data, 'big')
94522842520747284487117727783387188

>>> # 大整数转字节字符串
>>> x = 94522842520747284487117727783387188
>>> x.to_bytes(16, 'big')
b'\x00\x124V\x00x\x90\xab\x00\xcd\xef\x01\x00#\x004'
>>> x.to_bytes(16, 'little')
b'4\x00#\x00\x01\xef\xcd\x00\xab\x90x\x00V4\x12\x00'
```



### 5.分数运算
`fractions`模块可以被用来执行包含分数的数学运算, 比如`Fraction(numerator, denominator)`:
``` python
>>> from fractions import Fraction
>>> a = Fraction(5, 4)
>>> b = Fraction(7, 16)
>>> print(a + b)
27/16
>>> print(a * b)
35/64

>>> # 得到分子 / 分母
>>> c = a * b
>>> c.numerator
35
>>> c.denominator
64

>>> # 转为浮点数
>>> float(c)
0.546875

>>> # 找到一个分母不超过指定值的最接近的分数
>>> print(c.limit_denominator(8))
4/7

>>> # 将浮点数转为分数类型
>>> x = 3.75
>>> y = Fraction(*x.as_integer_ratio())
>>> y
Fraction(15, 4)
```



### 6.随机选择

多用于从一个序列中随机抽取若干元素或生成随机数
``` python
values = [1, 2, 3, 4, 5, 6]
print(random.choice(values))    # 从values序列中随机抽取一个元素

print(random.sample(values, 2)) # 取出N个不同元素的样本
```

如果仅仅只是想打乱序列中元素的顺序，可以使用`random.shuffle()`
``` python
random.shuffle(values)
print(values)   # [5, 2, 4, 1, 3, 6]
```

使用`random.randint(a, b)`生成`[a,b)`范围内的随机整数, 使用`random.random()`生成`[0,1)`范围内均匀分布的浮点数
``` python
a = random.randint(0, 10)
b = random.random()
print(a)
print(b)
```

## 日期

### 1.日期与时间转换
使用`datetime`模块执行简单的时间转换, 比如天到秒，小时到分钟等的转换, 可以创建一个`timedelta`实例表示一个时间段,`timedelta` 会把时间拆成：`days`, `seconds`, `microseconds`
``` python
>>> from datetime import timedelta
>>> a = timedelta(days=2, hours=6)
>>> b = timedelta(hours=4.5)
>>> c = a + b
>>> c.days
2
>>> c.seconds   # 去除整天之后剩余的秒数, 即10.5hours * 60
37800
>>> c.seconds / 3600        
10.5
>>> c.total_seconds() / 3600    
58.5
>>>
```

创建一个`datetime`实例表示指定的日期和时间，然后使用标准的数学运算来操作它们。比如：
``` python
from datetime import datetime, timedelta

dt1 = datetime(2025, 10, 11)
dt2 = dt1 + b

print(dt1)  # 2025-10-11 00:00:00
print(dt2)  # 2025-10-11 05:00:00

# 获取当前时间
now = datetime.today()
print(now)  # 2026-03-05 00:53:47.764217
print(now + b)  # 4.5h之后
```





### 2.字符串转为日期

即 `string format time`与 `string parse time`, 前者用于将日期类型格式化成指定格式的字符串, 后者用于将字符串解析成指定格式的日期类,值得注意的是, 解析需要严格按照字符串的模板结构.

#### 2.1 strptime

``` python
a = "2026-03-08 15:30"
b = datetime.strptime(a, "%Y-%m-%d %H:%M")
print(b)    # 2026-03-08 15:30:00
```

strptime 返回的是一个 datetime 对象，而 datetime 的内部结构固定包含：
 - year
 - month
 - day
 - hour
 - minute
 - second
 - microsecond

对于缺失的结构, 解析器会自动补0. 



#### 2.2 strftime

在日期类型格式化成字符串时, 可以根据需要自定义字符串格式:

``` python
c = datetime.strftime(b, "%m %d, %Y %H:%M:%S")
print(c)    # 03 08, 2026 15:30:00
```