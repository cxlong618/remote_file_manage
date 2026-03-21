# Remote File Manager - 开发执行计划

## 项目概述

为 Ubuntu 服务器开发一个轻量级文件管理系统，支持通过浏览器浏览、上传和预览文件。

## 需求分析

### 核心功能
1. ✅ 文件浏览：浏览本地文件，支持路径快速导航
2. ✅ 文件上传：支持拖拽上传和点击上传
3. ✅ 文件预览：Markdown、视频、音乐、图片
4. ✅ 用户认证：简单的密码登录
5. ✅ Web 访问：浏览器访问即可使用

### 技术方案
- **后端**：FastAPI + JWT + aiofiles
- **前端**：Vue 3 + Element Plus + Vite
- **部署**：支持手动部署和 Docker 部署

## 执行步骤

### ✅ 步骤 1：项目初始化
- 创建项目目录结构
- 配置后端依赖（requirements.txt）
- 配置前端依赖（package.json）
- 创建 .gitignore 和环境配置文件

### ✅ 步骤 2：后端认证模块
- 实现 JWT 认证逻辑
- 实现密码哈希验证
- 创建登录 API (/api/auth/login)
- 创建认证依赖注入

### ✅ 步骤 3：后端文件浏览服务
- 实现安全的路径遍历验证
- 实现文件列表获取
- 实现文件删除功能
- 创建文件 API (/api/files/*)

### ✅ 步骤 4：后端文件上传服务
- 实现分块上传
- 实现进度跟踪
- 创建上传 API (/api/upload)

### ✅ 步骤 5：后端文件预览服务
- 实现文本文件读取
- 实现媒体文件流式传输
- 创建预览 API (/api/files/preview/*)

### ✅ 步骤 6：前端项目基础
- 配置 Vite + TypeScript
- 安装 Vue Router、Pinia、Element Plus
- 配置 Axios 和 API 基础设置
- 创建路由和状态管理

### ✅ 步骤 7：前端登录页面
- 创建登录表单
- 实现 JWT 存储和验证
- 实现路由守卫

### ✅ 步骤 8：前端文件浏览器
- 实现文件列表展示
- 实现面包屑导航
- 实现路径快速跳转
- 实现文件操作（删除、预览）

### ✅ 步骤 9：前端文件上传组件
- 实现拖拽上传
- 实现进度条显示
- 实现多文件上传

### ✅ 步骤 10：前端文件预览组件
- 实现 Markdown 预览（marked + highlight.js）
- 实现图片预览（Element Plus Image）
- 实现音视频播放器（HTML5）

### ✅ 步骤 11：错误处理和优化
- 添加全局错误处理
- 添加加载状态指示
- 优化响应式布局

### ✅ 步骤 12：部署配置和文档
- 创建 Docker 配置
- 编写部署文档
- 编写使用说明

## 项目结构

```
remote_file_manage/
├── backend/                    # FastAPI 后端
│   ├── app/
│   │   ├── api/               # API 路由
│   │   ├── auth/              # 认证模块
│   │   ├── models/            # 数据模型
│   │   ├── services/          # 业务逻辑
│   │   ├── utils/             # 工具函数
│   │   ├── config.py          # 配置管理
│   │   ├── dependencies.py    # 依赖注入
│   │   └── main.py            # 应用入口
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
│
├── frontend/                   # Vue3 前端
│   ├── src/
│   │   ├── api/               # API 调用
│   │   ├── components/        # Vue 组件
│   │   ├── router/            # 路由配置
│   │   ├── stores/            # 状态管理
│   │   ├── types/             # TypeScript 类型
│   │   ├── utils/             # 工具函数
│   │   └── views/             # 页面组件
│   ├── package.json
│   ├── vite.config.ts
│   └── Dockerfile
│
├── docker-compose.yml          # Docker 编排
├── README.md                   # 项目文档
└── DEPLOYMENT.md               # 部署指南
```

## 核心功能实现

### 认证系统
- JWT Token 认证
- 密码 bcrypt 哈希
- 7 天 Token 有效期

### 文件浏览
- 安全的路径验证（防止目录遍历攻击）
- 文件列表排序（目录优先）
- 面包屑导航
- 快速路径跳转

### 文件上传
- 支持拖拽上传
- 100MB 大小限制
- 实时进度显示
- 自动重命名（避免覆盖）

### 文件预览
- Markdown：代码高亮、GitHub 风格
- 图片：缩放、旋转
- 视频：流式传输
- 音频：HTML5 播放器

## 安全措施

1. **路径遍历防护**：所有文件操作都经过路径验证
2. **JWT 认证**：除登录外所有 API 需要 Token
3. **CORS 配置**：限制允许的源
4. **文件类型限制**：上传时验证文件类型
5. **大小限制**：默认 100MB
6. **密码哈希**：使用 bcrypt

## 部署方式

### 手动部署
1. 后端：uvicorn + systemd
2. 前端：nginx 托管静态文件
3. 反向代理：nginx 配置

### Docker 部署
1. 使用 docker-compose 一键部署
2. 包含健康检查
3. 自动重启

## 开发环境启动

### 后端
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# 编辑 .env 文件
uvicorn app.main:app --reload
```

### 前端
```bash
cd frontend
npm install
npm run dev
```

## 完成状态

✅ 所有功能已开发完成
✅ 代码符合 SOLID、KISS、DRY、YAGNI 原则
✅ 包含完整的部署文档
✅ 支持 Docker 部署

## 下一步

1. 安装后端依赖并配置环境变量
2. 安装前端依赖并启动开发服务器
3. 测试所有功能
4. 部署到生产环境

## 技术亮点

- **异步处理**：后端使用 FastAPI 异步处理，提高并发能力
- **流式传输**：大文件和媒体文件使用流式传输，减少内存占用
- **类型安全**：前端使用 TypeScript，后端使用 Pydantic
- **响应式设计**：支持桌面和移动设备
- **模块化架构**：前后端分离，易于维护和扩展
