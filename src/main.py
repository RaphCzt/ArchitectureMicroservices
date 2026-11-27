from typing import Optional

from fastapi import FastAPI, HTTPException, status
from src.api import TodoCreate, TodoUpdate, create_todo, get_todos, todos_db, delete_todo, get_todo, update_todo, replace_todo
from uuid import UUID

app = FastAPI(title="Todo API")



@app.post("/todos", status_code=status.HTTP_201_CREATED)
def create_todo_endpoint(todo: TodoCreate):
    return create_todo(todo)

@app.get("/todos")
def list_todos():
    return todos_db

@app.get("/todos/{todo_id}")
def get_todo_endpoint(todo_id: UUID):
    todo = get_todo(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo non trouvé")
    return todo

@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo_endpoint(todo_id: UUID):
    deleted = delete_todo(todo_id)
    if not deleted:
        raise HTTPException(status_code=404, detail='Todo non trouvé')
    return {"message":"Todo supprimé"}

@app.patch("/todos/{todo_id}")
def patch_todo_endpoint(todo_id: UUID, todo_data: TodoUpdate):
    todo = update_todo(todo_id, todo_data)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo non trouvé")
    return todo

@app.put("/todos/{todo_id}")
def put_todo_endpoint(todo_id: UUID, todo_data: TodoUpdate):
    todo = replace_todo(todo_id, todo_data)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo non trouvé")
    return todo

@app.get("/todos")
def list_todos(tag: Optional[str] = None, tags: Optional[str]=None):
    tag_list = tags.split(',') if tags else None
    return get_todos(tag=tag, tags=tag_list)

@app.get("/todos/search")
def search_todos(q: Optional[str] = None, tag: Optional[str] = None):
    results = todos_db
    if q:
        q_lower = q.lower()
        results = [t for t in results 
                   if q_lower in t.title.lower()
                   or (t.description and q_lower in t.description.lower())]
    if tag:
        results = [t for t in results if tag in t.tags]
    return results
