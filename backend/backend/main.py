from fastapi import FastAPI, Depends
from .models import NEXTJS_TODOS, CREATE_TODO, NextJS_TODO_RETURN, Update_TODO
from .database import get_db, creat_tables
from typing import Annotated
from sqlmodel import Session, select
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.on_event("startup")
def on_startup():
    creat_tables()

@app.get("/api/health")
def hello_world():
    return {"message": "Hello World"}


@app.post("/api/todos", response_model = NextJS_TODO_RETURN)
def create_todos(todo: CREATE_TODO, session: Annotated[Session, Depends(get_db)]):
    todo = NEXTJS_TODOS.model_validate(todo)
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo

@app.get("/api/todos", response_model=list[NEXTJS_TODOS])
def get_todos(session: Annotated[Session, Depends(get_db)]):
    todos = session.exec(select(NEXTJS_TODOS)).all()
    return todos

@app.put("/api/todos")
def update_todos(update_todo: Update_TODO, session: Annotated[Session, Depends(get_db)]):
    statment = select(NEXTJS_TODOS).where(NEXTJS_TODOS.id == update_todo.id)
    todo_db = session.exec(statment).one()
    todo_db.title = update_todo.title
    session.add(todo_db)
    session.commit()
    session.refresh(todo_db)
    return todo_db

@app.delete("/api/todos/{todo_id}")
def delete_todos(todo_id: int, session: Annotated[Session, Depends(get_db)]):
    statment = select(NEXTJS_TODOS).where(NEXTJS_TODOS.id == todo_id)
    todo_db = session.exec(statment).one()
    session.delete(todo_db)
    session.commit()
    return {"message": "Todo deleted successfully"}