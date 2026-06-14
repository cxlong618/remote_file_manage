from pathlib import Path
from typing import List, Optional, Tuple
from datetime import datetime
import aiofiles
import os
import shutil

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


async def batch_delete_files(paths: List[str]) -> Tuple[int, int, List[str]]:
    """
    批量删除文件

    Args:
        paths: 相对于根目录的文件路径列表

    Returns:
        (成功删除数量, 失败数量, 错误信息列表)
    """
    deleted = 0
    failed = 0
    errors = []

    for path in paths:
        try:
            full_path = validate_path(path, settings.root_path)

            if not full_path.exists():
                failed += 1
                errors.append(f"{path}: 文件不存在")
                continue

            if full_path == Path(settings.root_path):
                failed += 1
                errors.append(f"{path}: 不能删除根目录")
                continue

            if full_path.is_dir():
                shutil.rmtree(full_path)
            else:
                full_path.unlink()
            deleted += 1
        except PermissionError:
            failed += 1
            errors.append(f"{path}: 权限不足")
        except Exception as e:
            failed += 1
            errors.append(f"{path}: {str(e)}")

    return deleted, failed, errors


async def batch_move_files(paths: List[str], target_path: str, overwrite: bool = False) -> Tuple[int, int, List[str]]:
    """
    批量移动文件

    Args:
        paths: 相对于根目录的文件路径列表
        target_path: 目标目录路径（相对于根目录）
        overwrite: 是否覆盖已存在的文件

    Returns:
        (成功移动数量, 失败数量, 错误信息列表)
    """
    moved = 0
    failed = 0
    errors = []

    try:
        target_full_path = validate_path(target_path, settings.root_path)

        if not target_full_path.exists():
            failed = len(paths)
            errors.append(f"目标目录不存在: {target_path}")
            return moved, failed, errors

        if not target_full_path.is_dir():
            failed = len(paths)
            errors.append(f"目标不是目录: {target_path}")
            return moved, failed, errors

        for path in paths:
            try:
                source_path = validate_path(path, settings.root_path)

                if not source_path.exists():
                    failed += 1
                    errors.append(f"{path}: 源文件不存在")
                    continue

                target_file_path = target_full_path / source_path.name

                # 检查目标是否已存在
                if target_file_path.exists():
                    if not overwrite:
                        failed += 1
                        errors.append(f"{path}: 目标位置已存在同名文件")
                        continue

                    # 覆盖已存在的文件/目录
                    if target_file_path.is_dir():
                        shutil.rmtree(target_file_path)
                    else:
                        target_file_path.unlink()

                # 执行移动
                shutil.move(str(source_path), str(target_file_path))
                moved += 1
            except PermissionError:
                failed += 1
                errors.append(f"{path}: 权限不足")
            except Exception as e:
                failed += 1
                errors.append(f"{path}: {str(e)}")

    except FileNotFoundError:
        failed = len(paths)
        errors.append(f"目标目录不存在: {target_path}")
    except Exception as e:
        failed = len(paths)
        errors.append(f"目标目录错误: {str(e)}")

    return moved, failed, errors


async def batch_download_files(paths: List[str]) -> Tuple[Path, int]:
    """
    批量下载文件（创建ZIP）

    Args:
        paths: 相对于根目录的文件路径列表

    Returns:
        (ZIP文件路径, 文件数量)
    """
    import zipfile
    import tempfile
    import uuid

    # 创建临时ZIP文件
    temp_dir = Path(tempfile.gettempdir())
    zip_path = temp_dir / f"batch_download_{uuid.uuid4().hex}.zip"

    file_count = 0

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for path in paths:
            try:
                full_path = validate_path(path, settings.root_path)

                if not full_path.exists():
                    continue

                if full_path.is_file():
                    # 添加单个文件
                    arcname = full_path.name
                    zip_file.write(full_path, arcname)
                    file_count += 1
                elif full_path.is_dir():
                    # 添加整个目录
                    for file_path in full_path.rglob('*'):
                        if file_path.is_file():
                            arcname = Path(full_path.name) / file_path.relative_to(full_path)
                            zip_file.write(file_path, arcname)
                            file_count += 1
            except Exception:
                continue

    return zip_path, file_count
