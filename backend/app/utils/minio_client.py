from pydantic_settings import BaseSettings, SettingsConfigDict

class MinioSettings(BaseSettings):
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET_NAME: str = "aigc-training"
    MINIO_SECURE: bool = False
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = MinioSettings()

try:
    from minio import Minio
    from minio.error import S3Error
    import io
    import uuid

    minio_client = Minio(
        settings.MINIO_ENDPOINT,
        access_key=settings.MINIO_ACCESS_KEY,
        secret_key=settings.MINIO_SECRET_KEY,
        secure=settings.MINIO_SECURE
    )

    def init_bucket():
        try:
            if not minio_client.bucket_exists(settings.MINIO_BUCKET_NAME):
                minio_client.make_bucket(settings.MINIO_BUCKET_NAME)
                print(f"Bucket {settings.MINIO_BUCKET_NAME} created successfully")
            else:
                print(f"Bucket {settings.MINIO_BUCKET_NAME} already exists")
        except S3Error as e:
            print(f"Error initializing bucket: {e}")

    def upload_file(file_data: bytes, filename: str, content_type: str = "application/octet-stream") -> str:
        try:
            object_name = f"{uuid.uuid4()}-{filename}"
            minio_client.put_object(
                settings.MINIO_BUCKET_NAME,
                object_name,
                io.BytesIO(file_data),
                len(file_data),
                content_type=content_type
            )
            return f"/api/files/{object_name}"
        except S3Error as e:
            raise Exception(f"Failed to upload file: {e}")

    def upload_image(image_data: bytes, filename: str) -> str:
        try:
            object_name = f"images/{uuid.uuid4()}-{filename}"
            minio_client.put_object(
                settings.MINIO_BUCKET_NAME,
                object_name,
                io.BytesIO(image_data),
                len(image_data),
                content_type="image/png"
            )
            return f"/api/files/{object_name}"
        except S3Error as e:
            raise Exception(f"Failed to upload image: {e}")

    def get_file_url(object_name: str) -> str:
        try:
            url = minio_client.presigned_get_object(settings.MINIO_BUCKET_NAME, object_name, expires=3600)
            return url
        except S3Error as e:
            raise Exception(f"Failed to get file URL: {e}")

    def download_file(object_name: str) -> bytes:
        try:
            response = minio_client.get_object(settings.MINIO_BUCKET_NAME, object_name)
            return response.read()
        except S3Error as e:
            raise Exception(f"Failed to download file: {e}")

    def delete_file(object_name: str):
        try:
            minio_client.remove_object(settings.MINIO_BUCKET_NAME, object_name)
        except S3Error as e:
            raise Exception(f"Failed to delete file: {e}")
except ImportError:
    print("MinIO 库未安装，已跳过初始化")
    minio_client = None
    
    def init_bucket():
        pass
    
    def upload_file(file_data: bytes, filename: str, content_type: str = "application/octet-stream") -> str:
        raise Exception("MinIO 未配置")
    
    def upload_image(image_data: bytes, filename: str) -> str:
        raise Exception("MinIO 未配置")
    
    def get_file_url(object_name: str) -> str:
        raise Exception("MinIO 未配置")
    
    def download_file(object_name: str) -> bytes:
        raise Exception("MinIO 未配置")
    
    def delete_file(object_name: str):
        raise Exception("MinIO 未配置")
