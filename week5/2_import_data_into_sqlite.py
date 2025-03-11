import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("sqlite:///demo.db", echo=True)
classroom_df = pd.read_csv("./data/classroom.csv")
student_df = pd.read_csv("./data/student.csv")

print(classroom_df.shape)
print(classroom_df.columns)

classroom_df.to_sql('classroom', engine, if_exists='append', index=False)
student_df.to_sql('student', engine, if_exists='append', index=False)

