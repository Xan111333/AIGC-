# AIGC 实训平台 - 部署指南

## 架构说明

| 部分 | 技术 | 部署平台 |
|------|------|---------|
| 后端 API | FastAPI + SQLite | Railway（免费） |
| 前端界面 | Vue3 + Vite | Vercel（免费） |

---

## 第一步：部署后端到 Railway

### 1.1 注册 Railway
访问 https://railway.app → 用 GitHub 账号登录

### 1.2 创建新项目
1. 点击 **New Project**
2. 选择 **Deploy from GitHub repo**
3. 选择你的仓库 `Xan111333/AIGC-`
4. 在 **Root Directory** 中填写 `backend`（重要！）

### 1.3 配置环境变量
在 Railway 项目设置 → **Variables** 中添加：

```
SECRET_KEY=换成一个随机字符串（比如32位随机字母数字）
DATABASE_URL=sqlite:///./aigc_training.db
DEEPSEEK_API_KEY=你的DeepSeek密钥
QIANFAN_AK=你的百度千帆AccessKey
QIANFAN_SK=你的百度千帆SecretKey
```

### 1.4 获取后端地址
部署成功后，在 Railway 项目页面可以看到域名，格式如：
`https://xxxx.up.railway.app`

**把这个地址保存下来，第二步要用。**

---

## 第二步：部署前端到 Vercel

### 2.1 注册 Vercel
访问 https://vercel.com → 用 GitHub 账号登录

### 2.2 导入项目
1. 点击 **Add New → Project**
2. 选择仓库 `Xan111333/AIGC-`
3. **Framework Preset** 选择 `Vite`
4. **Root Directory** 留空（默认根目录）

### 2.3 配置环境变量
在 **Environment Variables** 中添加：

```
VITE_API_BASE_URL = https://你的Railway后端地址.up.railway.app
```

（注意：填写第一步获取的 Railway 域名，不要带末尾斜杠）

### 2.4 点击 Deploy
等待 1-2 分钟，Vercel 会给你一个 `https://xxx.vercel.app` 的地址。

---

## 第三步：验证部署

1. 打开 Vercel 给你的前端地址
2. 尝试登录（使用初始账号或注册新账号）
3. 测试文本生成、图片生成等功能

---

## 本地开发

```bash
# 启动后端
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# 启动前端
npm install
npm run dev
```

本地开发时前端自动读取 `.env.local` 文件，指向 `localhost:8000`，无需手动修改。

---

## 常见问题

**Q: Railway 部署失败怎么办？**
检查 Logs 标签，常见原因是 `requirements.txt` 某个包版本不兼容。

**Q: 前端登录成功但功能报错？**
打开浏览器开发者工具 → Network，检查 API 请求地址是否正确指向 Railway。

**Q: Railway 免费版有什么限制？**
每月 $5 额度，轻量使用基本够用。休眠后首次访问稍慢（约 10 秒冷启动）。
