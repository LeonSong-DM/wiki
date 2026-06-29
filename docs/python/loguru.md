# loguru 日志管理

!!! overview
    本文基于 Loguru 官方英文文档整理，面向 Python 开发者，结合常见业务场景讲解 Loguru 的核心能力与推荐用法。

## 1. Loguru 简介

`Loguru` 是一个开箱即用第三方 Python 日志库，它让日志记录这件事更简单、更好看、更容易维护。

Loguru 的设计思路是:

- 默认开箱即用
- 用一个全局 `logger` 覆盖大多数使用场景
- 让格式化、异常捕获、上下文绑定、日志轮转都更直观

下载：

```python
pip install loguru
```

导入方式：

```python
from loguru import logger
```



## 2. 快速开始

第一个例子:

```python
from loguru import logger

logger.info("Hello, Loguru!")
logger.warning("这是一条警告日志")
logger.error("这是一条错误日志")
```

运行后，你会直接在控制台看到格式化后的输出。Loguru 默认已经帮你添加了一个输出到标准错误流的 sink，所以很多时候你导入之后就能直接写日志。

如果你想完全自定义输出方式，通常会先移除默认 sink:

```python
import sys
from loguru import logger

logger.remove()
logger.add(sys.stderr, level="INFO")

logger.debug("这条不会输出")
logger.info("这条会输出")
```



## 3. 基本日志输出

Loguru 内置了常见日志级别，还额外提供了一个很实用的 `SUCCESS` 级别。

### 3.1 常见日志方法

按照日志级别从小到大排序：

```python
from loguru import logger

logger.trace("trace 级别，最细粒度")
logger.debug("debug 级别，调试信息")
logger.info("info 级别，正常运行信息")
logger.success("success 级别，表示操作成功")
logger.warning("warning 级别，表示警告")
logger.error("error 级别，表示错误")
logger.critical("critical 级别，严重错误")
```

### 3.2 推荐的字符串格式化方式

Loguru 的日志消息使用 `str.format()` 风格格式化:

```python
from loguru import logger

user_id = 1001
order_id = "ORD-20260316-001"

logger.info("用户 {} 创建了订单 {}", user_id, order_id)
logger.info("用户 {user_id} 创建了订单 {order_id}", user_id=user_id, order_id=order_id)
```

这比手动拼接字符串更清晰，也比提前写好 f-string 更适合日志场景。



## 4. 日志写入文件

把日志写入文件，是 Loguru 最常见的用法之一。核心方法就是 `logger.add()`。

```python
from loguru import logger

logger.remove()
logger.add("app.log", encoding="utf-8", level="INFO")

logger.info("服务启动成功")
logger.error("数据库连接失败")
logger.trace("不会输出")
```

!!! warning
    这里的 level 参数代表将指定级别以上的日志信息添加到文件中

### 4.1 同时输出到控制台和文件

```python
import sys
from loguru import logger

logger.remove()

logger.add(sys.stderr, level="INFO")
logger.add("app.log", encoding="utf-8", level="DEBUG")

logger.debug("这条只会写入文件")
logger.info("这条会同时输出到控制台和文件")
```

### 4.2 写成 JSON 日志

如果你的日志需要接入 ELK、Loki、Datadog 之类的平台，结构化输出会更方便:

```python
from loguru import logger

logger.remove()
logger.add("app.json", serialize=True)

logger.info("用户登录成功", user_id=1001)
```

`serialize=True` 会把日志记录序列化为 JSON 字符串，便于后续采集与分析。

## 5. 日志格式化

Loguru 的格式化能力很强，最常用的是 `format` 参数。

```python
import sys
from loguru import logger

logger.remove()
logger.add(
    sys.stderr,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level:<8} | {name}:{function}:{line} - {message}",
    level="DEBUG",
)

logger.info("格式化输出示例")
```

### 5.1 常见占位符

常见字段包括:

- `{time}`: 时间
- `{level}`: 日志级别
- `{message}`: 日志正文
- `{name}`: 模块名
- `{function}`: 函数名
- `{line}`: 行号
- `{extra[...]}`: 通过 `bind()` 或 `contextualize()` 绑定的上下文字段

### 5.2 彩色输出

Loguru 支持颜色标记:

```python
import sys
from loguru import logger

logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | <cyan>{message}</cyan>",
    colorize=True,
)

logger.warning("彩色日志输出")
```

控制台 sink 可以保留颜色，文件 sink 一般不建议保留颜色。

## 6. 日志级别

Loguru 默认内置的级别如下:

| 级别 | 数值 |
| --- | --- |
| `TRACE` | 5 |
| `DEBUG` | 10 |
| `INFO` | 20 |
| `SUCCESS` | 25 |
| `WARNING` | 30 |
| `ERROR` | 40 |
| `CRITICAL` | 50 |

### 6.1 为 sink 设置最低级别

```python
import sys
from loguru import logger

logger.remove()
logger.add(sys.stderr, level="WARNING")

logger.info("不会输出")
logger.warning("会输出")
logger.error("也会输出")
```

### 6.2 查看级别信息

```python
from loguru import logger

level = logger.level("ERROR")
print(level)
```

### 6.3 自定义级别

官方文档支持通过 `logger.level()` 添加自定义级别:

```python
from loguru import logger

logger.level("AUDIT", no=25, color="<cyan>", icon="*")
logger.log("AUDIT", "审计日志: 用户修改了权限")
```

注意一点: 自定义级别在记录时要用名字，比如 `logger.log("AUDIT", "...")`，而不是只传级别数值。



## 7. 日志轮转

日志文件不能无限增长，所以轮转非常重要。Loguru 在 `add()` 中直接提供了 `rotation` 参数。

官方文档说明，`rotation` 可以接受:

- 文件大小，例如 `100 MB`
- 时间间隔，例如 `1 day`
- 每日固定时间，例如 `00:00`
- `datetime.time`
- `datetime.timedelta`
- 自定义函数

### 7.1 按文件大小轮转

```python
from loguru import logger

logger.remove()
logger.add("size_rotation.log", rotation="100 MB", encoding="utf-8")

for i in range(1000):
    logger.info("第 {} 条日志", i)
```

### 7.2 按时间轮转

```python
from loguru import logger

logger.remove()
logger.add("time_rotation.log", rotation="00:00", encoding="utf-8")

logger.info("每天零点轮转日志")
```

### 7.3 路径中使用 `{time}`

```python
from loguru import logger

logger.remove()
logger.add("app_{time}.log", encoding="utf-8")
logger.info("日志文件名里带时间戳")
```

这在批处理任务里很方便，可以自然地区分每次执行生成的日志文件。



## 8. 日志保留

轮转之后，旧日志怎么清理？这就是 `retention` 的用途。

官方文档说明，`retention` 可以接受:

- 整数: 保留最近多少个文件
- 时间长度: 保留多长时间内的文件
- 人类可读字符串，例如 `2 months`
- 自定义函数

### 8.1 保留最近 10 个文件

```python
from loguru import logger

logger.remove()
logger.add(
    "retention_count.log",
    rotation="100 MB",
    retention=10,
    encoding="utf-8",
)
```

### 8.2 保留 30 天

```python
from loguru import logger

logger.remove()
logger.add(
    "retention_days.log",
    rotation="1 day",
    retention="30 days",
    encoding="utf-8",
)
```

如果没有保留策略，日志长期运行后很容易把磁盘写满。



## 9. 日志压缩

Loguru 支持在日志轮转或 sink 结束时自动压缩旧日志，这个能力由 `compression` 提供。

官方文档给出的压缩格式包括:

- `gz`
- `bz2`
- `xz`
- `lzma`
- `tar`
- `tar.gz`
- `tar.bz2`
- `tar.xz`
- `zip`

### 9.1 自动压缩为 zip

```python
from loguru import logger

logger.remove()
logger.add(
    "archive.log",
    rotation="100 MB",
    retention="14 days",
    compression="zip",
    encoding="utf-8",
)

logger.info("旧日志会在轮转后自动压缩")
```

这在服务器环境里很实用，既能保留历史日志，又能节省空间。

## 10. 捕获异常

Loguru 在异常日志方面明显优于很多默认配置下的 `logging` 用法。

### 10.1 使用 logger.exception()

当你已经处于 `except` 块中时，可以直接记录异常:

```python
from loguru import logger

def divide(a, b):
    return a / b

try:
    divide(10, 0)
except ZeroDivisionError:
    logger.exception("计算失败")
```

### 10.2 使用 @logger.catch

这是 Loguru 很有代表性的特性。官方文档说明，`catch()` 既可以当装饰器，也可以当上下文管理器。

```python
from loguru import logger

@logger.catch
def parse_number(text):
    return int(text)

parse_number("abc")
```

### 10.3 控制是否继续抛出异常

```python
from loguru import logger

@logger.catch(reraise=True)
def risky():
    raise RuntimeError("任务失败")

try:
    risky()
except RuntimeError:
    print("异常继续向上抛出了")
```

### 10.4 作为上下文管理器使用

```python
from loguru import logger

with logger.catch(message="执行主流程时发生异常"):
    result = 10 / 0
```

### 10.5 backtrace 和 diagnose

`logger.add()` 里还有两个和异常相关的重要参数:

- `backtrace=True`: 异常回溯可以向上扩展，帮助定位真正调用链
- `diagnose=True`: 在异常展示中输出更多变量值，便于调试

开发环境里这两个参数很有帮助，但官方文档明确建议: **生产环境应考虑把 `diagnose=False`**，避免敏感数据泄露。

```python
from loguru import logger

logger.remove()
logger.add("error.log", backtrace=True, diagnose=False, encoding="utf-8")
```



## 11. 自定义 sink

在 Loguru 里，sink 可以理解为“日志最终流向哪里”。

官方文档说明，sink 可以是:

- 文件对象
- 文件路径
- 普通函数
- 协程函数
- `logging.Handler`

### 11.1 使用函数作为 sink

```python
from loguru import logger

alerts = []

def alert_sink(message):
    record = message.record
    alerts.append(
        {
            "time": record["time"].isoformat(),
            "level": record["level"].name,
            "message": record["message"],
        }
    )

logger.remove()
logger.add(alert_sink, level="ERROR")

logger.error("支付回调失败")
logger.critical("数据库不可用")

print(alerts)
```

这个例子里，日志没有写到文件，而是进入了一个内存列表。你也可以把它改造成:

- 发 HTTP 请求到告警系统
- 写入 Kafka
- 推送到消息队列
- 发邮件或企业微信通知

### 11.2 协程 sink

如果你在异步项目里写日志，可以使用协程 sink。根据官方文档，异步场景结束前可以调用 `await logger.complete()`，确保日志处理完成。

```python
import asyncio
from loguru import logger

async def async_sink(message):
    await asyncio.sleep(0.1)
    print("ASYNC:", message, end="")

async def main():
    logger.remove()
    logger.add(async_sink)
    logger.info("异步日志消息")
    await logger.complete()

asyncio.run(main())
```



## 12. bind 和 context

这部分是 Loguru 在“上下文日志”方面最实用的能力。

很多业务日志不只是打印一句话，还需要带上:

- 用户 ID
- 请求 ID
- 订单号
- 机器编号
- 租户 ID

这时 `bind()` 和 `contextualize()` 就非常好用。

### 12.1 `bind()`: 返回一个带上下文的新 logger

```python
import sys
from loguru import logger

logger.remove()
logger.add(
    sys.stderr,
    format="{extra[request_id]} | {message}",
)

request_logger = logger.bind(request_id="req-1001")
request_logger.info("开始处理请求")
request_logger.info("请求处理完成")
```

`bind()` 的特点是:

- 返回一个新的 logger 对象
- 适合绑定固定上下文
- 很适合放在类实例、请求对象、任务对象里

### 13.2 contextualize(): 在代码块内临时绑定上下文

官方文档特别提到，`contextualize()` 基于 `contextvars`，因此在线程和异步任务里都能保持上下文隔离。

```python
import sys
from loguru import logger

logger.remove()
logger.configure(extra={"request_id": "-"})
logger.add(sys.stderr, format="{extra[request_id]} | {message}")

logger.info("进入系统")

with logger.contextualize(request_id="req-2002"):
    logger.info("查询商品信息")
    logger.info("创建订单")

logger.info("离开上下文")
```

### 12.3 bind() 和 contextualize() 怎么选

简单理解:

- `bind()` 适合“这个 logger 以后都带这个字段”
- `contextualize()` 适合“这段代码执行期间临时带这个字段”

在 Web 场景里，通常可以这样用:

- 请求进入时用 `contextualize(request_id=...)`
- 某个服务对象内部用 `bind(service="payment")`


