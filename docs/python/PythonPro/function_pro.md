# 函数进阶



## 函数的多返回值

按照返回值的顺序（中间用逗号隔开），写对应顺序的多个变量接收即可，也支持不同类型数据的`return`

```python
def get_value():
	return 1, 2

a, b = get_value()
print(a, b)	# 1, 2
```



## 函数的传参方式

### 缺省参数

缺省参数也叫默认参数，用于定义函数，为参数提供默认值，调用函数时可不传该默认参数的值，但是所有位置参数必须出现在默认参数前

```python
def print_info(name, age, class_number, school='SLU'):
    print(f"{name} {age} {class_number} {school}")

# 有默认值school = SLU
print_info('leon', 18, 3)
```

### 不定长参数

不定长参数也叫可变参数，用于不确定调用的时候会传递多少个参数的场景，不定长参数有两个类型：

- 位置传递

    传进的所有参数都会被args变量收集，它会根据传进参数的位置和并称为一个元组`tuple`，**args**是元组类型

    ```python
    def user_info(*args):
        print(args)
    
    user_info('leon', 18, 'man')
    ```

- 关键字传递

    参数是`key=value`的情况下，所有的`key=value`对都会被**kwargs**接收并组成字典

    ```python
    def user_information(**kwargs):
        print(kwargs)
    
    user_information(name="leon", age=18, gender='man')
    ```

### 匿名函数

如果一个函数使用简单的表达式就可以实现所需功能，那么就无需显式定义一个函数，lamdba 表达式可以返回一个没有名字的函数，也即匿名函数。

语法：`lambda para1, para2 : functional code`

```python
def test_function(compute):
    result = compute(1, 2)
    print(result)

test_function(lambda x, y : x + y)	# 3
```





















