#!/bin/bash
# Remote File Manager - 生产环境启动脚本

set -e

echo "🚀 启动 Remote File Manager (生产模式)..."
echo ""

# 检查 .env 文件
if [ ! -f "backend/.env" ]; then
    echo "❌ 错误: 未找到 backend/.env 文件"
    exit 1
fi

# 启动后端
echo "📦 启动后端服务..."
cd backend

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate
pip install -q -r requirements.txt

# 生产模式启动（不使用 --reload）
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4 > logs/backend.log 2>&1 &
BACKEND_PID=$!
echo "后端 PID: $BACKEND_PID"
echo $BACKEND_PID > .backend.pid

cd ..

# 构建前端
echo "🎨 构建前端..."
cd frontend

if [ ! -d "node_modules" ]; then
    npm install
fi

npm run build

echo ""
echo "✅ 构建完成！"
echo ""
echo "📍 部署说明:"
echo "   前端静态文件: frontend/dist/"
echo "   后端 API: http://localhost:8000"
echo ""
echo "📝 使用 Nginx 托管前端:"
echo "   sudo nano /etc/nginx/sites-available/remote-file-manager"
echo ""
echo "   添加以下配置:"
cat << 'EOF'
server {
    listen 80;
    root /opt/remote_file_manage/frontend/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        client_max_body_size 100M;
    }
}
EOF

echo ""
echo "   然后执行:"
echo "   sudo ln -s /etc/nginx/sites-available/remote-file-manager /etc/nginx/sites-enabled/"
echo "   sudo nginx -t"
echo "   sudo systemctl restart nginx"
echo ""
