from pydantic import BaseModel
from datetime import datetime

class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    type: str
    requirements: str | None = None
    deadline: datetime | None = None

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    type: str | None = None
    requirements: str | None = None
    deadline: datetime | None = None
    is_active: bool | None = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    type: str
    requirements: str | None
    deadline: datetime | None
    teacher_id: int
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True

class SubmissionCreate(BaseModel):
    task_id: int
    file_path: str | None = None
    generated_content: str | None = None

class SubmissionUpdate(BaseModel):
    score: float | None = None
    comment: str | None = None
    status: str | None = None

class SubmissionResponse(BaseModel):
    id: int
    task_id: int
    student_id: int
    file_path: str | None
    generated_content: str | None
    status: str
    score: float | None
    comment: str | None
    submitted_at: datetime
    graded_at: datetime | None

    class Config:
        from_attributes = True