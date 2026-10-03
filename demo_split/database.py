# database.py —— 只干一件事:连数据库
# 谁需要数据库,谁就 import 这里的 engine

from sqlmodel import create_engine

# demo.db 会生成在这个文件夹里(和 StudentManager 的 students.db 互不干扰)
engine = create_engine("sqlite:///demo.db", echo=False)
