
from sqlmodel import SQLModel, Field, Session, create_engine

class NEXTJS_TODOS(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, index = True)
    title: str
    completed: bool | None =  Field(default=False)


class CREATE_TODO(SQLModel):
   title: str


class NextJS_TODO_RETURN(SQLModel):
   id: int 
   title: str
   completed: bool 
class Update_TODO(SQLModel):
    id : int
    title: str


