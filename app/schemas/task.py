from pydantic import BaseModel, ConfigDict

class TsakCreate(BaseModel):
    title: str
    description: str |None = None
    category: str |None = None

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    category: str | None = None
    completed: bool | None = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str |None
    category: str |None
    completed: bool

    model_config = ConfigDict(from_attributes=True)

