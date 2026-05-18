# AIGC实训平台 - GitHub部署指南

## 📋 项目文件清单

### 必须上传的文件
- `README.md` - 项目说明和部署指南
- `.gitignore` - Git忽略规则
- `.env.prod.example` - 生产环境变量示例
- `package.json` - 前端依赖
- `vite.config.js` - Vite配置
- `index.html` - 入口HTML
- `deploy.sh` - 一键部署脚本
- `rollback.sh` - 回滚脚本
- `docker-compose.prod.yml` - Docker编排
- `checklist.md` - 上线检查清单

### 目录结构
```
.
├── backend/                    # 后端代码
│   ├── app/
│   ├── main_simple.py         # 简化版后端（部署用）
│   ├── main.py                # 完整版后端
│   ├── requirements.txt       # Python依赖
│   ├── Dockerfile.prod        # 后端Dockerfile
│   └── .env.example          # 后端环境示例
├── src/                       # 前端源码
│   ├── views/                 # 页面组件
│   ├── api/                   # API封装
│   ├── router/                # 路由
│   ├── main.js                # 入口
│   └── App.vue                # 根组件
├── frontend/                  # 前端构建配置
│   ├── Dockerfile.prod        # 前端Dockerfile
│   └── nginx.conf             # Nginx配置
└── public/                    # 静态资源
```

## 🚀 部署步骤

### 第一步：上传到GitHub

```bash
# 1. 初始化Git仓库
git init

# 2. 查看状态（确认没有敏感文件）
git status

# 3. 添加所有文件
git add .

# 4. 提交
git commit -m "Initial commit: AIGC Training Platform"

# 5. 添加远程仓库（替换为你的仓库地址）
git remote add origin https://github.com/你的用户名/你的仓库名.git

# 6. 推送到GitHub
git push -u origin main
```

### 第二步：准备服务器

**服务器要求：**
- CPU: 2核以上
- 内存: 4GB以上
- 硬盘: 50GB以上
- 系统: Ubuntu 22.04 LTS 推荐

**安装Docker：**
```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装Docker
curl -fsSL https://get.docker.com | bash

# 启动Docker
sudo systemctl start docker
sudo systemctl enable docker

# 验证安装
docker --version
docker compose version
```

### 第三步：克隆代码

```bash
# 克隆仓库
git clone https://github.com/你的用户名/你的仓库名.git
cd 你的仓库名

# （可选）切换到特定版本
git checkout v1.0.0
```

### 第四步：配置环境变量

```bash
# 复制环境变量示例
cp .env.prod.example .env.prod

# 编辑配置
nano .env.prod
```

**必须修改的配置项：**
```bash
# 1. 数据库密码（设置强密码）
MYSQL_ROOT_PASSWORD=your_strong_root_password
MYSQL_PASSWORD=your_strong_db_password

# 2. 安全密钥（至少32字符，随机生成）
SECRET_KEY=your_very_long_secret_key_at_least_32_characters

# 3. 域名（如果有）
PRODUCTION_DOMAIN=yourdomain.com
```

**生成随机密钥：**
```bash
# 方法1：使用Python
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# 方法2：使用openssl
openssl rand -base64 32
```

### 第五步：执行部署

```bash
# 添加执行权限
chmod +x deploy.sh rollback.sh

# 一键部署
./deploy.sh
```

部署过程：
1. 环境检查
2. 创建备份
3. 拉取基础镜像
4. 构建服务镜像
5. 启动服务
6. 健康检查

### 第六步：验证部署

```bash
# 检查容器状态
docker compose -f docker-compose.prod.yml ps

# 查看日志
docker compose -f docker-compose.prod.yml logs backend
docker compose -f docker-compose.prod.yml logs frontend

# 测试访问
curl http://localhost:8000/docs
curl http://localhost/
```

## 🔧 常用操作

### 查看服务状态
```bash
docker compose -f docker-compose.prod.yml ps
```

### 查看日志
```bash
# 实时查看后端日志
docker compose -f docker-compose.prod.yml logs -f backend

# 查看最近100行
docker compose -f docker-compose.prod.yml logs --tail=100 backend
```

### 重启服务
```bash
# 全部重启
./deploy.sh restart

# 或使用docker compose
docker compose -f docker-compose.prod.yml restart

# 单独重启某个服务
docker compose -f docker-compose.prod.yml restart backend
```

### 停止/启动
```bash
# 停止
./deploy.sh stop

# 启动
./deploy.sh start
```

### 更新代码
```bash
# 拉取最新代码
git pull

# 重新部署
./deploy.sh
```

### 回滚到上一版本
```bash
# 查看可用备份
./rollback.sh list

# 回滚到最新备份
./rollback.sh latest

# 或回滚到指定版本
./rollback.sh 20240115_103000
```

## 🌐 访问服务

部署成功后，访问以下地址：

| 服务 | 地址 |
|------|------|
| 前端 | http://你的服务器IP |
| 后端API | http://你的服务器IP:8000 |
| API文档 | http://你的服务器IP:8000/docs |
| MinIO管理 | http://你的服务器IP:9001 |

## 🔑 默认测试账户

| 用户名 | 密码 | 角色 | 功能 |
|--------|------|------|------|
| admin | admin123 | 管理员 | 用户管理、系统配置 |
| teacher | teacher123 | 教师 | 任务管理、作业批改 |
| student | student123 | 学生 | AI生成、提交作业 |

**⚠️ 重要：** 请在部署后立即修改默认密码！

## 🔒 安全配置

### 1. 修改默认账户密码

登录后在个人设置中修改密码。

### 2. 配置防火墙

```bash
# Ubuntu
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# CentOS
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

### 3. 配置SSL（HTTPS）

```bash
# 安装Certbot
sudo apt install certbot

# 获取证书（替换为你的域名）
sudo certbot certonly --standalone -d yourdomain.com

# 复制证书到项目目录
mkdir -p ssl
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem ssl/cert.pem
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ssl/key.pem

# 修改nginx.conf启用SSL后重新部署
```

### 4. 定期备份

```bash
# 添加定时任务
crontab -e

# 添加以下行（每天凌晨2点备份）
0 2 * * * /path/to/deploy.sh backup
```

## 🐛 故障排查

### 问题1：容器无法启动
```bash
# 查看详细日志
docker compose -f docker-compose.prod.yml logs backend --tail=100

# 检查端口占用
netstat -tlnp | grep 8000
netstat -tlnp | grep 80
```

### 问题2：数据库连接失败
```bash
# 检查MySQL状态
docker compose -f docker-compose.prod.yml ps mysql

# 查看MySQL日志
docker compose -f docker-compose.prod.yml logs mysql

# 等待MySQL初始化（首次启动需要时间）
sleep 60
./deploy.sh restart
```

### 问题3：前端无法访问
```bash
# 检查Nginx配置
docker compose -f docker-compose.prod.yml exec frontend nginx -t

# 检查前端容器
docker compose -f docker-compose.prod.yml ps frontend
```

### 问题4：API调用失败
```bash
# 检查后端健康状态
curl http://localhost:8000/health

# 检查后端日志
docker compose -f docker-compose.prod.yml logs backend
```

## 📊 性能优化

### 增加后端Worker数量

编辑 `docker-compose.prod.yml`：
```yaml
backend:
  environment:
    - GUNICORN_WORKERS=4
    - GUNICORN_THREADS=4
```

### 配置CDN

如果使用CDN加速静态资源：
- 修改前端构建配置
- 将dist目录上传到CDN
- 更新nginx配置

## 📝 注意事项

1. **首次部署**：MySQL初始化需要1-2分钟，请耐心等待
2. **资源限制**：确保服务器内存足够（MySQL+Redis约需2GB）
3. **API Key**：不配置时使用Mock数据，可正常体验所有功能
4. **数据持久化**：Docker volumes已配置，重启不丢失数据
5. **端口冲突**：确保80、8000、3306、6379端口未被占用

## 📞 获取帮助

- 查看详细文档：[README.md](./README.md)
- 上线检查清单：[checklist.md](./checklist.md)
- API文档：部署后访问 `/docs`

## 🎯 快速验证清单

- [ ] Docker已安装并运行
- [ ] 环境变量已配置
- [ ] 所有容器状态为Up
- [ ] 可以访问前端页面
- [ ] 可以登录测试账户
- [ ] API文档可访问
- [ ] 防火墙规则已配置

部署完成后，您就拥有一个完整可用的AIGC实训平台了！🎉
