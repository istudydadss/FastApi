from fastapi import FastAPI

from routers import students


app = FastAPI(title="学生信息管理系统")

app.include_router(students.router)
