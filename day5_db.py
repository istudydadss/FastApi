# ===== Day 5:真数据库(SQLModel + SQLite)=====

# 【今天解决你忍了一天的三件事】
# 1) 重启不丢数据:数据存进磁盘文件 teachers.db,不再写在"草稿纸"(内存字典)上
# 2) id 数据库自动发:global 发号器消失;POST 返回自带 id(今天"手动补id"的活不用干了)
# 3) 不再手抄字段清单:s.add(整个对象)一行搞定,模型加字段也不会漏(grade事故消失)

# 【仓库比喻】
#   engine   = 仓库本身(磁盘上的 teachers.db 文件)
#   table    = 仓库里的一张货架(一个类=一张表)
#   Session  = 仓库管理员的手
#   add      = 把货放上传送带(还没真正入库!)
#   commit   = 按下"确认入库"——不 commit,东西只在传送带上(草稿)
#   refresh  = 入库后,把仓库自动编号(主键id)抄回你的收货单 

from fastapi import FastAPI, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select


# ---------- 1. 仓库位置:sqlite:/// + 文件名,就这一句 ----------
engine = create_engine("sqlite:///teachers.db", echo=False)


# ---------- 2. "模型 + 表"二合一(今天最核心的一行!)----------
class Teacher(SQLModel, table=True):        # table=True => 这个类就是数据库里的一张表
    id: int | None = Field(default=None, primary_key=True)  # 主键=自动发号的门牌号,不用自己管
    name: str
    age: int
    phone: str
    address: str


# ---------- 3. 照上面的类定义,把表建出来(已存在就跳过)----------
SQLModel.metadata.create_all(engine)
app = FastAPI()


# ========== C 创建:整包入库,不用手抄字段 ==========
@app.post("/teachers")
def create_teacher(teacher: Teacher):
    with Session(engine) as s:
        s.add(teacher)        # 放上传送带
        s.commit()            # 真正入库(没有这句,重启就没了!)
        s.refresh(teacher)    # 把数据库生成的 id 回填到对象
    return {"message": "老师添加成功", "老师": teacher}   # teacher 里已自带 id

# ========== R 按 id 查:主键查询,连 where 都不用写 ==========
@app.get("/teachers/{teacher_id}")
def get_teacher(teacher_id: int):
    with Session(engine) as s:
        t = s.get(Teacher, teacher_id)     # 按门牌号直接取,取不到=None
        if t is None:
            raise HTTPException(status_code=404, detail="查无此老师")
        return t                            # 对象含 id,返回天然带 id


# ========== R 查全部:select(表类).all() ==========
@app.get("/teachers")
def list_teachers():
    with Session(engine) as s:
        return s.exec(select(Teacher)).all()
# ---------- 🏋️ 留给你仿写的作业(CRUD 补齐后两件)----------
# PUT    /teachers/{teacher_id}:s.get 取出 → 改字段 → s.add + s.commit
# DELETE /teachers/{teacher_id}:s.get 取出 → s.delete + s.commit
# 写完 Ctrl+S 保存,--reload 生效,再用清单①复验 /docs
@app.put("/teachers/{teacher_id}")
def update_teacher(teacher_id: int,teacher: Teacher):
    with Session(engine) as s:
        # 取出要修改的老师
        t = s.get(Teacher, teacher_id)
        if t is None:
            raise HTTPException(status_code=404, detail="查无此老师")
        # 修改老师信息
        t.name = teacher.name
        t.age = teacher.age
        t.phone = teacher.phone
        t.address = teacher.address
        # 更新老师信息
        s.add(t)
        s.commit()
        s.refresh(t)
    return {"message": "老师修改成功", "老师": t}



@app.delete("/teachers/{teacher_id}")
def delete_teacher(teacher_id: int):
    with Session(engine) as s:
        t = s.get(Teacher, teacher_id)
        if t is None:
            raise HTTPException(status_code=404, detail="查无此老师")
        s.delete(t)
        s.commit()
    return {"message": "老师删除成功"}

