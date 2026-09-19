# assertions.py：断言工具模块
# 一个模块就是一个 .py 文件，把同类功能放在一起


def assert_status(actual: int, expected: int) -> bool:
    """校验状态码"""
    return actual == expected


def assert_response_time(actual_ms: int, max_ms: int) -> bool:
    """校验响应时间不超过上限"""
    return actual_ms <= max_ms

def assert_all(checks: list[bool]) -> bool:
    """所有断言都通过才算通过"""
    return all(checks)
