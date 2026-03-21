from pydantic_settings import BaseSettings
from typing import List
import json


class Settings(BaseSettings):
    """应用配置"""
    # 应用信息
    app_name: str = "Remote File Manager"
    app_version: str = "1.0.0"

    # 服务器配置
    host: str = "0.0.0.0"
    port: int = 8000

    # 文件系统配置
    root_path: str = "/home/user/files"

    # 安全配置
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24 * 7  # 7天

    # 用户认证
    username: str = "admin"
    password: str

    # CORS配置
    cors_origins: List[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]

    # 文件上传配置
    max_upload_size: int = 104857600  # 100MB

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def cors_origins_list(self) -> List[str]:
        """解析CORS origins"""
        if isinstance(self.cors_origins, str):
            try:
                return json.loads(self.cors_origins)
            except:
                return [self.cors_origins]
        return self.cors_origins


settings = Settings()
