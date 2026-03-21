#!/bin/bash
# Remote File Manager - 生产环境启动脚本（适合 SSH 远程部署）
# 特点：完全后台运行，不阻塞终端，适合 SSH 会话

set -e

echo "🚀 Remote File Manager - 生产环境启动"
echo "========================================"
echo ""

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 检查 .env 文件
if [ ! -f "backend/.env" ]; then
    echo "❌ 错误: 未找到 backend/.env 文件"
    echo "   请先复制并配置：cp backend/.env.example backend/.env"
    exit 1
fi

# 获取服务器 IP
SERVER_IP=$(hostname -I | awk '{print $1}')
echo "📍 服务器 IP: $SERVER_IP"
echo ""

# ==================== 后端启动 ====================
echo "📦 启动后端服务..."

cd backend

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "   创建 Python 虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装/更新依赖
echo "   安装 Python 依赖..."
pip install -q -r requirements.txt

# 创建日志目录
mkdir -p logs

# 检查是否已在运行
if [ -f .backend.pid ]; then
    OLD_PID=$(cat .backend.pid)
    if ps -p $OLD_PID > /dev/null 2>&1; then
        echo "   ⚠️  后端已在运行 (PID: $OLD_PID)"
        echo "   如需重启，请先运行: ./stop.sh"
    else
        echo "   清理旧的 PID 文件"
        rm .backend.pid
    fi
fi

# 启动后端（完全后台运行）
if [ ! -f .backend.pid ] || ! ps -p $(cat .backend.pid) > /dev/null 2>&1; then
    echo "   启动 FastAPI 服务..."
    nohup uvicorn app.main:app \
        --host 0.0.0.0 \
        --port 8000 \
        --workers 2 \
        --log-level info \
        >> logs/backend.log 2>&1 &

    BACKEND_PID=$!
    echo $BACKEND_PID > .backend.pid

    # 等待启动
    sleep 2

    if ps -p $BACKEND_PID > /dev/null; then
        echo "   ✅ 后端启动成功 (PID: $BACKEND_PID)"
    else
        echo "   ❌ 后端启动失败，查看日志:"
        echo "      tail -f backend/logs/backend.log"
        exit 1
    fi
fi

cd ..

# ==================== 前端构建和启动 ====================
echo ""
echo "🎨 启动前端服务..."

cd frontend

# 检查 node_modules
if [ ! -d "node_modules" ]; then
    echo "   安装前端依赖..."
    npm install --silent
fi

# 创建日志目录
mkdir -p logs

# 检查是否已在运行
if [ -f .frontend.pid ]; then
    OLD_PID=$(cat .frontend.pid)
    if ps -p $OLD_PID > /dev/null 2>&1; then
        echo "   ⚠️  前端已在运行 (PID: $OLD_PID)"
    else
        echo "   清理旧的 PID 文件"
        rm .frontend.pid
    fi
fi

# 启动前端（完全后台运行）
if [ ! -f .frontend.pid ] || ! ps -p $(cat .frontend.pid) > /dev/null 2>&1; then
    echo "   启动前端开发服务器..."
    nohup npm run dev >> logs/frontend.log 2>&1 &

    FRONTEND_PID=$!
    echo $FRONTEND_PID > .frontend.pid

    # 等待启动
    sleep 3

    if ps -p $FRONTEND_PID > /dev/null; then
        echo "   ✅ 前端启动成功 (PID: $FRONTEND_PID)"
    else
        echo "   ❌ 前端启动失败，查看日志:"
        echo "      tail -f frontend/logs/frontend.log"
        exit 1
    fi
fi

cd ..

# ==================== 启动完成 ====================
echo ""
echo "========================================"
echo "✅ 启动完成！"
echo ""
echo "📊 服务状态:"
echo "   后端 PID: $(cat backend/.backend.pid)"
echo "   前端 PID: $(cat frontend/.frontend.pid)"
echo ""
echo "📍 访问地址:"
echo "   本地前端: http://localhost:5173"
echo "   本地 API:  http://localhost:8000/api/docs"
echo ""
if [ ! -z "$SERVER_IP" ]; then
    echo "🌐 远程访问:"
    echo "   远程前端: http://$SERVER_IP:5173"
    echo "   远程 API:  http://$SERVER_IP:8000/api/docs"
    echo ""
fi

echo "📝 查看日志:"
echo "   后端: tail -f backend/logs/backend.log"
echo "   前端: tail -f frontend/logs/frontend.log"
echo ""

echo "🛠️  管理命令:"
echo "   查看状态: ./status.sh"
echo "   停止服务: ./stop.sh"
echo "   重启服务: ./restart.sh"
echo ""

echo "✨ 服务已在后台运行，可以安全关闭 SSH 连接"
echo "========================================"
