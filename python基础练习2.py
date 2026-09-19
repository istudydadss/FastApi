test_cases = [
    {"name": "用例1", "status": 200, "enabled": True},
    {"name": "用例2", "status": 500, "enabled": True},
    {"name": "用例4", "status": 500, "enabled": True},
    {"name": "用例5", "status": 500, "enabled": True},
    {"name": "用例3", "status": 404, "enabled": False},
]

success_count = 0
failure_count = 0
failure_case = []
for test_case in test_cases:
    # - 跳过未启用用例
    if not test_case["enabled"]:
        continue
    # - 判断用例执行结果
    if test_case["status"] == 200:
        success_count += 1
     
        print(f"{test_case['name']}用例执行成功")
    else:
        failure_count += 1
        failure_case.append(test_case)
        print(f"{test_case['name']}用例执行失败")

print("成功用例数量：", success_count)
print("失败用例数量：", failure_count)

# - 筛选全部失败用例
for case in failure_case:
    print(case["name"])

