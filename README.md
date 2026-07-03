# AI Agent Platform

全栈 AI Agent 平台：智能体对话、工作流编排、知识库 RAG、AI 编程（Docker 沙箱）。

| 模块 | 技术 |
|------|------|
| 后端 | FastAPI、SQLAlchemy、SQLite |
| 前端 | Vue 3、TypeScript、Vite |
| LLM | OpenAI 兼容 API（如阿里云 DashScope） |

---

## 目录结构

```
ai-agent-platform/
├── server/           # 后端 API
│   ├── app/
│   ├── requirements.txt
│   └── uploads/      # 知识库上传文件（运行时生成）
├── web/              # 前端
├── docker/           # Docker 构建文件
├── memory/           # 项目笔记与文档
├── docker-compose.yml
├── .env.example
├── CLAUDE.md         # 工程规范
└── README.md
```

更详细的模块说明见 `memory/server-web-directory-guide.md`。

---

## 环境要求

- **Python** 3.11+
- **Node.js** 20+
- **Docker Desktop**（AI 编程 Run 功能需要，用于沙箱执行代码）

---

## 本地开发

### 1. 配置环境变量

```bash
cp .env.example server/.env
```

编辑 `server/.env`，至少填写：

- `OPENAI_API_KEY`
- `OPENAI_BASE_URL`（如 DashScope 兼容地址）
- `SECRET_KEY`（生产环境请使用强随机值）

可选：在 `web/.env` 中设置：

```env
VITE_API_BASE_URL=http://localhost:8000
```

### 2. 启动后端

```bash
cd server
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

验证：访问 http://localhost:8000 应返回 `AI Agent Platform Backend Running`。

### 3. 启动前端

```bash
cd web
npm install
npm run dev
```

访问：http://localhost:5173

首次使用请先 **注册 / 登录**，再从广场进入各模块。

---

## Docker 部署（骨架）

适用于阿里云 ECS 等 Linux 服务器的初步部署验证。

### 1. 准备环境文件

```bash
cp .env.example server/.env
# 编辑 server/.env，填写密钥，并设置例如：
# CORS_ORIGINS=http://your-server-ip:8080
```

确保服务器已安装 **Docker** 与 **Docker Compose**，且 AI 编程功能需要 Docker 守护进程可用。

### 2. 构建并启动

```bash
docker compose up -d --build
```

| 服务 | 地址 |
|------|------|
| 前端（Nginx） | http://localhost:8080 |
| 后端 API | http://localhost:8000 |

Docker 模式下前端 `VITE_API_BASE_URL` 留空，由 Nginx 将 `/users`、`/agents`、`/chat` 等路径反代到 backend。

### 3. 数据持久化

以下目录/文件通过 volume 挂载，重启容器后保留：

- `server/ai_agent_platform.db` — SQLite 数据库
- `server/uploads/` — 知识库上传文件

---

## 环境变量说明

| 变量 | 位置 | 说明 |
|------|------|------|
| `OPENAI_API_KEY` | server/.env | LLM API 密钥 |
| `OPENAI_BASE_URL` | server/.env | OpenAI 兼容 API 地址 |
| `TAVILY_API_KEY` | server/.env | 搜索工具（可选） |
| `SECRET_KEY` | server/.env | JWT 签名密钥 |
| `CORS_ORIGINS` | server/.env | 允许的前端来源，逗号分隔 |
| `VITE_API_BASE_URL` | web/.env 或 Docker build | 前端 API 基址；Docker 同源部署可留空 |

完整示例见 [.env.example](.env.example)。

---

## 部署前已知事项

以下内容在骨架阶段**尚未完全统一**，上生产前需逐步处理：

1. **部分前端页面仍硬编码 `http://127.0.0.1:8000`**（Plaza、Knowledge、Chat 等），未走 `web/src/utils/request.ts`。Coding / Plugin 模块已使用统一封装。
2. **SQLite** 适合单机部署；高并发或集群场景需迁移 PostgreSQL 等。
3. **AI 编程沙箱** 需要宿主机 Docker，并挂载 `/var/run/docker.sock`（见 `docker-compose.yml`）。
4. **HTTPS** 生产环境建议在 Docker 前增加 Nginx / 阿里云 SLB 终止 SSL。

---

## 常用命令

```bash
# 后端测试
cd server && python -m pytest tests/   # 如有 pytest 用例

# 前端构建
cd web && npm run build

# Docker 停止
docker compose down

# Docker 查看日志
docker compose logs -f backend
```

---

## 相关文档

- [server-web-directory-guide.md](memory/server-web-directory-guide.md) — 目录与 API 详解
- [ai-agent-platform-overview.md](memory/ai-agent-platform-overview.md) — 项目总览
- [CLAUDE.md](CLAUDE.md) — 工程规范
