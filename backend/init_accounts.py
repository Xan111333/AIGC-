import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import Base, engine, SessionLocal
from app.models import User, UserRole
from app.utils.security import get_password_hash
from sqlalchemy import text

print("=== 重置数据库 ===")
print()

with engine.connect() as conn:
    conn.execute(text("DROP TABLE IF EXISTS users"))
    conn.execute(text("DROP TABLE IF EXISTS tasks"))
    conn.execute(text("DROP TABLE IF EXISTS submissions"))
    conn.execute(text("DROP TABLE IF EXISTS generation_records"))
    conn.commit()
    print("已删除旧表")

Base.metadata.create_all(bind=engine)
print("已重新创建表")

db = SessionLocal()

DEFAULT_ACCOUNTS = [
    {
        "username": "student",
        "email": "student@example.com",
        "password": "student123",
        "role": UserRole.student,
        "full_name": "测试学生"
    },
    {
        "username": "teacher",
        "email": "teacher@example.com",
        "password": "teacher123",
        "role": UserRole.teacher,
        "full_name": "测试教师"
    },
    {
        "username": "admin",
        "email": "admin@example.com",
        "password": "admin123",
        "role": UserRole.admin,
        "full_name": "系统管理员"
    }
]

print()
print("=== 创建默认账号 ===")
print()

for account in DEFAULT_ACCOUNTS:
    hashed_password = get_password_hash(account["password"])
    user = User(
        username=account["username"],
        email=account["email"],
        hashed_password=hashed_password,
        role=account["role"],
        full_name=account["full_name"],
        is_active=True
    )
    db.add(user)
    role_name = account["role"].value
    print(f"[OK] 创建账号: {account['username']} / {account['password']} (角色: {role_name})")

db.commit()

print()
print("=== 账号恢复完成 ===")
print()
print("可用账号:")
print("  学生:   student / student123")
print("  教师:   teacher / teacher123")
print("  管理员: admin / admin123")
print()

db.close()
