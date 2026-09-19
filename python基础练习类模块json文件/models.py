# models.py：数据模型模块
# 用类来描述一条测试用例，比裸 dict 更清晰、有提示



class TestCase:
    """ 一条测试用例"""


    def __init__(self,name :str,method :str,path :str,expected_status :int = 200,max_response_time :int = 1000) -> None:
        self.name = name
        self.method = method
        self.path = path
        self.expected_status = expected_status
        self.max_response_time = max_response_time


    @classmethod
    def from_dict(cls, data: dict) -> "TestCase":
        return cls(
            name=data["name"],
            method=data["method"],
            path=data["path"],
            expected_status=data.get("expected_status",200),
            max_response_time=data.get("max_response_time",1000)
        )

    def __str__(self) -> str:
        return f"[{self.method}] {self.name} -> 期望 {self.expected_status}"


class TestResult:
    """一条用例的执行结果"""

    def __init__(self, case: TestCase, passed: bool,actual_status: int, elapsed_ms: int) -> None:
         self.case = case
         self.passed = passed
         self.actual_status = actual_status
         self.elapsed_ms = elapsed_ms

    def format(self) -> str:
        tag = "SUCCESS" if self.passed else "ERROR"
        return (
            f"[{tag}] {self.case.name}"
            f"(状态码: {self.case.expected_status}/实际{self.actual_status})"
            f"(响应时间: {self.elapsed_ms}ms)"
        )
            
    
