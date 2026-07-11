from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskResponse,TaskUpdate,TsakCreate
from app.dependencies.dep_database import get_db
from app.core.security import get_current_user

router = APIRouter(prefix="/task", tags=["task"])

@router.post("/", response_model = TaskResponse)
async def create_task(task: TsakCreate,db:Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    new_task = Task(title=task.title, description=task.description, category=task.category,  owner_id=current_user.id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.get("/", response_model=list[TaskResponse])
async def get_tasks(
    completed: Optional[bool] = None,
    category: Optional[str] = None,
    db:Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    query=db.query(Task).filter(Task.owner_id==current_user.id)
    if completed is not None:
        query = query.filter(
            Task.completed == completed
        )
    if category:
        query = query.filter(
            Task.category == category
        )
    return query.all()

@router.get("/{task_id}", response_model=TaskResponse)
async  def get_task(task_id:int,db:Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id,Task.owner_id==current_user.id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task (task_id: int , task_data: TaskUpdate,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id, Task.owner_id==current_user.id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    for key,value in task_data.model_dump(exclude_unset= True).items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task

@router.delete("/{task_id}")
async def delete_task(task_id:int, db:Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == current_user.id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}

