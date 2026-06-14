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


class BatchDeleteRequest(BaseModel):
    """批量删除请求"""
    paths: list[str]


class BatchDeleteResponse(BaseModel):
    """批量删除响应"""
    success: bool
    deleted: int
    failed: int
    errors: list[str] = []


class BatchMoveRequest(BaseModel):
    """批量移动请求"""
    paths: list[str]
    target_path: str
    overwrite: bool = False


class BatchMoveResponse(BaseModel):
    """批量移动响应"""
    success: bool
    moved: int
    failed: int
    errors: list[str] = []


class BatchDownloadRequest(BaseModel):
    """批量下载请求"""
    paths: list[str]


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
