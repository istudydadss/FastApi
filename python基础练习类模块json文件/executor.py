# executor.py：执行器模块
# 负责：模拟发请求 -> 跑断言 -> 汇总结果 -> 写回 JSON


import json
import random
from pathlib import Path

# 模块导入：从其他模块按需导入
from models import TestCase, TestResult
from assertions import assert_status, assert_response_time, assert_all


class TestExecutor:
    """用例执行器"""
    def __init__(self, base_url: str = "https://api.example.com") -> None:
        self.base_url = base_url
        self.results: list[TestResult] = []
    
    def load_cases(self, file_path: Path) -> list[TestCase]:
        """从 JSON 文件读取用例数据"""

        with open(file_path, "r", encoding="utf-8") as f:
            raw_list = json.load(f)

        return [TestCase.from_dict(item) for item in raw_list]


    def send_requests(self, case: TestCase) -> dict:
        """模拟发送请求（真实项目里用 requests 库）"""

        # 模拟：大部分返回期望状态码，小概率返回 500

        if random.random() < 0.2:
            status = 500

        else:
            status = case.expected_status
        return {
            "status_code": status,
            "elapsed_ms": random.randint(50,800),
        }


    def run_case(self, case: TestCase) -> TestResult:
        """ 执行单条用例"""
        response = self.send_requests(case)
        passed = assert_all(
            [
                assert_status(response["status_code"], case.expected_status),
                assert_response_time(response["elapsed_ms"], case.max_response_time)
            ]
        )

        result = TestResult(case,passed, response["status_code"],response["elapsed_ms"])
        self.results.append(result)
        return result



    def run_all(self, cases: list[TestCase]) -> None:
        """运行全部用例"""

        for case in cases:
            result = self.run_case(case)
            print(result.format())


    def pass_rate(self) -> float:
        """计算通过率"""

        if not self.results:
            return 0.0
        passed = sum(1 for r in self.results if r.passed)
        return passed / len(self.results)

    def save_report(self, file_path: Path) -> None:
        """把结果写入 JSON 文件"""

        report = [
            {
                "name": r.case.name,
                "passed": r.passed,
                "expected_status": r.case.expected_status,
                "actual_status": r.actual_status,
                "response_time": r.elapsed_ms,
            }
            for r in self.results
        ]

        # 目标不存在就先创建

        file_path.parent.mkdir(parents=True,exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(report,f,ensure_ascii=False,indent=4)

        print(f"报告已保存到 {file_path}")





    





 