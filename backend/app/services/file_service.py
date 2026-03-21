from pathlib import Path
from typing import List, Optional
from datetime import datetime
import aiofiles
import os

from ..models.file import FileInfo
from ..utils.path import validate_path, get_relative_path, is_safe_path
from ..utils.preview import get_preview_type, is_previewable
from ..config import settings


async def list_files(path: str = "") -> List[FileInfo]:
    """
    列出目录中的文件和子目录

    Args:
        path: 相对于根目录的路径

    Returns:
        文件信息列表
    """
    # 验证并获取完整路径
    full_path = validate_path(path, settings.root_path)

    if not full_path.exists():
        raise FileNotFoundError(f"目录不存在: {path}")

    if not full_path.is_dir():
        raise NotADirectoryError(f"不是目录: {path}")

    files = []

    # 遍历目录
    for item in full_path.iterdir():
        try:
            # 获取文件信息
            stat = item.stat()
            is_dir = item.is_dir()

            # 判断是否可预览
            preview_type = None
            is_file_previewable = False
            if not is_dir:
                preview_type = get_preview_type(item.name)
                is_file_previewable = is_previewable(item.name)

            file_info = FileInfo(
                name=item.name,
                path=get_relative_path(item, Path(settings.root_path)),
                is_dir=is_dir,
                size=stat.st_size if not is_dir else 0,
                modified_time=datetime.fromtimestamp(stat.st_mtime),
                preview_type=preview_type,
                is_previewable=is_file_previewable
            )
            files.append(file_info)
        except (PermissionError, OSError) as e:
            # 跳过无权限访问的文件
            continue

    # 排序：目录在前，然后按名称排序
    files.sort(key=lambda x: (not x.is_dir, x.name.lower()))

    return files


async def get_file_info(path: str) -> FileInfo:
    """
    获取文件详细信息

    Args:
        path: 相对于根目录的路径

    Returns:
        文件信息
    """
    full_path = validate_path(path, settings.root_path)

    if not full_path.exists():
        raise FileNotFoundError(f"文件不存在: {path}")

    stat = full_path.stat()
    is_dir = full_path.is_dir()

    preview_type = None
    is_file_previewable = False
    if not is_dir:
        preview_type = get_preview_type(full_path.name)
        is_file_previewable = is_previewable(full_path.name)

    return FileInfo(
        name=full_path.name,
        path=get_relative_path(full_path, Path(settings.root_path)),
        is_dir=is_dir,
        size=stat.st_size if not is_dir else 0,
        modified_time=datetime.fromtimestamp(stat.st_mtime),
        preview_type=preview_type,
        is_previewable=is_file_previewable
    )


async def delete_file(path: str) -> bool:
    """
    删除文件或目录

    Args:
        path: 相对于根目录的路径

    Returns:
        是否成功
    """
    full_path = validate_path(path, settings.root_path)

    if not full_path.exists():
        raise FileNotFoundError(f"文件不存在: {path}")

    if full_path == Path(settings.root_path):
        raise PermissionError("不能删除根目录")

    try:
        if full_path.is_dir():
            import shutil
            shutil.rmtree(full_path)
        else:
            full_path.unlink()
        return True
    except Exception as e:
        raise Exception(f"删除失败: {str(e)}")


async def read_text_file(file_path: str, max_size: int = 10 * 1024 * 1024) -> str:
    """
    读取文本文件内容

    Args:
        file_path: 相对于根目录的文件路径
        max_size: 最大文件大小

    Returns:
        文件内容
    """
    full_path = validate_path(file_path, settings.root_path)

    if not full_path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")

    if full_path.is_dir():
        raise ValueError("不能读取目录")

    # 检查文件大小
    if full_path.stat().st_size > max_size:
        raise ValueError(f"文件过大（超过 {max_size // (1024*1024)}MB）")

    try:
        async with aiofiles.open(full_path, mode='r', encoding='utf-8') as f:
            return await f.read()
    except UnicodeDecodeError:
        # 尝试其他编码
        try:
            async with aiofiles.open(full_path, mode='r', encoding='gbk') as f:
                return await f.read()
        except:
            raise ValueError("无法解码文件内容")


def get_parent_path(path: str) -> Optional[str]:
    """
    获取父目录路径

    Args:
        path: 相对于根目录的路径

    Returns:
        父目录路径，根目录返回None
    """
    if not path or path == "." or path == "/":
        return None

    full_path = Path(path)
    parent = full_path.parent

    if parent == Path("."):
        return ""

    return str(parent)
