---
tags:
    - Python
    - SQLAlchemy
    - ORM
    - DataBase
---

# SQLAlchemy ORM



## 初识 SQLAlchemy

SQLAlchemy是一个数据库工具库,**允许开发者用Python操作关系型数据库**(如MySQL, PostgreSQL, SQLite...), 是传统数据库操作的一种抽象形式

它的内核由 **SQLAlchemy Core 和 SQLAlchemy ORM** 两部分组成,Core层是SQLAlchemy的基础模块, 其核心作用是**使用Python构建SQL语法树(SQL Expression Language)**, 并编译为可执行的SQL语句

ORM (Object Relational Mapper) 构建在CORE的基础上, **它将数据库表映射为Python类, 将表中的记录映射为对象实例, 实现Python对象与数据之间的相互转换;** 借助SQLAlchemy ORM可以用声明Python对象的方式建表, 通过操作Python对象, 实现数据库的增删改查等一系列操作


---


## 通过ORM建表


### 声明模型
通过声明式映射的结构, 允许我们创建Python类去描述数据库表的结构. 基本流程一般包括:

 - 创建数据库引擎
 - 定义基类Base (继承自sqlalchemy.orm.DeclarativeBase)
 - 定义模型类
 - 调用`Base.metadata.create_all(engine)`创建表

如果声明一个名为`user_table`的表, 包含`id`, `name`, `age`三个字段:
``` python
from sqlalchemy import String, Integer
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user_table"

    id: Mapped[int] = mapped_column("user_id", Integer, primary_key=True)
    name: Mapped[str] = mapped_column("user_name", String(30))
    age: Mapped[int] = mapped_column("user_age", Integer)

    # 为了便于调试
    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, age={self.age})"
```

!!! note
    - 每个数据表都至少声明一列作为主键
    -  如果在Base中定义字段, 这些字段会被所有继承自Base的模型类自动继承, 并在对应的数据表中生成相应的列


在SQLAlchemy 2.X版本中有 **类型推断** 和 **列名推断** 的特性, 可以从 `Mapped[]` 信息中自动推断出这些数据, 也就是说如果你没有其他的额外要求, 声明字段的时候可以省略 `mapped_column()`方法, 在这个例子中, 可以把 `age` 字段改写为:
```python
age: Mapped[int]
```
SQLAlchemy可以推断出以下信息:

 - age是一个映射字段
 - 列名: age
 - 类型: Integer

如果SQLAlchemy的自动推断无法满足你的需求, 就必须在`mapped_column()`中声明你的约束条件
<br>


!!! question "为什么要定义基类Base, 它为什么要继承 DeclarativeBase 类"

    Base需要管理自定义的所有模型类,就像三省六部制最终都要归到皇上那里去决策,Base类会收集所有模型类的元数据(metadata)并保存在 `Base.metadata`中, 元数据中存储了所有表的结构信息(表名, 字段, 类型, 约束...) 

    继承`DeclarativeBase` 是因为它提供了ORM映射的"声明式能力", 上文提到Base类会收集所有模型类的元数据, 它的收集能力就源自`DeclatativeBase`, 它不止做了这一件事情:

    - 读取 `__tablename__`
    - 解析 `mapped_column`
    - 构建Table对象
    - 注册到metadata
    - 建立ORM映射

!!! question "Mapped和mapped_column的作用"

    - Mapped: 告诉ORM这是一个被映射的属性
    - mapped_column: 告诉ORM如何映射到数据列

以 `id` 为例, `Mapped` 表示这是一个ORM字段, 它的Python类型是 `int`; 
对于 `mapped_column`, 这表示映射到数据库 (实际上是映射到Core Column), `id` 会映射到数据库表中的列`user_id`, 并声明该字段为主键且为 `Integer` 类型;

API文档参考: 📑  [mapped_column](https://docs.sqlalchemy.org.cn/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column)

---

### 创建引擎
<u>*为了方便并与官方文档保持一致性, 本文所有操作基于SQLite内存数据库进行演示*</u>

引擎是一个`Engine对象`,它充当特定数据库连接的中心来源(**只创建一次的全局对象**), 由一个URL字符串进行配置, 该字符串会描述如何连接到数据库主机.

```python
from sqlalchemy import create_engine

engine = create_engine(
    "sqlite+pysqlite:///:memory:",
    echo=True
)
```

### create_engine详解
*API文档参考:*  📑 [create_engine](https://docs.sqlalchemy.org.cn/en/20/core/engines.html#sqlalchemy.create_engine)

```python
function sqlalchemy.create_engine(url: str | _url.URL, **kwargs: Any) → Engine
```


**参数**

|  Param             | Description                                               |
|--------------------|-----------------------------------------------------------|
| echo               | 是否将执行的 SQL 语句输出到控制台(用于调试), 生产场景慎用 |
| pool_size          | 连接池中常驻的连接数量                                    |
| max_overflow       | 超出 `pool_size` 后允许创建的临时连接数量                 |
| pool_timeout       | 获取连接的最大等待时间（秒），超时会抛出异常              |
| pool_pre_ping      | 每次使用连接前进行一次有效性检测，防止连接失效            |
| pool_recycle       | 连接在指定时间（秒）后自动重建，常用于避免数据库断连问题  |

<br>

**url组成部分**

```
dialect+driver_name://username:password@host:port/database
```

|  Param        | Description |
|--------------------|------------|
| dialect            | SQLAlchemy dialect的标识名称如 `sqlite`, `mysql`, `postgresql`...|
| driver_name        | 该数据库对应DBAPI的名称,全小写字母 |
| username           | 用于连接数据库帐号的用户名|
| password           | 用于连接数据库帐号的用户密码|
| host               |  数据库主机地址|
| port               | 数据库主机端口 |
| database           | 目标数据库名称 |

以MySQL数据库为例:
```
mysql+pymysql://username:password@localhost:3306/my_database
```

<br>

**创建URL对象**

值得注意的是, 如果数据服务运行在目标主机的默认端口, 可以省略`port`参数

```python
from sqlalchemy.engine import URL
url = URL.create(
    drivername = "mysql+pymysql",
    username = "user",
    password = "passwd",
    host = "localhost"
    port = 3306,    
    database = "database"
)
```

------



### Create Table

调用元数据对象的`create_all()`方法并指定`engine`对象即可根据已定义的模型类在目标数据库中创建相应的表结构
```python
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column
)
from sqlalchemy import create_engine, String, Integer

DATABASE_URL =  "sqlite://"

engine = create_engine(
    DATABASE_URL,
    echo=True
)

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_table"

    id: Mapped[int] = mapped_column("user_id", Integer, primary_key=True)
    name: Mapped[str] = mapped_column("user_name", String(30))
    age: Mapped[int] = mapped_column("user_age", Integer)

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, age={self.age})"
    
Base.metadata.create_all(engine)

```

------



### 官方示例

上文已经介绍了如何定义模型类, 创建数据库引擎以及建表的流程, 因为示例过于简单, 现在回到官方给出的表结构重新建表
```Python
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship
)

from sqlalchemy import (
    String,
    ForeignKey,
    create_engine
)

url = "sqlite+pysqlite:///:memory:"

engine = create_engine(
    url=url,
    echo=True
)

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[str | None]

    addresses: Mapped[list["Address"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"User(id:{self.id!r}, name={self.name!r}, full_name={self.full_name!r})"
    
class Address(Base):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))

    user: Mapped["User"] = relationship(back_populates="addresses")

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, emil_addres{self.email_address!r})"
    

if __name__  == "__main__":
    Base.metadata.create_all(engine)
```

### relationship
User类和Address类中出现了`relationship()`, 它是SQLAlchemy ORM中的一个关系API, 这个属性不再代表表中的一个字段, 它用于提供两个模型类之间的关系, 在Python对象之间建立关联, 并不会在数据表中创建任何列:
 - User.address 将 User 对象链接到多个 Address 对象 (一对多)
 - Address.user 将 Address 对象关联到对应的 User 对象 (多对一)

不难看出, User对象的addresses属性是根据其`user.id`在表`address`中查询的结果, `address`表中存储的是每个用户的`email_address`且同一用户可能存在多个`email_address`, 这个概念或许过于抽象, 具体参见 📑 [关系配置](https://docs.sqlalchemy.org.cn/en/20/core/engines.html#sqlalchemy.create_engine)

------



## 通过Session与数据库交互

上文已经完成了建表的操作, 下面介绍如何通过 `Session` (会话)与数据库进行交互, `Session`是 SQLAlchemy ORM 中与数据库交互的核心对象, 可以将其理解为一次数据库操作的上下文或工作单元, 它主要负责:

 - 管理对象与数据库之间的映射关系
 - 跟踪对象的状态变化
 - 控制事物的提交与回滚
 - 通过底层的 `Engine` 与数据库建立连接并执行 SQL 

当前主要介绍如何通过 `Session` 对象执行数据库的增删改查操作, 在此之前, 需要了解 Python 的上下文机制:

学习Python文件操作时, 使用过 `with` 语句, 它是 Python 用来管理上下文的语法, **用于自动管理资源的创建和释放**, 那时候只知道使用 `with open()` 可以创建一个文件对象, 在执行完文件操作后不用手动关闭文件, 并且也只有在上下文的范围内可以对该对象进行操作. 

其实, 上下文指的就是执行对象操作时所依赖的环境状态, 这些对象一般都具有生命周期, 不能被程序长时间的占用, 例如:

 - 文件 : 文件描述符(FD)泄露, 打开文件数打到系统上限导致程序崩溃
 - 数据库连接 : 连接池耗尽导致新请求拿不到连接, 请求超时
 - 网络连接 : `TCP` 连接占用导致端口耗尽
 - 锁 : 其他线程拿不到锁, 导致死锁, 程序卡死
 - 事物 : 事物不提交将一直处于未完成状态


### 插入数据
插入数据在 ORM 层可以总结为四个过程:
 - 创建 `Session()` 会话
 - 创建模型类对象
 - 添加对象
 - 提交事务

```python
from sqlalchemy.orm import Session

with Session(engine) as session:
    # 声明对象
    spongebob = User(
        name="spongebob",
        fullname="Spongebob Squarepants",
        addresses=[
            Address(email_address="spongebob@sqlalchemy.org"),
            Address(email_address="spongebob@sqlalchemy.org"),
            Address(email_address="spongebob@sqlalchemy.org")
        ]
    )

    sandy = User(
        name="sandy",
        fullname="Sandy Cheeks",
        addresses=[
            Address(email_address="sandy@sqlalchemy.org"),
            Address(email_address="sandy@squirrelpower.org"),
        ],
    )

    patrick = User(name="patrick", fullname="Patrick Star")

    # 添加对象
    session.add_all([spongebob, sandy, patrick])


    # 查询
    result = session.execute(Select(User))
    for row in result.scalars():
        print(row)

    """ output
    User(id:1, name='spongebob', full_name='Spongebob Squarepants')
    User(id:2, name='sandy', full_name='Sandy Cheeks')
    User(id:3, name='patrick', full_name='Patrick Star')
    """

    # 提交事务
    session.commit()
```

添加对象后**不会立即提交事务**, 这些对象目前是**挂起状态**, 可以看到我在提交事务前加了一个查询语句用于查询 User 表中的所有内容, 会有人有疑问, 为什么添加对象后处于挂起状态却可以从数据库查询出这些挂起的数据, 挂起的含义实际上是把对象放进 Session 会话中进行管理, 而 Session 会自动进行 `flush()`, 它的作用是**把数据操作提交给数据库, 但是不提交事务.**

所以在当前 `Session` 会话中表现出在 `commit` 之前数据就已经存在于数据库, 但是在外界看来数据库其实没有变化
我们可以在创建上下文时指定参数 `autoflush=False` 以关闭自动 `flush`, 此时再执行就看不到刚才插入的数据



------



### 简单查询

在上一节中我放入了一个查询语句以供展示 `flush` 的作用, 实际上在 SQLAlchemy ORM 中的标准写法应为:
``` python
from sqlalchemy import select

result = session.execute(select(User))

print("-"*100)
print(type(result)) # <class 'sqlalchemy.engine.result.ChunkedIteratorResult'>
print("-"*100)

for row in result.scalars():
    print(row)
```
初学者很难发现其中的异同, 下面以标准写法讲解查询数据的流程:

执行查询需要使用 `select()` 函数创建一个 `Select` 对象然后通过 `Session` 对象调用它.  `select(User)` 会**生成一个 SQL 表达式对象**, 可以理解为翻译的角色, 但这只是 "翻译" 的一部分, `session.execute(sql_obj)` 会把这个**SQL 表达式对象编译成标准的 SQL 语句**, 通过数据库引擎 `Engine` 对象在**数据库连接池中获取一个连接并发送给数据库执行, 最后返回一个 `Result` 对象 (迭代器)**, 它里面封装了数据库返回的行数据和一些处理方法.

!!! question "为什么使用 `Select()` 也可以完成查询操作"

    `select()` 和 `Select()` 都会创建一个 Select 对象, 前者是 Select 类中专门用于创建 Select 对象的构造器,负责参数规范化, 表达式构建以及兼容性处理从而保证生成的查询对象在语义上的正确性与稳定性;  

    而后者仅通过 `__init__()` 完成一个 `Select` 对象的简单初始化, 它是底层接口, 只负责构造对象本身, 并不对参数进行完整的语义处理, 所以在生产环境下优先使用 `select()` 方法构造 `Select` 对象



#### 从 Result 对象中取出数据
`Result`对象可以理解为一个数据容器, 它提供了三种视图访问查询出的数据:

 - Row
 - Scalar (译 : 标量)
 - Mapping

##### Row视图

| method | description |
| ------ | ----------- |
| 直接遍历|  返回ROW对象  |
| `result.all()`  | 获取ROW对象列表|
|  `result.first()` | 返回第一个ROW对象或None |
| `result.one()`     | 必须只返回一个ROW对象 |
| `result.one_or_none()` | 要么一个ROW对象, 要么为None |



**直接遍历 Result** 

```python
result = session.execute(select(User))

# 直接遍历
for row in result:
    print(row)

""" output
(User(id:1, name='spongebob', full_name='Spongebob Squarepants'),)
(User(id:2, name='sandy', full_name='Sandy Cheeks'),)
(User(id:3, name='patrick', full_name='Patrick Star'),)
"""
```
可以看到, 每一个 `ROW` 对象都是一个元组, SQLAlchemy 会把每一个行数据映射为当前模型类的实例, 所以会返回对象的形式

!!! note
    
    不要忘记Python用 `(a,)` 这种方式声明单元素元组哦哈哈哈


如果只查询 `User` 表中的 `name` 与 `fullname` 字段:
``` python
result = session.execute(select(User.name, User.fullname))

for row in result:
    print(row)

"""output
('spongebob', 1)
('sandy', 2)
('patrick', 3)
"""
```

**获取 ROW 列表**

```python
result = session.execute(Select(User))
print("\n".join(f"- {x}" for x in result.all()))
```

**获取第一个 ROW 对象**

```python
result = session.execute(Select(User))
print(result.first())

""" output
(User(id:1, name='spongebob', full_name='Spongebob Squarepants'),)
"""
```

**必须只获取一个 ROW 对象**

```python
result = session.execute(select(User))
print(result.one())

"""output
raise exc.MultipleResultsFound(
sqlalchemy.exc.MultipleResultsFound: Multiple rows were found when exactly one was required
"""
```

**获取一或零个 ROW 对象**

```python
result = session.execute(Select(User).where(User.id > 10))
print(result.one_or_none())

"""output
None
"""
```



##### Scalar视图

Scalar视图的核心思想是**从每一行 `ROW` 提取“第一列”数据并以扁平形式返回**， 先回到 `ROW` 视图：

```python
# 查询所有User

""" output
(User(id:1, name='spongebob', full_name='Spongebob Squarepants'),)
(User(id:2, name='sandy', full_name='Sandy Cheeks'),)
(User(id:3, name='patrick', full_name='Patrick Star'),)
"""

# 查询User中的 name
"""output
('spongebob',)
('sandy',)
('patrick',)
"""
```

当我们的查询**只关注一个 ORM 模型或者一个字段值时**，`Result`的默认`行 Row` 视图总是会返回元组 `(a, )`的格式的数据，这是 SQLAlchemy 为了保证查询结果结构的一致性所做出的举措

**所谓扁平化，即我们可以直接从 `行 Row` 结构提取出实际需要的值， 去除外层的元组包装**

**常用方法**

| Method                        | Description                        |
| ----------------------------- | ---------------------------------- |
| `result.scalars()`            | 返回一个可迭代对象                 |
| `result.scalars().all()`      | 返回结果列表                       |
| `result.scalar()`             | 返回第一行的第一列，无数据返回None |
| `result.scalar_one()`         | 只能返回一条数据                   |
| `result.scalar_one_or_none()` | 最多返回一条数据， 无数据返回None  |



**💻 代码实现**

```python
-----------------------------------------------------------------------------------------
# scalars()
result = session.execute(Select(User.name))

res = result.scalars()

for row in res:
    print(row)

""" output
spongebob
sandy
patrick
"""
-----------------------------------------------------------------------------------------

# scalars.all()
result = session.execute(Select(User))
res = result.scalars().all()
print("\n".join(f"- {x}" for x in res))

""" output
- User(id:1, name='spongebob', full_name='Spongebob Squarepants')
- User(id:2, name='sandy', full_name='Sandy Cheeks')
- User(id:3, name='patrick', full_name='Patrick Star')
"""
-----------------------------------------------------------------------------------------

# scalar()
result = session.execute(Select(User))
res = result.scalar()
print(res)

""" output
User(id:1, name='spongebob', full_name='Spongebob Squarepants')
"""
-----------------------------------------------------------------------------------------

# scalar_one()
result = session.execute(Select(User))
try:
    res = result.scalar_one()
    print(res)
except Exception as e:
    print(e)
    
""" output
Multiple rows were found when exactly one was required
"""
-----------------------------------------------------------------------------------------
# scalar_one_or_none() 
# ...
-----------------------------------------------------------------------------------------
```



##### Mapping视图

Mapping视图很好理解，它用于**将每一行数据转换为字典的形式，以 “键值对” 的形式访问列数据**， 以拓展可读性以及对象操作的便利性

```
Row：
(1, "spongebob")

Mapping：
{
	"id" : 1,
	"name": "spongebob"
}
```

| Method                    | Description                                  |
| ------------------------- | -------------------------------------------- |
| `result.mappings()`       | 返回 MappingResult，可逐行以字典形式访问数据 |
| `result.mappings().all()` | 返回所有结果，类型为 `list[dict]`            |
| `result.mappings.first()` | 返回第一条记录（`dict`）或 `None`            |

!!! info
    
    本节不再添加代码演示喽



------



#### 条件查询

条件查询在 MySQL 中以 `where` 子句的形式实现, 相似地，在 SQLAlchemy ORM 中使用 `where()`方法实现条件查询

**基本用法**

查询 `id = 2` 的用户信息

```python
result = session.execute(select(User).where(User.id == 1))

""" output
User(id:1, name='spongebob', full_name='Spongebob Squarepants')
"""
```

**常见的条件运算符**

| Operator            | Description                                                  |
| ------------------- | ------------------------------------------------------------ |
| `==` / `!=`         | ...                                                          |
| `>` `>=` / `<` `<=` | ...                                                          |
| `like`              | 模糊查询，有参数 `%` 和 `_` 分别代表匹配**任意**个字符和**单个字符** |
| `in_`               | 判断值是否在指定的集合中， 对应 SQL 中的 `in`， 反之也存在`notin_` |
| `is_`               | 判断是否为 NULL， 对应 SQL 中的 `IS NULL`, 反之也存在 `is_not` |

**💻 代码实现**

```python
# like
result = session.execute(Select(User).where(User.name.like("_an%")))
        
for res in result.scalars():
    print(res)

""" output
User(id:2, name='sandy', full_name='Sandy Cheeks')
"""


# in
result = session.execute(Select(User).where(User.name.in_(["sandy", "patrick"])))
""" output
User(id:2, name='sandy', full_name='Sandy Cheeks')
User(id:3, name='patrick', full_name='Patrick Star')
"""

# is_not
result = session.execute(Select(User).where(User.name.is_not(None)))
""" output
User(id:1, name='spongebob', full_name='Spongebob Squarepants')
User(id:2, name='sandy', full_name='Sandy Cheeks')
User(id:3, name='patrick', full_name='Patrick Star')
"""
```



**多条件查询**

实际开发中查询工作一般都有多个条件约束，使用 SQLAlchemy ORM 进行多条件查询有不同风格的写法，以 `id > 1 && name like ("%andy")` 为例：



**隐式 AND**

多个查询条件作为 `where` 方法的参数并用 `,` 分割，也最符合 SQLAlchemy ORM 风格

```python
result = session.execute(Select(User).where(User.id > 1, User.name.like("%andy")))

for res in result.scalars():
    print(res)

""" output
User(id:2, name='sandy', full_name='Sandy Cheeks')
"""
```



**显式组合条件**

使用 `sqlalchemy.and_` ， `sqlalchemy.or_`  和 `sqlalchemy.not_` 显示的构建多个条件之间的逻辑关系

```python
from sqlalchemy import (
	and_,
	or_,
	not_
)
```

逻辑与

```python
result = session.execute(Select(User).where(
    and_(
        User.id > 1,
        User.name.like("%andy")
    )
))
```

逻辑或

```python
result = session.execute(Select(User).where(
    or_(
        User.id > 1,
        User.name.like("%andy")
    )
))
```



逻辑非

不接受多个参数？

```python
result = session.execute(Select(User).where(
    and_(
        not_(User.id > 1),
        not_(User.name.like("%andy"))
    )
))
```



同样的，也可以在 `where()` 方法中通过运算符 `&` `|`的形式来构建不同条件之间的逻辑关系， **前提是使用元素符表示时需要用括号包裹每个条件**

!!! warning
    
    这些逻辑运算并不是 Python 中的逻辑运算符， 只用于生成 SQL 的逻辑结构

```python
# 逻辑与
result = session.execute(Select(User).where(
    (User.id > 1) & (User.name.like("%andy"))
))


# 逻辑或
result = session.execute(Select(User).where(
    (User.id > 1) | (User.name.like("%andy"))
))
```

**链式写法**

通过链式调用  `where` 语句的方式拼接多个查询条件

```python
result = session.execute(Select(User)
                         .where(User.id > 1)
                         .where(User.name.like("%andy"))
                    )
```

------



#### 聚合查询

在 SQL 中通常使用聚合函数如`COUNT`, `SUM` 和 `AVG`等实现聚合查询， 在 SQLAlchemy 中通过 SQL 函数生成器 `func` 构建数据库函数调用表达式来实现， 它不仅限于聚合操作， 也不真正的实现计算，只构建 SQL 表达式

常用方法

| Method         | Description |
| -------------- | ----------- |
| `func.count()` | 计数        |
| `func.sum()`   | 求和        |
| `func.avg()`   | 取平均值    |
| `func.max()`   | 最大值      |
| `func.min()`   | 最小值      |

**💻 代码实现**

```python
from sqlalchemy import func_
result = session.execute(select(func.count(User.id)))
```

------



#### 连接查询

实际生产环境中， 数据总是遍布多张表，需要通过连接查询将多张表的数据进行关联从而完成数据库操作，连接查询实际上就是根据多表之间的连接关系将数据进行组合查询， 下面以：

```
查询邮箱地址为spongebob@sqlalchemy.org的用户名称
```

为例：

在 SQL 中， 通常使用 `JOIN...ON` 语句实现：

```sql
SELECT user_account.name 
FROM user_account
JOIN address on user_account.id = address.user_id
WHERE address.emil_address = "spongebob@sqlalchemy.org"
```

在 SQLAlchemy 中使用 `join(target_table, connect_condition)`

- `tatget_table`: 目标表
- `connect_condtion`: 连接条件

```python
result = session.execute(select(User)
                             .join(Address, User.id == Address.user_id )
                             .where(Address.email_address == "spongebob@sqlalchemy.org")
                            )
```

**基于`relationship`实现：**
在建表时， 我们通过 `relationship` 已经声明了 `User` 和 `Address` 两个模型类的连接关系，在进行 `join`时， SQLAlchemy 会读取 `relationship` 的配置并找到该表的外键自动生成连接条件

```pyhton
result = session.execute(select(User)
                             .join(Address)
                             .where(Address.email_address == "spongebob@sqlalchemy.org")
                            )
```



#### 分页查询

分页查询经常在在渲染数据时使用， 一般包含两个参数：

- `offset` : 跳过的数据量
- `limit` ：最多返回数据量 

> **offset** n. 译：偏移量

因为官方示例数据很少， 我们假设跳过2条数据， 最多返回3条数据， 在 `Addre` 查询所有数据，以下是 SQL 实现：
``` sql
SELECT *
FROM address
LIMIT 3 OFFSET 2
```

SQLAlchemy 通过 `limit(int)` 和 `offset(int)` 实现分页操作
```python
result = session.execute(select(Address).limit(3).offset(2))

""" output
Address(id=3, emil_addres='spongebob@sqlalchemy.org', user_id=1)
Address(id=4, emil_addres='sandy@sqlalchemy.org', user_id=2)
Address(id=5, emil_addres='sandy@squirrelpower.org', user_id=2)
"""
```




### 更新 & 删除数据

更新和删除数据也是 CRUD 操作的重要组成部分， 在 SQLAlchemy ORM 中， 可以通过修改 ORM 对象和 `update()` 方法两种方式完成数据的更新， 修改 ORM 对象的方式需要先获得目标对象 `get(model_class, primary_key)` 再对其属性进行修改:
``` python
user = session.get(User, 1)
user.name = "Leon"

result = session.execute(select(User))

for res in result.scalars():
    print(res)
 
"""output
User(id:1, name='Leon', full_name='Spongebob Squarepants')
User(id:2, name='sandy', full_name='Sandy Cheeks')
User(id:3, name='patrick', full_name='Patrick Star')
"""
```

`update()` 与 `select()` 相似， 它的作用是生成响应的 SQL 更新语句作为 `session.execute()` 的参数：

```python
session.execute(
    update(User)
    .where(User.id == 1)
    .values(name="Leon")
)

""" output
User(id:1, name='Leon', full_name='Spongebob Squarepants')
User(id:2, name='sandy', full_name='Sandy Cheeks')
User(id:3, name='patrick', full_name='Patrick Star')
"""
```

同样地， 删除对象既可以通过 删除 ORM 对象的方式（与通过操作ORM对象更新数据相似， 都需要先获取目标对象）和 `delete` 语句实现
```python
# orm
user = session.get(User, 1)
session.delete(user)

""" output
User(id:2, name='sandy', full_name='Sandy Cheeks')
User(id:3, name='patrick', full_name='Patrick Star')
"""



# delete
session.execute(
    delete(User)
    .where(User.id == 1)
)

""" output
User(id:2, name='sandy', full_name='Sandy Cheeks')
User(id:3, name='patrick', full_name='Patrick Star')
"""
```









