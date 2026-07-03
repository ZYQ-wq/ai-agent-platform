---
name: server-web-directory-guide
description: server 与 web 目录结构梳理
metadata:
  type: reference
  updated: 2026-07-03
---

# Server / Web 目录梳理

## 总览

| 目录 | 职责 | 技术栈 |
|------|------|--------|
| `server/` | 后端 API、业务逻辑、工作流引擎、Docker 沙箱 | FastAPI、SQLAlchemy、SQLite |
| `web/` | 前端页面、路由、API 封装 | Vue 3、TypeScript、Vite、Vue Router |

默认地址：后端 `http://localhost:8000`，前端 `http://localhost:5173`

---

## Server 目录

```
server/
├── app/
│   ├── main.py              # FastAPI 入口，注册路由与 CORS
│   ├── api/                 # HTTP 路由层（6 个模块）
│   ├── services/            # 业务逻辑层
│   ├── models/              # SQLAlchemy 数据模型
│   ├── schemas/             # Pydantic 请求/响应模型
│   ├── runtime/             # 工作流运行时引擎
│   ├── tools/               # Agent 工具（calculator、search）
│   └── core/                # 配置、数据库、认证、文件存储
├── tests/                   # 测试脚本（手动/集成）
└── uploads/kb/              # 知识库上传文件存储
```

### api/ — 路由层

| 文件 | 前缀 | 职责 |
|------|------|------|
| `user.py` | `/users` | 注册、登录 |
| `agent.py` | `/agents` | Agent CRUD |
| `chat.py` | `/chat` | 对话、历史、**流式对话** |
| `workflow.py` | `/workflow` | 工作流保存/查询/运行/删除 |
| `knowledge.py` | `/kb` | 知识库 CRUD、上传、检索 |
| `plugin.py` | `/plugins` | AI 编程项目、文件、运行、Agent 改码 |

**主要端点速查：**

```
GET  /
POST /users/register、/users/login

POST /agents/create
GET  /agents/my
GET/PUT/DELETE /agents/{id}

POST /chat/{agent_id}              # 非流式
POST /chat/{agent_id}/stream       # SSE 流式
GET  /chat/history/{agent_id}

POST /workflow/save
GET  /workflow/my
GET  /workflow/{id}
DELETE /workflow/{id}
POST /workflow/run/{id}

POST /kb/create
GET  /kb/list
GET/PUT/DELETE /kb/{id}
POST /kb/upload/{kb_id}
POST /kb/search/{kb_id}
DELETE /kb/file/{file_id}

POST/GET /plugins
GET  /plugins/{id}/files
POST /plugins/{id}/run
POST /plugins/agent
POST /plugins/apply
...
```

### services/ — 业务逻辑

| 文件 | 模块 | 说明 |
|------|------|------|
| `user_service.py` | 用户 | 注册、登录、JWT |
| `agent_service.py` | Agent | Agent CRUD |
| `ai_service.py` | 对话 | 记忆 + RAG + 工具调用 + **流式输出** |
| `memory_manager.py` | 记忆 | 短期/长期记忆、向量检索 |
| `tool_call_service.py` | 工具 | 工具执行与日志 |
| `workflow_service.py` | 工作流 | 持久化与运行调度 |
| `kb_service.py` | 知识库 | 创建、上传、切片、向量化 |
| `search_embedding_service.py` | 知识库 | 语义检索（余弦相似度） |
| `embedding_service.py` | 通用 | Embedding（text-embedding-v1） |
| `document_parser.py` | 知识库 | PDF/DOCX/TXT 解析 |
| `text_splitter.py` | 知识库 | 文本切片 |
| `search_service.py` | 工具 | Tavily 互联网搜索 |
| `plugin_service.py` | AI 编程 | 项目/文件 CRUD、变更应用、运行调度 |
| `project_agent_service.py` | AI 编程 | 多文件 Agent 生成（FILE/ACTION 块） |
| `codegen_service.py` | AI 编程 | 单文件生成/编辑 |
| `sandbox_service.py` | AI 编程 | Docker 沙箱（Python / Web 预览） |
| `plugin_manifest_service.py` | AI 编程 | plugin.yaml 校验（暂无 API） |
| `knowledge_service.py` | — | **遗留**，未使用 |
| `coding_agent_service.py` | — | **占位**，未完成 |

### models/ — 数据表

| 模型 | 表名 | 用途 |
|------|------|------|
| `user.py` | users | 用户 |
| `agent.py` | agents | 智能体 |
| `memory.py` | memories | 对话短期记忆 |
| `memory_summary.py` | memory_summaries | 长期摘要 |
| `tool_call.py` | tool_calls | 工具调用日志 |
| `workflow.py` | workflows | 工作流 |
| `workflow_node.py` | workflow_nodes | 工作流节点 |
| `workflow_edge.py` | workflow_edges | 工作流边 |
| `knowledge.py` | knowledge_bases | 知识库 |
| `knowledge_file.py` | knowledge_files | 知识库文件 |
| `knowledge_chunks.py` | knowledge_chunks | 文档切片 + 向量 |
| `plugin_project.py` | plugin_projects | 编程项目（按用户隔离） |
| `plugin_file.py` | plugin_files | 项目文件内容 |

### runtime/ — 工作流引擎

| 文件 | 说明 |
|------|------|
| `workflow_engine.py` | DAG 顺序执行 |
| `executors.py` | 节点：start / llm / tool / output |
| `context.py` | 运行时上下文 |
| `llm_client.py` | LLM 节点调用 qwen |
| `base_node.py` | 节点基类 |

### tools/ — Agent 工具

| 文件 | 说明 |
|------|------|
| `registry.py` | 工具注册，导出 OpenAI function 格式 |
| `calculator_tool.py` | 计算器 |
| `search_tool.py` | Tavily 搜索 |
| `base_tool.py` | 工具基类 |

### core/ — 基础设施

| 文件 | 说明 |
|------|------|
| `config.py` | 环境变量（OPENAI_*、TAVILY_*、SECRET_KEY） |
| `database.py` | SQLite + SessionLocal |
| `auth.py` | JWT、密码哈希 |
| `file_storage.py` | 知识库文件存 uploads/kb/ |
| `deps.py` | FastAPI 依赖 |

### tests/

| 文件 | 说明 |
|------|------|
| `test_runtime.py` | 工作流引擎简单链测试 |
| `test_workflow_runtime.py` | 从 DB 读工作流运行 |
| `test_docker.py` | Docker 连通性 |

---

## Web 目录

```
web/
├── index.html
├── package.json
├── vite.config.ts
├── tsconfig*.json
├── public/
│   └── icons.svg
└── src/
    ├── main.ts              # 应用入口
    ├── App.vue              # 根组件（router-view）
    ├── style.css            # 全局样式
    ├── router/index.ts      # 路由配置
    ├── utils/request.ts     # axios 封装（JWT、超时）
    ├── api/                 # 后端 API 封装
    ├── stores/              # Pinia 状态
    ├── types/               # TypeScript 类型
    ├── views/               # 页面级组件
    └── components/          # 可复用组件
        ├── coding/          # AI 编程 IDE 组件
        └── workflow/        # 工作流节点组件
```

### 路由 ↔ 页面

| 路径 | 视图 | 需登录 | 说明 |
|------|------|--------|------|
| `/` | → `/plaza` | — | 首页重定向 |
| `/plaza` | Plaza.vue | ✓ | 平台广场入口 |
| `/login` | Login.vue | — | 登录 |
| `/register` | Register.vue | — | 注册 |
| `/agents/studio` | AgentStudio.vue | ✓ | Agent 管理 |
| `/agents` | Agents.vue | ✓ | Agent 列表（备用） |
| `/chat/:agentId` | Chat.vue | ✓ | 流式对话 |
| `/workflow-management` | WorkflowManagement.vue | ✓ | 工作流列表 |
| `/workflow` | WorkflowStudio.vue | ✓ | 工作流编辑器（?id=） |
| `/kb` | Knowledge.vue | ✓ | 知识库列表 |
| `/kb/upload/:id` | KBUpload.vue | ✓ | 知识库管理（学习/检索/设置） |
| `/kb/:id` | → `/kb/upload/:id` | ✓ | 旧链接重定向 |
| `/coding` | CodingIDE.vue | ✓ | AI 编程 IDE |

**未挂路由的视图（遗留）：** `KnowledgeBase.vue`、`WorkflowEditor.vue`、`Agents.vue`（部分场景仍可用）

### views/ — 页面说明

| 文件 | 功能 |
|------|------|
| `Plaza.vue` | 四大模块入口 + 统计 |
| `Login.vue` / `Register.vue` | 认证 |
| `AgentStudio.vue` | Agent CRUD，返回广场 |
| `Chat.vue` | 流式聊天，停止生成 |
| `WorkflowManagement.vue` | 工作流列表 |
| `WorkflowStudio.vue` | Vue Flow 编排，返回工作流管理 |
| `Knowledge.vue` | 知识库列表，返回广场 |
| `KBUpload.vue` | 上传、向量检索测试、设置 |
| `coding/CodingIDE.vue` | Monaco 编辑器 + Agent + Run |

### api/ — 前端 API 层

| 文件 | 封装 |
|------|------|
| `utils/request.ts` | axios 实例，baseURL:8000，Bearer token |
| `agent.ts` | GET /agents/my |
| `plugin.ts` | /plugins 全套（含长超时 agentChat） |
| `codegen.ts` | POST /plugins/generate |
| `coding.ts` | 空文件 |

**说明：** Plaza、Chat、Knowledge、Workflow 等页面部分仍直接用 axios 硬编码 `127.0.0.1:8000`。

### components/

**coding/** — AI 编程 IDE

| 组件 | 职责 |
|------|------|
| `ProjectSidebar.vue` | 项目列表 |
| `CodingFileTree.vue` | 文件树 |
| `CodingEditor.vue` | Monaco 编辑器 |
| `AgentChatPanel.vue` | Agent 对话 + Apply |
| `CopilotPanel.vue` | Copilot 面板 |
| `CodingAssistant.vue` | 助手 |
| `ApplyChangesModal.vue` | 变更预览弹窗 |
| `ChangePreview.vue` | 变更预览 |
| `CodingToolbar.vue` / `CodingConsole.vue` | 工具栏 / 控制台 |

**workflow/**

| 组件 | 职责 |
|------|------|
| `WorkflowNode.vue` | Vue Flow 自定义节点 UI |

### stores/

| 文件 | 说明 |
|------|------|
| `coding.ts` | Pinia demo 数据，IDE 主要直连 API |

---

## 模块对应关系

```
Plaza
 ├── AgentStudio  → /agents/*     → agent_service、ai_service
 ├── WorkflowMgmt → /workflow/*    → workflow_service、WorkflowEngine
 ├── Knowledge    → /kb/*         → kb_service、search_embedding_service
 └── CodingIDE    → /plugins/*    → plugin_service、sandbox_service

Chat             → /chat/*         → ai_service（流式 + 记忆 + 工具）
```

---

## 启动命令

```bash
# 后端
cd server
uvicorn app.main:app --reload --port 8000

# 前端
cd web
npm run dev
```

---

## 相关文档

- `memory/ai-agent-platform-overview.md` — 全项目总览
- `memory/front-end-dev-server-startup.md` — 前端启动说明
- `CLAUDE.md` — 工程规范
