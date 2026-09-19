# 复习：

# - 参数
# - 返回值
# - 默认参数
# - 关键字参数
# - 类型注解
# - `list[dict]`
# - `dict[str, str]`
# - `str | None`



def assert_status(
    actual_status: int,
    expected_status: int = 200,
) -> bool:
    return actual_status == expected_status
print(assert_status(201, 201))



# assert_status()
# assert_response_time()
# 校验响应时间
def assert_response_time(actual_time: int, max_time: int = 1000) -> bool:
    return actual_time <= max_time
print(assert_response_time(500, 1000))


# calculate_pass_rate()
def calculate_pass_rate(passed: int,total: int) -> float:
    if total == 0:
        return 0.0
    return passed / total
print(calculate_pass_rate(10, 10))

# format_test_result()
def format_test_result(name: str,passed: bool,status_code: int) ->str:
    if passed:
        result = "Passed"
    else:
        result = "Failed"
    return f"[{result}] {name} (状态码 : {status_code})"

print(format_test_result("用例1", True, 200))
