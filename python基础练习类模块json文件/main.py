# main.py：程序入口
# 运行方式：在 week01 目录下执行  python main.py

from pathlib import Path

from models import TestCase
from executor import TestExecutor


def main() -> None:
    # 文件路径：用 __file__ 定位，无论在哪运行都能找到 data 目录
    base_dir = Path(__file__).parent
    cases_file = base_dir / "testcase.json"
    report_file = base_dir / "report.json"

    if not cases_file.exists():
        print(f"用例文件不存在: {cases_file}")
        return

    executor = TestExecutor()

    # 1. 读取 JSON 用例
    cases = executor.load_cases(cases_file)
    print(f"共加载 {len(cases)} 条用例")
    for case in cases:
        print(" -", case)

    print("-" * 40)

    # 2. 执行全部用例
    executor.run_all(cases)

    # 3. 输出通过率
    print("-" * 40)
    print(f"通过率: {executor.pass_rate():.0%}")

    # 4. 保存 JSON 报告
    executor.save_report(report_file)


# 只有直接运行 main.py 时才执行；被别的模块 import 时不执行
if __name__ == "__main__":
    main()