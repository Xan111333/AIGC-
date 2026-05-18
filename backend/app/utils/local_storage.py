import os
import uuid
from datetime import datetime
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class LocalStorageSettings(BaseSettings):
    STORAGE_ROOT: str = "storage"
    STORAGE_URL_PREFIX: str = "/api/files"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = LocalStorageSettings()

storage_root = Path(settings.STORAGE_ROOT)

def init_storage():
    try:
        storage_root.mkdir(parents=True, exist_ok=True)
        (storage_root / "generated").mkdir(parents=True, exist_ok=True)
        (storage_root / "images").mkdir(parents=True, exist_ok=True)
        (storage_root / "audio").mkdir(parents=True, exist_ok=True)
        (storage_root / "uploads").mkdir(parents=True, exist_ok=True)
        print(f"本地存储目录初始化完成: {storage_root.absolute()}")
    except Exception as e:
        print(f"初始化本地存储目录失败: {e}")

def _get_full_path(object_name: str) -> Path:
    """
    获取文件的完整路径
    """
    full_path = (storage_root / object_name).resolve()
    if not str(full_path).startswith(str(storage_root.resolve())):
        raise ValueError("无效的文件路径")
    return full_path

def upload_file(file_data: bytes, filename: str, content_type: str = "application/octet-stream") -> str:
    """
    上传文件到本地存储
    返回文件的访问 URL
    """
    try:
        object_name = f"uploads/{uuid.uuid4()}-{filename}"
        full_path = _get_full_path(object_name)
        
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_bytes(file_data)
        
        return f"{settings.STORAGE_URL_PREFIX}/{object_name}"
    except Exception as e:
        raise Exception(f"上传文件失败: {e}")

def upload_bytes(file_data: bytes, object_name: str, content_type: str = "application/octet-stream") -> str:
    """
    上传字节数据到本地存储（指定对象名称）
    返回文件的访问 URL
    """
    try:
        full_path = _get_full_path(object_name)
        
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_bytes(file_data)
        
        return f"{settings.STORAGE_URL_PREFIX}/{object_name}"
    except Exception as e:
        raise Exception(f"上传文件失败: {e}")

def upload_image(image_data: bytes, filename: str) -> str:
    """
    上传图片到本地存储
    返回文件的访问 URL
    """
    try:
        object_name = f"images/{uuid.uuid4()}-{filename}"
        full_path = _get_full_path(object_name)
        
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_bytes(image_data)
        
        return f"{settings.STORAGE_URL_PREFIX}/{object_name}"
    except Exception as e:
        raise Exception(f"上传图片失败: {e}")

def get_file_url(object_name: str) -> str:
    """
    获取文件的访问 URL
    """
    return f"{settings.STORAGE_URL_PREFIX}/{object_name}"

def download_file(object_name: str) -> bytes:
    """
    从本地存储下载文件
    返回文件字节数据
    """
    try:
        full_path = _get_full_path(object_name)
        if not full_path.exists():
            raise Exception(f"文件不存在: {object_name}")
        return full_path.read_bytes()
    except Exception as e:
        raise Exception(f"下载文件失败: {e}")

def delete_file(object_name: str):
    """
    从本地存储删除文件
    """
    try:
        full_path = _get_full_path(object_name)
        if full_path.exists():
            full_path.unlink()
    except Exception as e:
        raise Exception(f"删除文件失败: {e}")

def file_exists(object_name: str) -> bool:
    """
    检查文件是否存在
    """
    try:
        full_path = _get_full_path(object_name)
        return full_path.exists()
    except Exception:
        return False
