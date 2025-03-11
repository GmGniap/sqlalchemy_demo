## Ref - https://docs.sqlalchemy.org/en/20/orm/quickstart.html#declare-models


from sqlalchemy import ForeignKey, Integer,String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Student(Base):
    __tablename__ = "student"

    student_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    age: Mapped[int]
    academic_year: Mapped[int]

    classroom_id: Mapped[int] = mapped_column(ForeignKey("classroom.classroom_id"), nullable=False)
    classroom: Mapped["Classroom"] = relationship(back_populates="student_lst")

    ## Need to show with/without __repr__
    def __repr__(self):
        return f"Student_id:{self.student_id}\nName:{self.name} from {self.academic_year} Year"
    
    
class Classroom(Base):
    __tablename__ = "classroom"

    classroom_id: Mapped[int] = mapped_column(primary_key=True)
    class_name: Mapped[str] = mapped_column(nullable=False)

    student_lst: Mapped[list["Student"]] = relationship(back_populates="classroom", cascade="all, delete-orphan")

