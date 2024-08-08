from sqlmodel import SQLModel, Field, Session, create_engine
from dotenv import load_dotenv
import os
load_dotenv()

conn_str : str = os.getenv("DATABASE_URL")
engine = create_engine(conn_str, pool_recycle=300, pool_size=10)

def get_db():
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()
def creat_tables():
    SQLModel.metadata.create_all(engine)
