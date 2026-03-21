#!/bin/bash
# Remote File Manager - 查看服务状态

echo "📊 Remote File Manager - 服务状态"
echo "=================================="
echo ""

# 获取服务器 IP
SERVER_IP=$(hostname -I | awk '{print $1}')

# 检查后端
echo "📦 后端服务:"
if [ -f "backend/.backend.pid" ]; then
    BACKEND_PID=$(cat backend/.backend.pid)
    if ps -p $BACKEND_PID > /dev/null 2>&1; then
        echo "   ✅ 运行中 (PID: $BACKEND_PID)"
        echo "   端口: 8000"
        echo "   日志: tail -f backend/logs/backend.log"
        echo "   远程访问: http://$SERVER_IP:8000/api/docs"
    else
        echo "   ❌ 未运行 (PID 文件存在但进程不存在)"
        echo "   请运行: ./start-server.sh"
    fi
else
    echo "   ❌ 未运行 (无 PID 文件)"
    echo "   请运行: ./start-server.sh"
fi

echo ""

# 检查前端
echo "🎨 前端服务:"
if [ -f "frontend/.frontend.pid" ]; then
    FRONTEND_PID=$(cat frontend/.frontend.pid)
    if ps -p $FRONTEND_PID > /dev/null 2>&1; then
        echo "   ✅ 运行中 (PID: $FRONTEND_PID)"
        echo "   端口: 5173"
        echo "   日志: tail -f frontend/logs/frontend.log"
        echo "   远程访问: http://$SERVER_IP:5173"
    else
        echo "   ❌ 未运行 (PID 文件存在但进程不存在)"
        echo "   请运行: ./start-server.sh"
    fi
else
    echo "   ❌ 未运行 (无 PID 文件)"
    echo "   请运行: ./start-server.sh"
fi

echo ""

# 检查端口占用
echo "🔍 端口占用情况:"
if command -v netstat &> /dev/null; then
    echo "   端口 8000:"
    netstat -tuln | grep 8000 && echo "   ✅ 正在监听" || echo "   ❌ 未监听"
    echo "   端口 5173:"
    netstat -tuln | grep 5173 && echo "   ✅ 正在监听" || echo "   ❌ 未监听"
fi

echo ""
echo "=================================="
