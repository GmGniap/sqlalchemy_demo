from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base
from models import Base

# Create an engine to connect to sqlite db
engine = create_engine("sqlite:///demo.db", echo=True)

# # Establish a connection
# connection = engine.connect()

## Drop if exist
# Base.metadata.drop_all(engine)

## Create tables by following schema from models.py
Base.metadata.create_all(engine)