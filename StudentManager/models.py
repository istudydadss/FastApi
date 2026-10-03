from sqlmodel import SQLModel, Field

from database import engine
class Student(SQLModel,table=True):
    id: int | None = Field(default=None,primary_key=True)
    name: str
    age: int
    score: float
    grade: str


# 结合数据模型创建数据表
SQLModel.metadata.create_all(engine)
