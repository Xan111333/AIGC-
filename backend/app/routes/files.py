from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from ..utils.local_storage import download_file, upload_file
from ..utils.depends import get_current_active_user
from ..models import User
from fastapi import File, UploadFile
import io

router = APIRouter(prefix="/api/files", tags=["文件管理"])

@router.get("/{object_name:path}")
def get_file(object_name: str, current_user: User = Depends(get_current_active_user)):
    try:
        file_data = download_file(object_name)
        return StreamingResponse(io.BytesIO(file_data), media_type="application/octet-stream")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/upload")
async def upload_file_endpoint(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user)
):
    try:
        file_data = await file.read()
        file_url = upload_file(file_data, file.filename, file.content_type)
        return {"file_url": file_url}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))