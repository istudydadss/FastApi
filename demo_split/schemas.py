# schemas.py —— 只干一件事:定义"报名表"(输入模型)
# 注意:这个文件不需要 import database,也不需要连数据库!
# 报名表只是"客人能填什么"的校验标准,和数据库无关。

from pydantic import BaseModel


class BookCreate(BaseModel):
    title: str
    price: float
