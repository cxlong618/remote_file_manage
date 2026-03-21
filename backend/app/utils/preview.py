from pathlib import Path
from typing import Optional


# 预览支持的文件类型
PREVIEW_TYPES = {
    "markdown": [".md", ".markdown"],
    "text": [".txt", ".log", ".json", ".xml", ".yaml", ".yml", ".csv", ".ini", ".conf"],
    "image": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".ico"],
    "video": [".mp4", ".avi", ".mov", ".wmv", ".flv", ".webm", ".mkv", ".m4v"],
    "audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a", ".wma"],
}

# 最大预览文件大小（文本文件）
MAX_PREVIEW_SIZE = 10 * 1024 * 1024  # 10MB


def get_preview_type(filename: str) -> Optional[str]:
    """
    获取文件的预览类型

    Args:
        filename: 文件名

    Returns:
        预览类型或None
    """
    ext = Path(filename).suffix.lower()

    for preview_type, extensions in PREVIEW_TYPES.items():
        if ext in extensions:
            return preview_type

    return None


def is_previewable(filename: str) -> bool:
    """
    判断文件是否可以预览

    Args:
        filename: 文件名

    Returns:
        是否可预览
    """
    return get_preview_type(filename) is not None


def is_text_previewable(filename: str) -> bool:
    """
    判断是否为文本预览类型

    Args:
        filename: 文件名

    Returns:
        是否为文本类型
    """
    preview_type = get_preview_type(filename)
    return preview_type in ["markdown", "text"]


def is_media_previewable(filename: str) -> bool:
    """
    判断是否为媒体预览类型

    Args:
        filename: 文件名

    Returns:
        是否为媒体类型
    """
    preview_type = get_preview_type(filename)
    return preview_type in ["image", "video", "audio"]


def should_stream_preview(filename: str) -> bool:
    """
    判断是否需要流式传输预览（音视频）

    Args:
        filename: 文件名

    Returns:
        是否需要流式传输
    """
    preview_type = get_preview_type(filename)
    return preview_type in ["video", "audio"]
