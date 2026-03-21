#!/bin/bash
# Remote File Manager - 快速启动脚本

set -e

echo "🚀 正在启动 Remote File Manager..."
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python3，请先安装"
    exit 1
fi

# 检查 Node.js
if ! command -v npm &> /dev/null; then
    echo "❌ 错误: 未找到 npm，请先安装 Node.js"
    exit 1
fi

# 检查 .env 文件
if [ ! -f "backend/.env" ]; then
    echo "⚠️  未找到 backend/.env 文件，从示例复制..."
    cp backend/.env.example backend/.env
    echo "❗ 请编辑 backend/.env 文件，设置您的配置！"
    echo ""
    read -p "按 Enter 继续（确保已修改 .env 文件）..."
fi

# 启动后端
echo "📦 启动后端服务..."
cd backend

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "创建 Python 虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
echo "安装 Python 依赖..."
pip install -q -r requirements.txt

# 启动后端（后台运行）
echo "启动 FastAPI 服务（端口 8000）..."
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 > /dev/null 2>&1 &
BACKEND_PID=$!
echo "后端 PID: $BACKEND_PID"

cd ..

# 启动前端
echo "🎨 启动前端服务..."
cd frontend

# 检查 node_modules
if [ ! -d "node_modules" ]; then
    echo "安装前端依赖..."
    npm install -q
fi

# 开发模式启动
echo "启动前端开发服务器（端口 5173）..."
npm run dev &
FRONTEND_PID=$!

echo ""
echo "✅ 启动完成！"
echo ""
echo "📍 访问地址:"
echo "   前端: http://localhost:5173"
echo "   API:  http://localhost:8000/api/docs"
echo ""
echo "💡 登录信息请查看 backend/.env 文件"
echo ""
echo "⏹️  停止服务:"
echo "   kill $BACKEND_PID $FRONTEND_PID"
echo "   或运行: ./stop.sh"
echo ""

# 保存 PID
echo $BACKEND_PID > .backend.pid
echo $FRONTEND_PID > .frontend.pid

# 等待用户输入
echo "按 Ctrl+C 停止所有服务"
wait
