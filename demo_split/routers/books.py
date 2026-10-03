# routers/books.py —— 只干一件事:books 这组路由(增删改查)
# 关键区别:以前是 @app.get(...),现在是 @router.get(...)
# router 只是个"收纳架",最后要由 main.py 装车。

from fastapi import APIRouter, HTTPException
from sqlmodel import Session

from database import engine
from models import Book
from schemas import BookCreate

router = APIRouter()


@router.post("/book")
def create_book(book: BookCreate):
    with Session(engine) as s:
        db_book = Book(**book.model_dump())  # 报名表 → 档案卡
        s.add(db_book)
        s.commit()
        s.refresh(db_book)
    return {"status": 200, "message": "创建成功", "书": db_book}


@router.get("/book/{id}")
def get_book(id: int):
    with Session(engine) as s:
        b = s.get(Book, id)
        if b is None:
            raise HTTPException(status_code=404, detail="这本书不存在")
        return {"status": 200, "书": b}
