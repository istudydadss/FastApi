
from fastapi import APIRouter, HTTPException
from schemas import StudentCreate
from models import Student

from database import engine

from sqlmodel import Session,select


router = APIRouter()
#创建学生
@router.post("/student")
def create_student(student: StudentCreate):
    with Session(engine) as s:
        db_student = Student(**student.model_dump())
        s.add(db_student) # 添加学生到会话
        s.commit() 
        s.refresh(db_student)
    return {"status":200,"message":"创建学生成功","学生": db_student}


#查询学生
@router.get("/student/{id}")
def get_student(id: int):
    with Session(engine) as s:
        st = s.get(Student,id)
        if st is None:
            raise HTTPException(status_code=404,detail="该学生不存在")
    return {"status":200,"message":"查询学生成功","学生":st}


@router.get("/students")
def query_students(name: str | None = None, age: int | None = None, min_score: float | None = None,max_score: float | None = None, grade: str | None = None):
    conds = []
    if name is not None:
        conds.append(Student.name.contains(name))
    if age is not None:
        conds.append(Student.age == age)
    if min_score is not None:
        conds.append(Student.score >= min_score)
    if max_score is not None:
        conds.append(Student.score <= max_score)
    if grade is not None:
        conds.append(Student.grade == grade)
    
    stmt = select(Student)

    for c in conds:
        stmt = stmt.where(c)
    with Session(engine) as s:
        return s.exec(stmt).all()



#修改学生
@router.put("/student/{id}")
def update_student(id: int, student: StudentCreate):
    with Session(engine) as s:
        st = s.get(Student,id)
        if st is None:
            raise HTTPException(status_code=404,detail="该学生不存在")
        st.name = student.name
        st.age = student.age
        st.score = student.score
        st.grade = student.grade
        s.add(st)
        s.commit()
        s.refresh(st)
    return {"status":200,"message":"修改学生成功","学生": st}


#删除学生
@router.delete("/student/{id}")
def delete_student(id: int):
    with Session(engine) as s:
        st = s.get(Student,id)
        if st is None:
            raise HTTPException(status_code=404,detail="该学生不存在")
        s.delete(st)
        s.commit()
    return {"status":200,"message":"删除学生成功"}


#查询所有学生列表
@router.get("/student")
def get_students_all():
    with Session(engine) as s:
        return s.exec(select(Student)).all()

        