from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File
from typing import List

from ..models.file import UploadResponse
from ..services.upload_service import save_upload_file, upload_multiple_files
from ..dependencies import get_current_user
from ..config import settings

router = APIRouter(prefix="/api/upload", tags=["文件上传"])


@router.post("/", response_model=UploadResponse, summary="上传单个文件")
async def upload_file(
    file: UploadFile = File(...),
    path: str = "",
    current_user: str = Depends(get_current_user)
):
    """
    上传单个文件到指定目录

    - **file**: 要上传的文件
    - **path**: 目标目录（相对于根目录），空字符串表示根目录
    """
    # 检查文件大小
    if file.size and file.size > settings.max_upload_size:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"文件过大（最大 {settings.max_upload_size // (1024*1024)}MB）"
        )

    try:
        result = await save_upload_file(file, path)
        return UploadResponse(
            success=True,
            message="上传成功",
            file_path=result["file_path"],
            file_name=result["file_name"],
            file_size=result["file_size"]
        )
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/multiple", summary="上传多个文件")
async def upload_files(
    files: List[UploadFile] = File(...),
    path: str = "",
    current_user: str = Depends(get_current_user)
):
    """
    上传多个文件到指定目录

    - **files**: 要上传的文件列表
    - **path**: 目标目录（相对于根目录），空字符串表示根目录
    """
    try:
        results = await upload_multiple_files(files, path)
        return {
            "success": all(r["success"] for r in results),
            "results": results
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
