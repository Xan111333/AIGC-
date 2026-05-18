from sqlalchemy.orm import Session
from ..models import Task, Submission, User
from ..schemas.task import TaskCreate, TaskUpdate, SubmissionCreate, SubmissionUpdate
from fastapi import HTTPException, status
from datetime import datetime

def create_task(db: Session, task: TaskCreate, teacher_id: int) -> Task:
    new_task = Task(
        title=task.title,
        description=task.description,
        type=task.type,
        requirements=task.requirements,
        deadline=task.deadline,
        teacher_id=teacher_id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def get_tasks(db: Session, skip: int = 0, limit: int = 100, teacher_id: int | None = None):
    query = db.query(Task)
    if teacher_id:
        query = query.filter(Task.teacher_id == teacher_id)
    return query.filter(Task.is_active == True).offset(skip).limit(limit).all()

def get_task(db: Session, task_id: int) -> Task | None:
    return db.query(Task).filter(Task.id == task_id, Task.is_active == True).first()

def update_task(db: Session, task_id: int, task_update: TaskUpdate) -> Task:
    task = get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="任务不存在")
    
    if task_update.title:
        task.title = task_update.title
    if task_update.description is not None:
        task.description = task_update.description
    if task_update.type:
        task.type = task_update.type
    if task_update.requirements is not None:
        task.requirements = task_update.requirements
    if task_update.deadline:
        task.deadline = task_update.deadline
    if task_update.is_active is not None:
        task.is_active = task_update.is_active
    
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task_id: int) -> Task:
    task = get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="任务不存在")
    
    task.is_active = False
    db.commit()
    db.refresh(task)
    return task

def create_submission(db: Session, submission: SubmissionCreate, student_id: int) -> Submission:
    task = get_task(db, submission.task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="任务不存在")
    
    existing_submission = db.query(Submission).filter(
        Submission.task_id == submission.task_id,
        Submission.student_id == student_id
    ).first()
    if existing_submission:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="已提交过该作业")
    
    new_submission = Submission(
        task_id=submission.task_id,
        student_id=student_id,
        file_path=submission.file_path,
        generated_content=submission.generated_content,
        status="pending"
    )
    db.add(new_submission)
    db.commit()
    db.refresh(new_submission)
    return new_submission

def get_submissions(db: Session, task_id: int | None = None, student_id: int | None = None, skip: int = 0, limit: int = 100):
    query = db.query(Submission)
    if task_id:
        query = query.filter(Submission.task_id == task_id)
    if student_id:
        query = query.filter(Submission.student_id == student_id)
    return query.order_by(Submission.submitted_at.desc()).offset(skip).limit(limit).all()

def get_submission(db: Session, submission_id: int) -> Submission | None:
    return db.query(Submission).filter(Submission.id == submission_id).first()

def grade_submission(db: Session, submission_id: int, update: SubmissionUpdate) -> Submission:
    submission = get_submission(db, submission_id)
    if not submission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="作业不存在")
    
    if update.score is not None:
        submission.score = update.score
    if update.comment is not None:
        submission.comment = update.comment
    if update.status:
        submission.status = update.status
    
    if update.score is not None or update.status == "completed":
        submission.graded_at = datetime.utcnow()
        submission.status = "completed"
    
    db.commit()
    db.refresh(submission)
    return submission

def get_student_tasks(db: Session, student_id: int, skip: int = 0, limit: int = 100):
    submissions = db.query(Submission).filter(Submission.student_id == student_id).all()
    task_ids = [s.task_id for s in submissions]
    
    tasks = db.query(Task).filter(Task.id.in_(task_ids), Task.is_active == True).all()
    return tasks

def get_task_statistics(db: Session, task_id: int):
    total = db.query(Submission).filter(Submission.task_id == task_id).count()
    graded = db.query(Submission).filter(
        Submission.task_id == task_id,
        Submission.status == "completed"
    ).count()
    
    avg_score = db.query(Submission.score).filter(
        Submission.task_id == task_id,
        Submission.score is not None
    ).all()
    
    if avg_score:
        avg_score = sum(s[0] for s in avg_score) / len(avg_score)
    else:
        avg_score = 0
    
    return {
        "total_submissions": total,
        "graded_submissions": graded,
        "avg_score": avg_score
    }