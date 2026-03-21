# 快速启动指南

## 🚀 最快启动方式（推荐）

### 1️⃣ 配置环境变量
```bash
cd remote_file_manage
cp backend/.env.example backend/.env
nano backend/.env  # 必须修改：USERNAME、PASSWORD、SECRET_KEY、ROOT_PATH
```

### 2️⃣ 一键启动
```bash
./start.sh
```

### 3️⃣ 访问应用
- 前端: http://localhost:5173
- API: http://localhost:8000/api/docs

---

## 📋 启动脚本说明

| 脚本 | 说明 | 使用场景 |
|------|------|---------|
| `./start.sh` | 开发模式（前端热重载） | 日常开发测试 |
| `./start-prod.sh` | 生产模式（构建前端） | 服务器部署 |
| `./stop.sh` | 停止所有服务 | 停止应用 |
| `./restart.sh` | 重启服务 | 更新后重启 |

---

## 🛑 停止服务

```bash
./stop.sh
```

或手动停止：
```bash
# 查找进程
ps aux | grep uvicorn
ps aux | grep vite

# 杀死进程
kill <PID>
```

---

## 🔧 常见问题

### Q1: 启动失败？
```bash
# 检查端口是否被占用
lsof -i :8000
lsof -i :5173

# 杀死占用进程
kill -9 <PID>
```

### Q2: 权限错误？
```bash
# 给脚本添加执行权限
chmod +x *.sh
```

### Q3: 依赖安装失败？
```bash
# 后端
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 前端
cd frontend
rm -rf node_modules
npm install
```

---

## 📊 系统服务（生产环境）

### 安装服务
```bash
sudo cp remote-file-manager.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable remote-file-manager
sudo systemctl start remote-file-manager
```

### 管理服务
```bash
# 启动
sudo systemctl start remote-file-manager

# 停止
sudo systemctl stop remote-file-manager

# 重启
sudo systemctl restart remote-file-manager

# 查看状态
sudo systemctl status remote-file-manager

# 查看日志
sudo journalctl -u remote-file-manager -f
```

---

## 🌐 Nginx 配置（生产环境）

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端静态文件
    location / {
        root /opt/remote_file_manage/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # 后端 API
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        client_max_body_size 100M;
    }
}
```

---

## 💡 开发技巧

### 后台运行
```bash
# 后端后台运行
cd backend
source venv/bin/activate
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 > backend.log 2>&1 &

# 前端后台运行
cd frontend
nohup npm run dev > frontend.log 2>&1 &
```

### 查看日志
```bash
# 后端
tail -f backend.log

# 前端
tail -f frontend.log
```

---

## ✅ 检查清单

部署前检查：
- [ ] 修改 `.env` 中的 `SECRET_KEY`
- [ ] 修改 `.env` 中的 `USERNAME` 和 `PASSWORD`
- [ ] 设置正确的 `ROOT_PATH`
- [ ] 配置 `CORS_ORIGINS`
- [ ] 设置 `MAX_UPLOAD_SIZE`
- [ ] 测试登录功能
- [ ] 测试文件浏览
- [ ] 测试文件上传
- [ ] 测试文件预览

---

## 📞 获取帮助

```bash
# 查看后端日志
cd backend
tail -f logs/backend.log

# 查看前端日志
cd frontend
cat npm-debug.log
```
