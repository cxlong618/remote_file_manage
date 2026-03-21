from pathlib import Path
from typing import Optional
import os


def validate_path(path: str, root_path: str) -> Path:
    """
    验证并规范化路径

    Args:
        path: 用户提供的路径
        root_path: 根目录路径

    Returns:
        规范化后的Path对象

    Raises:
        ValueError: 路径不安全时
    """
    root = Path(root_path).resolve()

    # 处理空路径或相对路径
    if not path or path == "." or path == "/":
        return root

    # 解析用户路径
    user_path = Path(path)

    # 如果是相对路径，相对于根目录
    if not user_path.is_absolute():
        target_path = (root / user_path).resolve()
    else:
        target_path = user_path.resolve()

    # 安全检查：确保路径在根目录内
    if not is_safe_path(target_path, root):
        raise ValueError(f"访问被拒绝：路径超出允许的范围")

    return target_path


def is_safe_path(target_path: Path, root_path: Path) -> bool:
    """
    检查路径是否安全（不越界）

    Args:
        target_path: 目标路径
        root_path: 根路径

    Returns:
        是否安全
    """
    try:
        target_path.resolve().relative_to(root_path.resolve())
        return True
    except ValueError:
        return False


def get_relative_path(file_path: Path, root_path: Path) -> str:
    """
    获取相对于根目录的路径

    Args:
        file_path: 文件完整路径
        root_path: 根目录路径

    Returns:
        相对路径字符串
    """
    try:
        return str(file_path.resolve().relative_to(root_path.resolve()))
    except ValueError:
        return str(file_path)
