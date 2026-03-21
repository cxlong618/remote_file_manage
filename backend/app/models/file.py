from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime


class FileInfo(BaseModel):
    """文件信息模型"""
    name: str
    path: str
    is_dir: bool
    size: int
    modified_time: datetime
    preview_type: Optional[str] = None
    is_previewable: bool = False


class FileListResponse(BaseModel):
    """文件列表响应"""
    current_path: str
    files: list[FileInfo]
    parent_path: Optional[str] = None


class DeleteResponse(BaseModel):
    """删除响应"""
    success: bool
    message: str


class UploadResponse(BaseModel):
    """上传响应"""
    success: bool
    message: str
    file_path: str
    file_name: str
    file_size: int


class PreviewResponse(BaseModel):
    """预览响应"""
    content_type: str
    content: Optional[str] = None
    file_url: Optional[str] = None
