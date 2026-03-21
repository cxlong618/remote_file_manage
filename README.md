# Remote File Manager

为 Ubuntu 服务器开发的一个轻量级文件管理系统，支持通过浏览器浏览、上传和预览文件。

## 功能特性

- ✅ **文件浏览**：浏览服务器文件，支持路径快速导航
- ✅ **文件上传**：拖拽上传或点击上传文件
- ✅ **文件预览**：
  - Markdown 文档（带代码高亮）
  - 图片（支持缩放、旋转）
  - 视频（流式播放）
  - 音乐（音频播放）
- ✅ **用户认证**：简单的密码登录
- ✅ **响应式设计**：支持桌面和移动设备

## 技术栈

### 后端
- **FastAPI** - 现代化的 Python Web 框架
- **JWT** - 用户认证
- **aiofiles** - 异步文件操作

### 前端
- **Vue 3** - 渐进式 JavaScript 框架
- **Element Plus** - Vue 3 UI 组件库
- **Pinia** - 状态管理
- **Axios** - HTTP 客户端
- **marked + highlight.js** - Markdown 渲染

## 快速开始

### 🚀 一键启动（推荐）

```bash
# 1. 进入项目目录
cd remote_file_manage

# 2. 配置环境变量
cp backend/.env.example backend/.env
nano backend/.env  # 修改 USERNAME、PASSWORD、SECRET_KEY、ROOT_PATH

# 3. 一键启动
./start.sh
```

**启动脚本说明：**
- `start.sh` - 开发模式启动（前端热重载）
- `start-prod.sh` - 生产模式（构建前端 + 启动后端）
- `stop.sh` - 停止所有服务
- `restart.sh` - 重启服务

**访问地址：**
- 前端: http://localhost:5173
- API文档: http://localhost:8000/api/docs

---

### 手动启动（可选）

#### 后端设置

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env

# 编辑 .env 文件，设置以下配置：
# - SECRET_KEY: 生成随机密钥 (openssl rand -hex 32)
# - USERNAME: 登录用户名
# - PASSWORD: 登录密码
# - ROOT_PATH: 要管理的根目录（绝对路径）

# 运行后端
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### 前端设置

```bash
# 新开一个终端，进入前端目录
cd frontend

# 安装依赖
npm install

# 配置环境变量（可选）
echo "VITE_API_URL=http://localhost:8000" > .env

# 运行开发服务器
npm run dev
```

#### 访问应用

打开浏览器访问：`http://localhost:5173`

默认登录信息（在 `.env` 中配置）：
- 用户名：`admin`（或您设置的用户名）
- 密码：您在 `.env` 中设置的密码

## 生产部署

### 方式 1：直接运行

#### 后端

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

#### 前端

```bash
cd frontend
npm run build

# 使用 nginx 或其他 Web 服务器托管 dist 目录
```

### 方式 2：使用 Docker

```bash
# 构建并启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

## 配置说明

### 后端配置 (.env)

```bash
# 应用配置
APP_NAME=Remote File Manager
APP_VERSION=1.0.0

# 服务器配置
HOST=0.0.0.0
PORT=8000

# 文件系统配置
ROOT_PATH=/home/user/files  # 设置为您要管理的目录

# 安全配置
SECRET_KEY=your-secret-key-here  # 必须修改！
USERNAME=admin
PASSWORD=your-password-here  # 必须修改！

# CORS配置
CORS_ORIGINS=["http://localhost:5173","http://127.0.0.1:5173"]

# 文件上传配置
MAX_UPLOAD_SIZE=104857600  # 100MB
```

### 前端配置 (.env)

```bash
VITE_API_URL=http://localhost:8000
```

## API 文档

启动后端后，访问以下地址查看 API 文档：

- Swagger UI: `http://localhost:8000/api/docs`
- ReDoc: `http://localhost:8000/api/redoc`

## 项目结构

```
remote_file_manage/
├── backend/                 # 后端代码
│   ├── app/
│   │   ├── api/            # API 路由
│   │   ├── auth/           # 认证模块
│   │   ├── models/         # 数据模型
│   │   ├── services/       # 业务逻辑
│   │   ├── utils/          # 工具函数
│   │   ├── config.py       # 配置管理
│   │   ├── dependencies.py # 依赖注入
│   │   └── main.py         # 应用入口
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/                # 前端代码
│   ├── src/
│   │   ├── api/            # API 调用
│   │   ├── components/     # Vue 组件
│   │   ├── router/         # 路由配置
│   │   ├── stores/         # 状态管理
│   │   ├── types/          # TypeScript 类型
│   │   ├── utils/          # 工具函数
│   │   └── views/          # 页面组件
│   ├── package.json
│   └── vite.config.ts
│
└── README.md
```

## 安全建议

1. **修改默认密码**：在生产环境中必须修改 `.env` 中的默认密码
2. **生成强密钥**：使用 `openssl rand -hex 32` 生成随机的 `SECRET_KEY`
3. **限制访问范围**：通过防火墙或反向代理限制访问
4. **使用 HTTPS**：在生产环境中建议使用 nginx 配置 SSL
5. **定期备份**：备份重要文件和配置

## 常见问题

### 1. 无法访问文件

确保 `.env` 中的 `ROOT_PATH` 设置正确，并且应用有读取权限。

### 2. 上传失败

检查文件大小是否超过 `MAX_UPLOAD_SIZE` 限制。

### 3. CORS 错误

确保 `.env` 中的 `CORS_ORIGINS` 包含前端地址。

### 4. 预览不显示

某些文件格式可能不支持预览，尝试下载文件查看。

## 开发

### 后端开发

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

### 前端开发

```bash
cd frontend
npm run dev
```

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！
