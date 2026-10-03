# models.py —— 只干一件事:定义"档案卡"(数据库表模型)

from sqlmodel import Field, SQLModel

from database import engine  # 档案卡要入库,所以需要连接

# 这个model层的含义我理解的就是定义基本的数据模型和数据表
class Book(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    price: float


# 建表(只建表,不会删已有数据)
SQLModel.metadata.create_all(engine)
