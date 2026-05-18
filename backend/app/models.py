import enum
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum, Float, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class UserRole(enum.Enum):
    student = "student"
    teacher = "teacher"
    admin = "admin"

class GenerateType(enum.Enum):
    text = "text"
    image = "image"
    video = "video"
    audio = "audio"

class TaskStatus(enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole, values_callable=lambda x: [e.value for e in x]), default=UserRole.student, nullable=False)
    full_name = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    tasks = relationship("Task", back_populates="teacher")
    submissions = relationship("Submission", back_populates="student")
    generation_records = relationship("GenerationRecord", back_populates="user")

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    type = Column(Enum(GenerateType, values_callable=lambda x: [e.value for e in x]), nullable=False)
    requirements = Column(Text)
    deadline = Column(DateTime)
    teacher_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    teacher = relationship("User", back_populates="tasks")
    submissions = relationship("Submission", back_populates="task")

class Submission(Base):
    __tablename__ = "submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    student_id = Column(Integer, ForeignKey("users.id"))
    file_path = Column(String(500))
    generated_content = Column(Text)
    status = Column(Enum(TaskStatus, values_callable=lambda x: [e.value for e in x]), default=TaskStatus.pending)
    score = Column(Float)
    comment = Column(Text)
    submitted_at = Column(DateTime, default=datetime.utcnow)
    graded_at = Column(DateTime)
    
    task = relationship("Task", back_populates="submissions")
    student = relationship("User", back_populates="submissions")

class GenerationRecord(Base):
    __tablename__ = "generation_records"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(Enum(GenerateType, values_callable=lambda x: [e.value for e in x]), nullable=False)
    prompt = Column(Text, nullable=False)
    params = Column(Text)
    result_url = Column(String(500))
    status = Column(Enum(TaskStatus, values_callable=lambda x: [e.value for e in x]), default=TaskStatus.pending)
    error_message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    
    user = relationship("User", back_populates="generation_records")
