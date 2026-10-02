# 学生成绩管理系统后端crud接口,三层架构:路由+pydantic+sqlmodel


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, SQLModel, create_engine, select,Field



engine = create_engine("sqlite:///students.db", echo=False)


# 学生模型
class Student(SQLModel,table=True):
    id: int | None = Field(default=None,primary_key=True)
    name: str
    age: int
    score: float
    grade: str


# 输入模型:只描述"客人能填什么"——没有 id(门牌号店家发),校验严格,脏数据会被挡在 422
class StudentCreate(BaseModel):
    name: str
    age: int
    score: float
    grade: str


# 按照上面的创建相关的表结构
SQLModel.metadata.create_all(engine)
app = FastAPI()



#创建学生
@app.post("/student")
def create_student(student: StudentCreate):
    with Session(engine) as s:
        db_student = Student(**student.model_dump())  # 输入模型 → 表模型(数据库那一行)
        s.add(db_student) # 添加学生到会话 
        s.commit()
        s.refresh(db_student)
    return {"status": 200,"message":"创建学生成功","学生": db_student}



#根据姓名查询学生
@app.get("/student/{id}")
def get_student(id: int):
    with Session(engine) as s:
        st = s.get(Student,id)  #  根据id查询学生信息
        if st is None:
            raise HTTPException(status_code=404, detail="该学生不存在")
        return {"status": 200,"message":"查询学生成功","学生": st}


@app.put("/student/{id}")
def update_student(id: int,student: StudentCreate):
    with Session(engine) as s:
        st = s.get(Student, id)
        if st is None:
            raise HTTPException(status_code=404, detail="该学生不存在")
        st.name = student.name
        st.age = student.age
        st.score = student.score
        st.grade = student.grade
        s.add(st)
        s.commit()
        s.refresh(st)
    return {"status": 200,"message": "更新学生成功","更新后的学生": st}


@app.delete("/student/{id}")
def delete_student(id: int):
    with Session(engine) as s:
        st = s.get(Student,id)
        if st is None:
            raise HTTPException(status_code=404, detail="该学生不存在")
        s.delete(st)
        s.commit()
    return {"status": 200,"message": "删除学生成功"}


#查询所有学生信息
@app.get("/student")
def get_students():
    with Session(engine) as s:
        return s.exec(select(Student)).all()


# 你的代码(行号)	它背后实际发给数据库的 SQL	属于
# class Student(SQLModel, table=True):	# 创建学生表
#     id: int | None = Field(default=None, primary_key=True)	# id: int | None = Field(default=None, primary_key=True)
#     name: str	# name: str
#     age: int	# age: int
#     score: float	# score: float
#     grade: str	# grade: str
# s.add(student) + s.commit()(POST 32-33行)	
# INSERT INTO student (name, age, score, grade) VALUES ('WangWei', 18, 95.5, 'GaoSan')	C



# s.get(Student, id)(GET 43行)	SELECT id,name,age,score,grade FROM student WHERE id = 1	R


# st.age = student.age … + commit()(PUT 56-61行)	UPDATE student SET age=19, score=100.0 WHERE id = 1	U


# s.delete(st) + commit()(DELETE 71-72行)	DELETE FROM student WHERE id = 1	D


# s.exec(select(Student)).all()(你 day5 写过)	SELECT * FROM student	查全部