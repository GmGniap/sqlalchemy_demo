from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base
from models import Student, Classroom, Base

# Create an engine to connect to sqlite db
engine = create_engine("sqlite:///test.db", echo=True)

# Establish a connection
connection = engine.connect()

## Create tables by following schema from models.py
Base.metadata.create_all(engine)