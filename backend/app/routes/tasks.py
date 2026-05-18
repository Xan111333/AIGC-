from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.task_service import (
    create_task, get_tasks, get_task, update_task, delete_task,
    create_submission, get_submissions, get_submission, grade_submission,
    get_student_tasks, get_task_statistics
)
from ..schemas.task import TaskCreate, TaskUpdate, TaskResponse, SubmissionCreate, SubmissionUpdate, SubmissionResponse
from ..utils.depends import get_current_active_user, require_teacher, require_admin
from ..models import User

router = APIRouter(prefix="/api/tasks", tags=["实训任务"])

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_new_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher)
):
    return create_task(db, task, current_user.id)

@router.get("/", response_model=list[TaskResponse])
def list_tasks(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if current_user.role in ["teacher", "admin"]:
        return get_tasks(db, skip, limit, current_user.id)
    return get_tasks(db, skip, limit)

@router.get("/{task_id}", response_model=TaskResponse)
def get_task_by_id(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    task = get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="任务不存在")
    return task

@router.put("/{task_id}", response_model=TaskResponse)
def update_task_by_id(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher)
):
    task = get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="任务不存在")
    if task.teacher_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="只能修改自己创建的任务")
    return update_task(db, task_id, task_update)

@router.delete("/{task_id}", response_model=TaskResponse)
def delete_task_by_id(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher)
):
    task = get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="任务不存在")
    if task.teacher_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="只能删除自己创建的任务")
    return delete_task(db, task_id)

@router.post("/submissions", response_model=SubmissionResponse, status_code=status.HTTP_201_CREATED)
def submit_assignment(
    submission: SubmissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if current_user.role == "teacher" or current_user.role == "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="学生才能提交作业")
    return create_submission(db, submission, current_user.id)

@router.get("/submissions", response_model=list[SubmissionResponse])
def list_submissions(
    task_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if current_user.role == "student":
        return get_submissions(db, task_id, current_user.id, skip, limit)
    return get_submissions(db, task_id, None, skip, limit)

@router.get("/submissions/{submission_id}", response_model=SubmissionResponse)
def get_submission_by_id(
    submission_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    submission = get_submission(db, submission_id)
    if not submission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="作业不存在")
    
    if current_user.role == "student" and submission.student_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="只能查看自己的作业")
    
    return submission

@router.put("/submissions/{submission_id}", response_model=SubmissionResponse)
def grade_assignment(
    submission_id: int,
    update: SubmissionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher)
):
    submission = get_submission(db, submission_id)
    if not submission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="作业不存在")
    
    task = get_task(db, submission.task_id)
    if task and task.teacher_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="只能批改自己发布的任务")
    
    return grade_submission(db, submission_id, update)

@router.get("/{task_id}/statistics")
def get_task_stats(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher)
):
    task = get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="任务不存在")
    if task.teacher_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="只能查看自己任务的统计")
    return get_task_statistics(db, task_id)