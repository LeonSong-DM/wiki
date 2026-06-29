import sys
from loguru import logger

"""
# 移除默认 sink
logger.remove()
# 添加自定义 sink
logger.add(sys.stderr, level="INFO")

logger.debug("debug message")
logger.info("info message")

logger.add(sys.stderr, level="DEBUG")
logger.debug("debug message")
"""

# loguru 提供的日志级别
logger.trace("trace 级别，最细粒度")
logger.debug("debug 级别，调试信息")
logger.info("info 级别，正常运行信息")
logger.success("success 级别，表示操作成功")
logger.warning("warning 级别，表示警告")
logger.error("error 级别，表示错误")
logger.critical("critical 级别，严重错误")

# 字符串格式化
user_id = 1001
order_id = "ORD-20260626-001"
logger.info("用户 {} 创建了订单 {}", user_id, order_id)

"""
# 日志写入文件
logger.remove()
logger.add("app.log", encoding="utf-8", level="INFO")

logger.info("This message will writed to app.log file.")
logger.error("something wrong.")
"""

# 写入文件并同时打印到控制台
logger.remove()

logger.add(sys.stderr, level="INFO")
logger.add("app.log", level="INFO")

logger.info("info message")
logger.error("error message")


logger.remove()

logger.add(sys.stderr, level="INFO")
logger.info("info msg")
logger.error("error msg")
logger.trace("hello")


# 写成 json 日志
logger.remove()
logger.add("log.json", serialize=True)
logger.info("用户登录成功", user_id)

# 定义 json 日志的格式

# 日志格式化
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss:ms}</green> | {name}:{line} | {message}",
    level="INFO",
)
logger.info("Hello")

# 查看级别信息
level = logger.level("INFO")
logger.info(level)

"""
# 添加自定义级别
logger.level("AUDIT", no=25, color="<bold>", icon="*")
logger.log("AUDIT", "审计日志")

logger.remove()
logger.add("app.log", level="INFO", rotation="1 MB", encoding="utf8", retention=1)
while True:
    logger.info("This is log info")
"""

logger.remove()
logger.add(sys.stderr, level="INFO")

# 捕获异常
try:
    a = 1 / 0
except Exception as e:
    logger.exception(e)


@logger.catch
def parse_number(text):
    return int(text)


parse_number("abc")

with logger.catch(message="error message"):
    a = 1 / 0
