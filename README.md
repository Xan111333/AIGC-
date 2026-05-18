# AIGC实训平台

一个面向高校师生的AI生成内容实训平台，支持文本、图像、视频、音频生成，以及任务管理、作业批改、数据统计等完整功能。

## 功能特性

### 🎨 AI生成功能
- **文本生成** - 基于DeepSeek API的智能文本生成
- **图像生成** - 基于百度千帆API的图像生成
- **视频生成** - AI视频生成
- **音频生成** - AI音频生成

### 📋 任务管理
- 教师端：任务发布、编辑、删除
- 学生端：任务查看、作业提交
- 作业批改：评分、评语

### 📊 数据统计
- 成绩分布图表
- 任务完成率分析
- 模块使用频次统计
- Excel报表导出

### 👨‍💼 管理员功能
- 用户管理（增删改查）
- 系统配置
- 内容审核
- 操作日志

### 📁 作品管理
- 作品列表展示
- 批量导出（PDF、Word、ZIP）
- 分类管理

### 📚 学习资源
- 资源分类管理
- 搜索和筛选
- 教师端资源上传

## 技术栈

### 前端
- **Vue 3** + Composition API
- **Element Plus** - UI组件库
- **Vue Router** - 路由管理
- **ECharts** - 数据可视化
- **Vite** - 构建工具

### 后端
- **FastAPI** - Python Web框架
- **SQLite** (开发) / **MySQL** (生产)
- **Redis** - 缓存和会话
- **MinIO** - 对象存储
- **JWT** - 身份认证

## 项目结构

```
AIGC实训平台/
├── backend/                    # 后端代码
│   ├── app/                    # 应用核心
│   │   ├── routes/            # API路由
│   │   ├── services/          # 业务逻辑
│   │   ├── schemas/           # Pydantic模型
│   │   └── utils/             # 工具函数
│   ├── main_simple.py         # 简化版后端（开发用）
│   ├── main.py                # 完整版后端
│   ├── requirements.txt       # Python依赖
│   ├── Dockerfile.prod        # 生产环境Dockerfile
│   └── .env.example          # 环境变量示例
├── src/                       # 前端代码
│   ├── views/                 # 页面组件
│   │   ├── admin/            # 管理员页面
│   │   ├── teacher/          # 教师页面
│   │   ├── student/          # 学生页面
│   │   └── *.vue             # 通用页面
│   ├── api/                  # API封装
│   ├── router/               # 路由配置
│   └── main.js               # 入口文件
├── docker-compose.prod.yml   # 生产环境编排
├── nginx.conf               # Nginx配置
├── deploy.sh                # 一键部署脚本
├── rollback.sh              # 回滚脚本
├── checklist.md             # 上线检查清单
└── package.json             # 前端依赖
```

## 快速开始

### 方式一：本地开发

#### 1. 安装依赖

```bash
# 后端依赖
cd backend
pip install -r requirements.txt

# 前端依赖
npm install
```

#### 2. 配置环境变量

```bash
# 复制后端环境变量
cp backend/.env.example backend/.env

# 编辑配置
vim backend/.env
```

#### 3. 启动服务

```bash
# 启动后端
cd backend
python main_simple.py

# 启动前端（新终端）
npm run dev
```

#### 4. 访问

- 前端：http://localhost:5173
- 后端：http://localhost:8000
- API文档：http://localhost:8000/docs

### 方式二：Docker部署

#### 1. 准备配置

```bash
# 复制环境变量
cp .env.prod.example .env.prod

# 编辑配置
vim .env.prod
```

#### 2. 一键部署

```bash
chmod +x deploy.sh
./deploy.sh
```

#### 3. 访问

- 前端：https://yourdomain.com
- 后端API：http://yourserver:8000

## 测试账户

| 用户名 | 密码 | 角色 |
|--------|------|------|
| admin | admin123 | 管理员 |
| teacher | teacher123 | 教师 |
| student | student123 | 学生 |

## 环境变量配置

### 必需配置

```bash
# 数据库
MYSQL_ROOT_PASSWORD=your_password
MYSQL_DATABASE=aigc_platform
MYSQL_USER=aigc_user
MYSQL_PASSWORD=your_db_password

# 安全
SECRET_KEY=your_secret_key

# 域名
PRODUCTION_DOMAIN=yourdomain.com

# API Key（可选，不配置使用Mock）
DEEPSEEK_API_KEY=your_key
QIANFAN_AK=your_ak
QIANFAN_SK=your_sk
```

## 完整部署指南

### 1. 准备服务器

**最低配置：**
- CPU：2核+
- 内存：4GB+
- 硬盘：50GB+
- 操作系统：Ubuntu 22.04 LTS 或 CentOS 8

**安装Docker：**
```bash
# Ubuntu
curl -fsSL https://get.docker.com | bash

# CentOS
curl -fsSL https://get.docker.com | bash

# 启动Docker
sudo systemctl start docker
sudo systemctl enable docker

# 安装Docker Compose
sudo apt install docker-compose-plugin  # Ubuntu
sudo dnf install docker-compose-plugin   # CentOS
```

### 2. 上传代码

```bash
# 方式一：Git
git clone your_repo_url
cd AIGC实训平台

# 方式二：SCP
scp -r local_path user@server:/opt/aigc-platform
```

### 3. 配置环境变量

```bash
cd /opt/aigc-platform
cp .env.prod.example .env.prod
vim .env.prod
```

**重要配置项：**
- `SECRET_KEY` - 生成随机密钥
- `PRODUCTION_DOMAIN` - 你的域名
- 数据库密码
- API密钥（如需要）

### 4. 执行部署

```bash
chmod +x deploy.sh rollback.sh
./deploy.sh
```

### 5. 配置SSL（可选）

使用Certbot免费证书：

```bash
# 安装Certbot
sudo apt install certbot python3-certbot-nginx

# 获取证书
sudo certbot certonly --nginx -d yourdomain.com

# 复制证书到项目目录
mkdir -p ssl
cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem ssl/cert.pem
cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ssl/key.pem

# 重新部署
docker-compose -f docker-compose.prod.yml restart frontend
```

### 6. 验证部署

```bash
# 检查容器状态
docker-compose -f docker-compose.prod.yml ps

# 查看日志
docker-compose -f docker-compose.prod.yml logs backend
docker-compose -f docker-compose.prod.yml logs frontend

# 访问测试
curl http://localhost:8000/docs
curl http://localhost/
```

## 常用命令

### 查看状态
```bash
docker-compose -f docker-compose.prod.yml ps
```

### 查看日志
```bash
docker-compose -f docker-compose.prod.yml logs -f backend
docker-compose -f docker-compose.prod.yml logs -f frontend
```

### 重启服务
```bash
docker-compose -f docker-compose.prod.yml restart
```

### 停止服务
```bash
docker-compose -f docker-compose.prod.yml down
```

### 启动服务
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### 回滚
```bash
# 查看可用备份
./rollback.sh list

# 回滚到最新备份
./rollback.sh latest

# 回滚到指定版本
./rollback.sh 20240115_103000
```

## 故障排查

### 1. 容器无法启动

```bash
# 查看详细日志
docker-compose -f docker-compose.prod.yml logs backend --tail=100

# 检查端口占用
netstat -tlnp | grep 8000
netstat -tlnp | grep 80
```

### 2. 数据库连接失败

```bash
# 检查MySQL容器状态
docker-compose -f docker-compose.prod.yml ps mysql

# 查看MySQL日志
docker-compose -f docker-compose.prod.yml logs mysql

# 手动连接测试
docker-compose -f docker-compose.prod.yml exec mysql mysql -u root -p
```

### 3. 前端无法访问

```bash
# 检查Nginx配置
docker-compose -f docker-compose.prod.yml exec frontend nginx -t

# 检查容器
docker-compose -f docker-compose.prod.yml ps frontend

# 查看日志
docker-compose -f docker-compose.prod.yml logs frontend
```

### 4. API调用失败

```bash
# 检查后端健康状态
curl http://localhost:8000/health

# 检查API文档
curl http://localhost:8000/docs

# 检查CORS配置
cat backend/.env | grep CORS
```

## 安全建议

1. **修改默认密码**
   - 所有默认密码必须修改
   - 使用强密码生成工具

2. **防火墙配置**
   ```bash
   # Ubuntu
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw allow 22/tcp
   sudo ufw enable
   
   # CentOS
   sudo firewall-cmd --add-port=80/tcp --permanent
   sudo firewall-cmd --add-port=443/tcp --permanent
   sudo firewall-cmd --reload
   ```

3. **定期备份**
   ```bash
   # 添加定时任务
   crontab -e
   
   # 每天凌晨2点备份
   0 2 * * * /opt/aigc-platform/deploy.sh backup
   ```

4. **监控告警**
   - 设置容器健康检查
   - 配置资源告警
   - 设置错误日志告警

## 性能优化

### 1. 后端优化
```bash
# 增加worker数量（在docker-compose.yml中修改）
environment:
  - GUNICORN_WORKERS=4
  - GUNICORN_THREADS=4
```

### 2. 前端优化
- 启用gzip压缩（已在nginx.conf配置）
- 使用CDN加速静态资源
- 启用浏览器缓存

### 3. 数据库优化
- 启用查询缓存
- 添加必要的索引
- 定期优化表

## 支持

如有问题，请参考：
- API文档：`/docs`
- 上线检查清单：`checklist.md`
- 常见问题：见上方故障排查

## 许可证

MIT License
