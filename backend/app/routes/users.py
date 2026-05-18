from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.user_service import get_users, get_user, update_user, delete_user
from ..schemas.user import UserResponse, UserUpdate
from ..utils.depends import get_current_active_user, require_admin
from ..models import User

router = APIRouter(prefix="/api/users", tags=["用户管理"])

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.get("/", response_model=list[UserResponse])
def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    return get_users(db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    return get_user(db, user_id)

@router.put("/{user_id}", response_model=UserResponse)
def update_user_by_id(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    return update_user(db, user_id, user_update)

@router.delete("/{user_id}", response_model=UserResponse)
def delete_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    return delete_user(db, user_id)