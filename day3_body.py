# ===== Day 3:请求体(Request Body)+ Pydantic 模型 =====
#
# 回顾前两天的"数据从哪来":
#   Day1 路径参数:/hello/{name}       —— 数据在网址路径里
#   Day2 查询参数:/search?keyword=x   —— 数据在 ? 后面
# 这两种数据都写在 URL 里,适合 GET 请求传"少量、简单"的数据。
#
# 【新场景】要"创建"一个学生,数据又多又复杂:
#   姓名、年龄、邮箱、是否毕业…… 全塞进 URL 里又长又乱又不安全。
#   这时用"请求体(Request Body)":数据打包成 JSON,放进请求的"包裹"里,用 POST 发送。
#
# 【餐厅比喻升级】
#   GET + 查询参数 = 口头跟服务员说"要辣一点"(简单要求)
#   POST + 请求体  = 填一整张"订单表"(姓名/菜品/数量/备注),交给后厨
#
# 【Pydantic 是什么】
#   它就是这张"订单表的模板/模具":规定必须填哪些字段、每个字段什么类型。
#   填错了(少填、类型不对),FastAPI 当场打回,返回 422。
#   —— 和你 week01 的 TestCase 类是同一思路,只是 Pydantic 自带校验超能力!


from fastapi import FastAPI
from pydantic import BaseModel   # Pydantic 的"数据模具"基类

app = FastAPI()


# ---------- 第 1 步:定义一个"数据模具"(Pydantic 模型)----------
# 人话:我规定一个"学生"必须长这样。继承 BaseModel 后,这个类自动获得校验能力。
class Student(BaseModel):
    name: str                    # 必填,文字
    age: int                     # 必填,整数
    email: str | None = None     # 可选,不填就是 None(用上你 Day1 学的 str | None)
    graduated: bool = False      # 可选,默认没毕业


# 用一个列表先"假装"是数据库,存放创建的学生(Day4/Day5 会换成真数据库)
students_db: list[Student] = []


# ---------- 第 2 步:POST 创建学生(接收请求体)----------
# 人话:有人 POST 一段 JSON 到 /students,就用 Student 模具自动校验它
# 关键:参数 student: Student —— 类型是模型名,FastAPI 就知道"去请求体里读 JSON"
@app.post("/students")
def create_student(student: Student):
    # 能走到这里,说明数据已通过校验、类型也转好了,直接用 . 取字段
    students_db.append(student)
    return {"状态": "创建成功", "收到的学生": student.name, "当前总数": len(students_db)}


# ---------- 第 3 步:GET 查询所有学生 ----------
# 人话:创建完想看看存了哪些?GET /students 一次性返回
# 注意:路径同样是 /students,但方法不同(一个 POST 一个 GET),是两个不同的接口
@app.get("/students")
def list_students():
    return {"所有学生": students_db}
