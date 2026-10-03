from sqlmodel import  create_engine


engine = create_engine("sqlite:///students.db", echo=True)
