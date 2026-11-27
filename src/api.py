from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from enum import Enum

class State(Enum):
    NDONE = "not done"
    INPROGRESS = "in progress"
    DONE = "done"


class TodoCreate(BaseModel):
    title: str = Field(..., max_length=100)
    description: Optional[str] = None
    state: State = Field(default=State.NDONE)
    tags: list[str] = Field(default_factory=list)

class TodoUpdate(BaseModel):
    title: Optional[str] = Field(default=None, max_length=100)
    description: Optional[str] = None
    state: Optional[State] = None
    tags: Optional[list[str]] = None

class Todo(BaseModel):
    id : UUID
    title : str 
    description : Optional[str] = None
    state: State = State.NDONE
    created_at : datetime
    tags: list[str] = Field(default_factory=list)


todos_db: list[Todo] = []

def create_todo(todo_data: TodoCreate) -> Todo:
    todo = Todo(**todo_data.model_dump(), id=uuid4(), created_at=datetime.now())
    todos_db.append(todo)
    return todo

def get_todo(id: UUID) -> Optional[Todo]:
    for todo in todos_db:
            if todo.id == id:
                return todo
    return None

def update_todo(id: UUID, todo_data: TodoUpdate) -> Optional[Todo]:
    todo = get_todo(id)
    if not todo:
        return None
    update_data = todo_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(todo,key,value)
    return todo

def replace_todo(id: UUID, todo_data: TodoCreate) -> Optional[Todo]:
    todo = get_todo(id)
    if not todo:
        return None
    new_todo = Todo(
        **todo_data.model_dump(),
        id = todo.id,
        created_at=todo.created_at
    )
    for i, t in enumerate(todos_db):
        if t.id == id:
            todos_db[i] = new_todo
            break
    return new_todo


def delete_todo(id: UUID) -> bool:
    for i,todo in enumerate(todos_db):
        if todo.id == id:
            todos_db.pop(i)
            return True
    return False

def get_todos(tag: Optional[str] = None, tags: Optional[list[str]] = None) -> list[Todo]:
    result = todos_db
    if tag:
        result = [t for t in result if tag in t.tags]
    if tags:
        result = [t for t in result if all(tg in t.tags for tg in tags)]
    return result
        

    
