# 复习：

# - `try/except`
# - 捕获具体异常
# - `else`
# - `finally`
# - `raise`
# - 自定义异常


class AssertionFailedError(Exception):
    pass


def assert_status(actual: int, expected: int) -> None:
    if actual != expected:
        raise AssertionFailedError(
            f"状态码断言失败：预期{expected}，实际{actual}"
        )



# - `try/except`
def run_one_case(actual: int,expected: int) -> None:
    try:
        assert_status(actual, expected)
    except AssertionFailedError as e:
        print(f"用例失败: {e}")
    else:
        print("用例通过")
    finally:
        print("用例执行完毕")

# - 捕获具体异常
try:
    token = test_case["headers"]["Authorization"]
except KeyError as e:
    print(f"字段缺失 : {e}")
except TypeError as e:
    print(f"类型错误 : {e}:")


# ... existing code ...
class APIError(Exception):
    """所有接口测试异常的基类"""
    pass


class NetworkError(APIError):
    """网络异常：连接失败、超时等，可重试"""
    pass


class AssertionFailedError(APIError):
    """断言失败：实际结果与预期不符"""
    pass


class BusinessError(APIError):
    """业务异常：业务规则不满足"""
    pass


# 重点区分：

# - 系统异常
# - 网络异常
# - 参数错误
# - 业务异常
# - 断言失败