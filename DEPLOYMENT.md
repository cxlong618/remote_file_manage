# 部署指南

本文档详细说明如何在 Ubuntu 服务器上部署 Remote File Manager。

## 前置要求

- Ubuntu 20.04+
- Python 3.8+
- Node.js 16+
- Nginx（可选，用于生产环境）

## 方式 1：手动部署

### 步骤 1：安装依赖

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装 Python 和 pip
sudo apt install python3 python3-pip python3-venv -y

# 安装 Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs -y

# 安装 Nginx
sudo apt install nginx -y
```

### 步骤 2：克隆项目

```bash
cd /opt
sudo git clone <your-repo-url> remote_file_manage
cd remote_file_manage

# 设置权限
sudo chown -R $USER:$USER /opt/remote_file_manage
```

### 步骤 3：配置后端

```bash
cd backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 生成密钥
SECRET_KEY=$(openssl rand -hex 32)
echo "SECRET_KEY=$SECRET_KEY" >> .env

# 配置环境变量
nano .env
```

在 `.env` 文件中设置：

```bash
APP_NAME=Remote File Manager
HOST=0.0.0.0
PORT=8000

# 设置您要管理的根目录
ROOT_PATH=/home/username/files

# 设置用户名和密码
USERNAME=admin
PASSWORD=your-secure-password

# 其他配置...
SECRET_KEY=<生成的密钥>
```

### 步骤 4：创建管理目录

```bash
# 创建文件管理目录
mkdir -p /home/username/files

# 设置权限
chmod 755 /home/username/files
```

### 步骤 5：测试后端

```bash
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

访问 `http://your-server-ip:8000/api/docs` 测试 API。

### 步骤 6：构建前端

```bash
cd ../frontend

# 安装依赖
npm install

# 构建生产版本
npm run build

# 构建 output 在 dist/ 目录
```

### 步骤 7：配置 Nginx

创建 Nginx 配置文件：

```bash
sudo nano /etc/nginx/sites-available/remote-file-manager
```

添加以下配置：

```nginx
server {
    listen 80;
    server_name your-domain.com;  # 或服务器 IP

    # 前端静态文件
    location / {
        root /opt/remote_file_manage/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # 后端 API 代理
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # 支持大文件上传
        client_max_body_size 100M;
    }

    # 媒体文件流式传输
    location /api/files/preview/stream {
        proxy_pass http://127.0.0.1:8000;
        proxy_buffering off;
        proxy_set_header Host $host;
    }
}
```

启用配置：

```bash
sudo ln -s /etc/nginx/sites-available/remote-file-manager /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 步骤 8：创建 Systemd 服务

创建后端服务文件：

```bash
sudo nano /etc/systemd/system/remote-file-manager.service
```

添加以下内容：

```ini
[Unit]
Description=Remote File Manager Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/remote_file_manage/backend
Environment="PATH=/opt/remote_file_manage/backend/venv/bin"
ExecStart=/opt/remote_file_manage/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo systemctl daemon-reload
sudo systemctl enable remote-file-manager
sudo systemctl start remote-file-manager
sudo systemctl status remote-file-manager
```

### 步骤 9：配置防火墙

```bash
# 允许 HTTP
sudo ufw allow 'Nginx Full'

# 或允许特定端口
sudo ufw allow 80
sudo ufw allow 443

# 启用防火墙
sudo ufw enable
```

### 步骤 10：配置 HTTPS（可选但推荐）

使用 Let's Encrypt 免费证书：

```bash
# 安装 Certbot
sudo apt install certbot python3-certbot-nginx -y

# 获取证书
sudo certbot --nginx -d your-domain.com

# 自动续期
sudo certbot renew --dry-run
```

## 方式 2：Docker 部署

### 创建 Docker Compose 配置

项目根目录下已包含 `docker-compose.yml` 文件。

### 构建和启动

```bash
# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

## 安全加固

### 1. 修改默认端口

修改 Nginx 配置，使用非标准端口。

### 2. 启用 Basic Auth

```bash
# 创建密码文件
sudo htpasswd -c /etc/nginx/.htpasswd admin

# 修改 Nginx 配置
auth_basic "Restricted Access";
auth_basic_user_file /etc/nginx/.htpasswd;
```

### 3. 限制访问 IP

在 Nginx 配置中添加：

```nginx
allow 192.168.1.0/24;  # 允许的 IP 段
deny all;
```

### 4. 定期更新

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 更新依赖
cd /opt/remote_file_manage/backend
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 监控和维护

### 查看日志

```bash
# 后端日志
sudo journalctl -u remote-file-manager -f

# Nginx 日志
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### 备份

```bash
# 备份配置
tar -czf backup-$(date +%Y%m%d).tar.gz /opt/remote_file_manage/backend/.env

# 备份文件（根据需要）
rsync -avz /home/username/files /backup/location
```

## 性能优化

### 1. 启用 Gzip 压缩

在 Nginx 配置中添加：

```nginx
gzip on;
gzip_types text/plain text/css application/json application/javascript;
```

### 2. 启用缓存

```nginx
location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

## 故障排除

### 问题 1：502 Bad Gateway

检查后端服务是否运行：

```bash
sudo systemctl status remote-file-manager
```

### 问题 2：静态文件 404

检查 Nginx 配置中的路径是否正确。

### 问题 3：上传大文件失败

增加 Nginx 和后端的文件大小限制：

```nginx
client_max_body_size 100M;
```

## 更新应用

```bash
# 拉取最新代码
cd /opt/remote_file_manage
git pull

# 更新后端
cd backend
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart remote-file-manager

# 更新前端
cd ../frontend
npm install
npm run build

# 重启 Nginx
sudo systemctl restart nginx
```

## 完成！

现在您可以通过浏览器访问 `http://your-domain.com` 或 `http://your-server-ip` 来使用 Remote File Manager。
