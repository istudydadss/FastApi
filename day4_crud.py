# ===== Day 4:完整 CRUD(增删改查)+ 404 错误处理 =====
#
# 昨天(Day3)你已经做对了 CRUD 的一半:
#   C 创建  POST ✅      R 读取  GET ✅
# 今天补齐另一半:
#   U 更新  PUT  (今天新学)      D 删除  DELETE (今天新学)
#
# 【餐厅比喻】一桌菜的四件事:
#   下单(POST) / 看这桌点了啥(GET) / "这道菜改成不辣"(PUT) / "撤掉这道菜"(DELETE)
#
# 【今天两个最重要的新观念】
#   1) 存储从 list 升级成 dict:
#      改和删都要"精确点名某一个"(比如 3 号学生)。
#      list 像排队,位置会挪、找要一个个翻;dict 像储物柜,给每人一个门牌号(id),一秒打开。
#   2) 404 错误处理:
#      你要改/删的 id 根本不存在(比如 99 号),不能假装成功,
#      要大声告诉对方"查无此人" -> 主动抛出 HTTPException(404)。
#      (还记得 Day3 的 422 吗?那是自动校验;今天这个 404 是你主动抛!)


from fastapi import FastAPI, HTTPException   # 新增 HTTPException:主动抛错误的工具
from pydantic import BaseModel

app = FastAPI()


# ---------- 输入模具:客人创建学生时填的内容(注意:不含 id!)----------
# 为什么不含 id?因为 id(门牌号)是"系统"发的,不能让客人自己填,
# 否则两个人抢同一个柜号就乱套了。
class StudentIn(BaseModel):
    name: str
    age: int
    grade: str


# ---------- "数据库":用字典存。key 是 id(门牌号),value 是学生资料 ----------
# 这是今天最大的升级:list -> dict
students_db: dict[int, dict] = {}
next_id: int = 1   # 发号器:下一个要分配的门牌号


# ========== C 创建:POST /students ==========
@app.post("/students")
def create_student(student: StudentIn):
    global next_id                     # 要在函数里改全局变量,得先 global 声明
    new_id = next_id                   # 给这个新学生分配门牌号
    next_id += 1                       # 发号器 +1,留给下一个
    students_db[new_id] = {"id": new_id, "name": student.name, "age": student.age}
    return {"状态": "创建成功", "分配的门牌号id": new_id}


# ========== R 读取:GET /students/{student_id} —— 顺便演示 404 ==========
@app.get("/students/{student_id}")
def get_student(student_id: int):
    if student_id not in students_db:                       # 门牌号不存在
        raise HTTPException(status_code=404, detail="查无此学生")   # 主动抛 404!
    return students_db[student_id]


# ========== U 更新:PUT /students/{student_id}(今天新学 ⭐)==========
# 人话:把某个学生的资料整份换新(比如改年龄)
@app.put("/students/{student_id}")
def update_student(student_id: int, student: StudentIn):
    if student_id not in students_db:                 # 先确认存在,不存在 404
        raise HTTPException(status_code=404, detail="查无此学生")
    students_db[student_id] = {"id": student_id, "name": student.name, "age": student.age}
    return {"状态": "更新成功", "现在的资料": students_db[student_id]}


# ========== D 删除:DELETE /students/{student_id}(今天新学 ⭐)==========
# 人话:把这个学生从数据库里彻底移除
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="查无此学生")
    removed = students_db.pop(student_id)             # pop:取出来并删掉
    return {"状态": "删除成功", "被删的是": removed["name"]}

@app.get("/students")
def get_students():
    return {"所有学生": students_db}

