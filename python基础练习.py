test_case = {
    "id": 1,
    "name": "查询用户",
    "method": "GET",
    "url": "https://example.com/users/1",
    "headers": {
        "Authorization": "Bearer token"
    },
    "expected": {
        "status_code": 200,
        "max_response_time": 1000,
    },
    "enabled": True,
}


# 1. 获取用例名称。
test_case_name = test_case["name"]
print(test_case_name)
# 2. 获取Token。
token = test_case["headers"]["Authorization"].split(" ")[1]
print(token)
# 3. 获取预期状态码。
expected_status_code = test_case["expected"]["status_code"]
print(expected_status_code)
# 4. 增加标签字段。
test_case["tags"] = ["api", "user"]
print(test_case)
# 5. 判断用例是否启用。
is_enabled = test_case["enabled"]
print(is_enabled)
# 6. 删除Token字段。
del test_case["headers"]["Authorization"]
print(test_case)
