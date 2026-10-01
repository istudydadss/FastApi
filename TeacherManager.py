# 教室管理系统 主要为增删改产.用于读fastapi
# 基本功能的联系,练习的方法为post put delete get
# 我认为fastapi框架主要为三部分 1.路由 2.请求 3.响应



from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()


# 定义老师的基本模型
class Teacher(BaseModel):
    name: str
    age: int
    phone: str
    address: str

# 存储老师的信息
teacher_db: dict[int, Teacher] = {} 
teacher_id: int = 0

# 添加老师的信息
@app.post("/teacher")
def create_teacher(teacher: Teacher):
    global teacher_id
    teacher_id += 1
    teacher_db[teacher_id] = teacher
    return {"status": 200,"message":"老师添加成功"}
# 根据id来查询老师的信息
@app.get("/teacher/{teacher_id}")
def get_teacher(teacher_id: int):
    if teacher_id not in teacher_db:
        raise HTTPException(status_code=404, detail="查无此学生")
    return teacher_db[teacher_id]
# 展示老师全部信息
@app.get("/teacher")
def get_teacher():
    return teacher_db
# 根据id来修改老师的信息
@app.put("/teacher/{teacher_id}")
def update_teacher(teacher_id: int, teacher: Teacher):
    if teacher_id not in teacher_db:
        raise HTTPException(status_code=404, detail="查无此学生")
    teacher_db[teacher_id] = {"name": teacher.name, "age": teacher.age, "phone": teacher.phone, "address": teacher.address}
    return {"status": 200,"message":"老师修改成功", "更新后老师的信息": teacher_db[teacher_id]}
# 根据id删除老师信息
@app.delete("/teacher/{teacher_id}")
def delete_teacher(teacher_id: int):
    if teacher_id not in teacher_db:
        raise HTTPException(status_code=404, detail="查无此学生")
    teacher_db.pop(teacher_id)
    return {"status": 200,"message":"老师删除成功"}
    

   
