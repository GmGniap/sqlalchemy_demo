import pandas as pd
from sqlalchemy import create_engine

import os
from dotenv import load_dotenv
load_dotenv()

postgres_url = os.getenv('postgres')
print(postgres_url)

engine = create_engine(postgres_url, echo=True)
classroom_df = pd.read_csv("./data/classroom.csv")
student_df = pd.read_csv("./data/student.csv")

classroom_df.to_sql('classroom', engine, if_exists='append', index=False)
student_df.to_sql('student', engine, if_exists='append', index=False)
print(f"Successfully added data into Postgres!")