from pathlib import Path
from typing import Callable, Optional
import aiofiles
import shutil

from fastapi import UploadFile

from ..utils.path import validate_path
from ..config import settings


async def save_upload_file(
    upload_file: UploadFile,
    destination: str,
    progress_callback: Optional[Callable[[int], None]] = None
) -> dict:
    """
    保存上传的文件

    Args:
        upload_file: 上传的文件对象
        destination: 目标目录（相对于根目录）
        progress_callback: 进度回调函数

    Returns:
        包含文件信息的字典
    """
    # 验证目标路径
    dest_path = validate_path(destination, settings.root_path)

    if not dest_path.exists():
        raise FileNotFoundError(f"目标目录不存在: {destination}")

    if not dest_path.is_dir():
        raise NotADirectoryError(f"目标不是目录: {destination}")

    # 构建完整文件路径
    file_path = dest_path / upload_file.filename

    # 如果文件已存在，添加数字后缀
    counter = 1
    original_path = file_path
    while file_path.exists():
        stem = original_path.stem
        suffix = original_path.suffix
        file_path = dest_path / f"{stem}_{counter}{suffix}"
        counter += 1

    try:
        # 分块写入文件
        async with aiofiles.open(file_path, 'wb') as f:
            while chunk := await upload_file.read(1024 * 1024):  # 1MB chunks
                await f.write(chunk)
                if progress_callback:
                    await progress_callback(len(chunk))

        # 获取文件大小
        file_size = file_path.stat().st_size

        return {
            "file_path": str(file_path),
            "file_name": file_path.name,
            "file_size": file_size,
            "success": True
        }

    except Exception as e:
        # 如果失败，删除已上传的文件
        if file_path.exists():
            file_path.unlink()
        raise Exception(f"文件上传失败: {str(e)}")


async def upload_multiple_files(
    files: list[UploadFile],
    destination: str
) -> list[dict]:
    """
    上传多个文件

    Args:
        files: 上传的文件列表
        destination: 目标目录

    Returns:
        上传结果列表
    """
    results = []

    for file in files:
        try:
            result = await save_upload_file(file, destination)
            results.append({
                **result,
                "original_filename": file.filename,
                "message": "上传成功"
            })
        except Exception as e:
            results.append({
                "success": False,
                "original_filename": file.filename,
                "message": str(e)
            })

    return results
