from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import FileResponse, StreamingResponse
from pathlib import Path
import mimetypes

from ..models.file import FileListResponse, FileInfo, DeleteResponse
from ..services.file_service import (
    list_files,
    get_file_info,
    delete_file,
    read_text_file,
    get_parent_path
)
from ..utils.preview import should_stream_preview, is_text_previewable
from ..dependencies import get_current_user
from ..config import settings

router = APIRouter(prefix="/api/files", tags=["文件操作"])


@router.get("/list", response_model=FileListResponse, summary="获取文件列表")
async def get_file_list(
    path: str = "",
    current_user: str = Depends(get_current_user)
):
    """
    获取指定目录的文件列表

    - **path**: 相对于根目录的路径，空字符串表示根目录
    """
    try:
        files = await list_files(path)
        parent_path = get_parent_path(path)

        return FileListResponse(
            current_path=path or "/",
            files=files,
            parent_path=parent_path
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


@router.get("/info", response_model=FileInfo, summary="获取文件信息")
async def get_info(
    path: str,
    current_user: str = Depends(get_current_user)
):
    """
    获取文件或目录的详细信息

    - **path**: 相对于根目录的路径
    """
    try:
        return await get_file_info(path)
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


@router.delete("/", response_model=DeleteResponse, summary="删除文件或目录")
async def delete_item(
    path: str,
    current_user: str = Depends(get_current_user)
):
    """
    删除指定的文件或目录

    - **path**: 相对于根目录的路径
    """
    try:
        await delete_file(path)
        return DeleteResponse(success=True, message="删除成功")
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/preview/text", summary="预览文本文件")
async def preview_text(
    path: str,
    current_user: str = Depends(get_current_user)
):
    """
    预览文本文件内容（包括Markdown）

    - **path**: 相对于根目录的路径
    """
    try:
        content = await read_text_file(path)
        return {"content": content}
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/preview/stream", summary="流式传输媒体文件")
async def preview_media(
    path: str,
    current_user: str = Depends(get_current_user)
):
    """
    流式传输音视频文件

    - **path**: 相对于根目录的路径
    """
    from ..utils.path import validate_path

    try:
        full_path = validate_path(path, settings.root_path)

        if not full_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="文件不存在"
            )

        if full_path.is_dir():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="无法预览目录"
            )

        # 获取MIME类型
        mime_type, _ = mimetypes.guess_type(str(full_path))
        if mime_type is None:
            mime_type = "application/octet-stream"

        # 流式返回文件
        def iterfile():
            with open(full_path, mode="rb") as f:
                while chunk := f.read(1024 * 1024):  # 1MB chunks
                    yield chunk

        return StreamingResponse(
            iterfile(),
            media_type=mime_type,
            headers={
                "Content-Disposition": f"inline; filename={full_path.name}",
                "Accept-Ranges": "bytes"
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/download", summary="下载文件")
async def download_file(
    path: str,
    current_user: str = Depends(get_current_user)
):
    """
    下载文件

    - **path**: 相对于根目录的路径
    """
    from ..utils.path import validate_path

    try:
        full_path = validate_path(path, settings.root_path)

        if not full_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="文件不存在"
            )

        if full_path.is_dir():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="无法下载目录"
            )

        return FileResponse(
            path=str(full_path),
            filename=full_path.name,
            media_type="application/octet-stream"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/download-folder", summary="下载文件夹（压缩）")
async def download_folder(
    path: str,
    current_user: str = Depends(get_current_user)
):
    """
    下载文件夹（ZIP格式）

    - **path**: 相对于根目录的路径
    """
    from ..utils.path import validate_path
    import zipfile
    import io

    try:
        full_path = validate_path(path, settings.root_path)

        if not full_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="文件夹不存在"
            )

        if not full_path.is_dir():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="不是文件夹"
            )

        # 计算文件夹大小（限制 500MB）
        total_size = 0
        MAX_SIZE = 500 * 1024 * 1024  # 500MB
        file_count = 0

        for file_path in full_path.rglob('*'):
            if file_path.is_file():
                total_size += file_path.stat().st_size
                file_count += 1
                if total_size > MAX_SIZE:
                    raise HTTPException(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        detail=f"文件夹过大（超过{MAX_SIZE // (1024*1024)}MB），无法下载"
                    )

        # 创建ZIP文件
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for file_path in full_path.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(full_path)
                    zip_file.write(file_path, arcname)

        zip_buffer.seek(0)

        return StreamingResponse(
            io.BytesIO(zip_buffer.read()),
            media_type="application/zip",
            headers={
                "Content-Disposition": f"attachment; filename={full_path.name}.zip"
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
