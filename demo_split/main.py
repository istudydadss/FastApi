# main.py —— 总装配车间:建 app、把 router 装车。不含任何业务代码!

from fastapi import FastAPI

from routers import books

app = FastAPI(title="拆包演示")

# 装车:把 books 这束路由挂到 app 上
app.include_router(books.router)
