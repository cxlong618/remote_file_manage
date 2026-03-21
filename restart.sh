#!/bin/bash
# Remote File Manager - 重启脚本

echo "🔄 正在重启 Remote File Manager..."
echo ""

# 停止服务
./stop.sh

# 等待进程完全停止
sleep 3

# 启动服务
./start-server.sh
