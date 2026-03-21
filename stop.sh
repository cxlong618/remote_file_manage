#!/bin/bash
# Remote File Manager - 停止脚本

echo "🛑 正在停止 Remote File Manager..."
echo ""

# 停止后端
if [ -f "backend/.backend.pid" ]; then
    BACKEND_PID=$(cat backend/.backend.pid)
    if ps -p $BACKEND_PID > /dev/null 2>&1; then
        kill $BACKEND_PID 2>/dev/null && echo "✅ 后端已停止 (PID: $BACKEND_PID)"
    else
        echo "⚠️  后端进程不存在"
    fi
    rm -f backend/.backend.pid
else
    echo "⚠️  后端未运行"
fi

# 停止前端
if [ -f "frontend/.frontend.pid" ]; then
    FRONTEND_PID=$(cat frontend/.frontend.pid)
    if ps -p $FRONTEND_PID > /dev/null 2>&1; then
        kill $FRONTEND_PID 2>/dev/null && echo "✅ 前端已停止 (PID: $FRONTEND_PID)"
    else
        echo "⚠️  前端进程不存在"
    fi
    rm -f frontend/.frontend.pid
else
    echo "⚠️  前端未运行"
fi

# 清理可能残留的进程
pkill -f "uvicorn app.main:app" 2>/dev/null
pkill -f "vite.*5173" 2>/dev/null

echo ""
echo "✅ 所有服务已停止"
