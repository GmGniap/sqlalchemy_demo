from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from models import Classroom, Student

engine = create_engine("sqlite:///test.db", echo=True)

with Session(engine) as session:

    query = select(Student)
    for student in session.scalars(query):
        print(student)

