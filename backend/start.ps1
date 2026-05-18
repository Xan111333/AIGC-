Write-Host "启动 AIGC 实训平台后端服务..."

Write-Host "1. 初始化 MinIO Bucket..."
python -c "from app.utils.minio_client import init_bucket; init_bucket()"

Write-Host "2. 启动 FastAPI 服务..."
uvicorn main:app --host 0.0.0.0 --port 8000 --reload