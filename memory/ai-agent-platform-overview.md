---
name: ai-agent-platform-overview
description: AI Agent 平台全项目结构与模块总结
metadata:
  type: project
  updated: 2026-06-29
---

# AI Agent Platform 项目总结

## 项目概述

**ai-agent-platform** 是一个全栈 AI Agent 平台，提供以下核心能力：

- **智能体（Agent）**：创建、配置、对话，支持工具调用与记忆管理
- **工作流（Workflow）**：可视化 DAG 编排与运行
- **知识库（Knowledge Base）**：文档上传、切片、向量检索（RAG）
- **插件 / Coding IDE**：在线代码编辑、AI 辅助开发、Docker 沙箱运行

前后端分离架构：后端 FastAPI + SQLite，前端 Vue 3 + Vite + TypeScript。工程规范见根目录 `CLAUDE.md`，强调平台稳定性、复用现有架构、最小改动。

---

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | FastAPI、SQLAlchemy、SQLite、JWT（python-jose + passlib/bcrypt） |
| LLM | OpenAI 兼容 API（模型：qwen-max、qwen-mt-flash；Embedding：text-embedding-v1） |
| 外部服务 | Tavily 搜索、Docker 沙箱 |
| 文档处理 | PyPDF2、python-docx、自研文本切片 |
| 前端 | Vue 3、TypeScript、Vite、Vue Router、Pinia、Monaco Editor、axios |
| 工作流 UI | `@vue-flow/core`（依赖在根 `package.json`） |

环境变量（`server/app/core/config.py`）：`OPENAI_API_KEY`、`OPENAI_BASE_URL`、`TAVILY_API_KEY`、`SECRET_KEY`。

---

## 目录结构

```
ai-agent-platform/
├── package.json              # 根级依赖（vue-flow、axios、pinia 等）
├── requirements.txt          # Python 依赖
├── CLAUDE.md                 # 工程规范
├── memory/                   # 项目记忆 / 开发笔记
├── server/
│   ├── app/
│   │   ├── main.py           # FastAPI 入口
│   │   ├── api/              # 路由层（6 个模块）
│   │   ├── services/         # 业务逻辑（约 20 个服务）
│   │   ├── models/           # SQLAlchemy 模型（13 个）
│   │   ├── schemas/          # Pydantic 请求/响应模型
│   │   ├── runtime/          # 工作流引擎 + LLM 客户端
│   │   ├── tools/            # Agent 工具注册与实现
│   │   └── core/             # 配置、数据库、认证、文件存储
│   └── tests/                # 测试脚本（3 个文件）
└── web/
    ├── package.json          # 前端依赖
    ├── vite.config.ts
    └── src/
        ├── views/            # 页面视图
        ├── components/       # 可复用组件（coding、workflow）
        ├── api/              # API 封装层
        ├── stores/           # Pinia 状态
        ├── router/           # 路由
        └── utils/request.ts  # axios 封装
```

---

## 后端模块

### API 路由（`server/app/api/`）

入口：`server/app/main.py`，CORS 允许 `http://localhost:5173`。

| 模块 | 前缀 | 主要端点 |
|------|------|----------|
| `user.py` | `/users` | `POST /register`、`POST /login` |
| `chat.py` | `/chat` | `POST /{agent_id}`、`GET /history/{agent_id}` |
| `agent.py` | `/agents` | `POST /create`、`GET /my`、`GET/PUT/DELETE /{agent_id}` |
| `workflow.py` | `/workflow` | `POST /save`、`GET /my`、`GET/DELETE /{workflow_id}`、`POST /run/{workflow_id}` |
| `knowledge.py` | `/kb` | `POST /create`、`POST /upload/{kb_id}`、`GET /list`、`GET/PUT/DELETE /{kb_id}`、`DELETE /file/{file_id}`、`POST /search/{kb_id}` |
| `plugin.py` | `/plugins` | 项目 CRUD、文件 CRUD、运行、代码生成/编辑、Agent 绑定与对话、变更应用 |

**Plugin 模块完整端点：**

- `POST/GET /plugins` — 创建/列出项目
- `GET /plugins/{project_id}/files`、`POST /plugins/{project_id}/files`
- `PUT/DELETE /plugins/files/{file_id}`、`PUT /plugins/files/{file_id}/rename`
- `POST /plugins/{project_id}/run`
- `POST /plugins/generate`、`POST /plugins/edit`
- `PUT /plugins/{project_id}/agent/{agent_id}`、`PUT /plugins/{project_id}/agent/unbind`
- `POST /plugins/agent`、`POST /plugins/agent/run`
- `POST /plugins/apply`

根路径：`GET /` → `{"message": "AI Agent Platform Backend Running"}`

### Services（`server/app/services/`）

| 服务 | 职责 |
|------|------|
| `user_service.py` | 注册、登录 |
| `agent_service.py` | Agent CRUD |
| `ai_service.py` | Agent 对话核心：短期记忆 + 长期摘要 + RAG + 工具调用 + LLM |
| `memory_manager.py` | 聊天记忆存取、向量检索 |
| `tool_call_service.py` | 工具执行与日志 |
| `workflow_service.py` | 工作流持久化与运行 |
| `kb_service.py` | 知识库 CRUD、上传切片向量化 |
| `search_embedding_service.py` | 知识库语义搜索（余弦相似度） |
| `embedding_service.py` | 统一 Embedding 接口 |
| `document_parser.py` | PDF/DOCX/TXT 解析与切片 |
| `search_service.py` | Tavily 互联网搜索 |
| `plugin_service.py` | 插件项目/文件管理、Docker 运行、变更应用 |
| `project_agent_service.py` | Coding IDE Agent：读项目文件 → LLM → 解析 FILE/ACTION 块 |
| `codegen_service.py` | 单轮代码生成/编辑 |
| `sandbox_service.py` | Docker 隔离执行 Python/Web |
| `plugin_manifest_service.py` | `plugin.yaml` 校验（无对应 API 路由） |

**遗留 / 未完成：**

- `knowledge_service.py` — 引用不存在的 `KnowledgeBase` 模型，未被 API 使用
- `coding_agent_service.py` — 占位/未完成

### Models（`server/app/models/`）

| 模型 | 表名 | 说明 |
|------|------|------|
| `user.py` | `users` | 用户账号 |
| `agent.py` | `agents` | 智能体，含 system_prompt |
| `memory.py` | `memories` | 短期对话记忆，含 embedding |
| `memory_summary.py` | `memory_summaries` | 长期记忆摘要 |
| `tool_call.py` | `tool_calls` | 工具调用日志 |
| `workflow.py` | `workflows` | 工作流定义 |
| `workflow_node.py` | `workflow_nodes` | 工作流节点（JSON 配置） |
| `workflow_edge.py` | `workflow_edges` | 工作流边 |
| `knowledge.py` | `knowledge_bases` | 知识库 |
| `knowledge_file.py` | `knowledge_files` | 知识库文件 |
| `knowledge_chunks.py` | `knowledge_chunks` | 文档切片 + 向量 |
| `plugin_project.py` | `plugin_projects` | 插件项目（UUID），可绑定 Agent |
| `plugin_file.py` | `plugin_files` | 插件项目文件（存 DB） |

### Runtime（`server/app/runtime/`）

| 文件 | 作用 |
|------|------|
| `workflow_engine.py` | 工作流 DAG 顺序执行，解析变量引用，写入 WorkflowContext |
| `executors.py` | 节点类型：`start`、`llm`、`tool`、`output` |
| `base_node.py` | 节点基类 |
| `context.py` | 工作流运行时上下文 |
| `llm_client.py` | `call_qwen()` 供 LLM 节点使用 |

### Tools（`server/app/tools/`）

| 文件 | 说明 |
|------|------|
| `base_tool.py` | 抽象基类（name、description、parameters、run） |
| `calculator_tool.py` | 数学计算 |
| `search_tool.py` | Tavily 搜索 |
| `registry.py` | `tool_registry` 单例，导出 OpenAI function calling 格式 |

### Core（`server/app/core/`）

- `database.py` — SQLite + SessionLocal + `get_db()`
- `auth.py` — JWT 签发/验证、密码哈希
- `config.py` — 环境变量
- `file_storage.py` — 知识库文件存 `uploads/kb/`
- `deps.py` — FastAPI 依赖注入

---

## 前端模块

### 路由（`web/src/router/index.ts`）

| 路径 | 视图 | 需登录 |
|------|------|--------|
| `/` | 重定向 `/plaza` | — |
| `/plaza` | `Plaza.vue`（平台首页） | 是 |
| `/login`、`/register` | 登录/注册 | 否 |
| `/agents` | `Agents.vue` | 是 |
| `/agents/studio` | `AgentStudio.vue` | 是 |
| `/chat/:agentId` | `Chat.vue` | 是 |
| `/workflow` | `WorkflowStudio.vue` | 是 |
| `/workflow-management` | `WorkflowManagement.vue` | 是 |
| `/coding` | `CodingIDE.vue`（懒加载） | 否 |

**未注册路由的视图：** `Knowledge.vue`、`KnowledgeBase.vue`、`KBDetail.vue`、`KBUpload.vue`、`WorkflowEditor.vue`（Plaza 跳转 `/kb` 会 404）。

### Views 功能概览

| 视图 | 功能 |
|------|------|
| `Plaza.vue` | 平台入口，展示 Agent/工作流/知识库统计 |
| `Login.vue` / `Register.vue` | 用户认证 |
| `Agents.vue` / `AgentStudio.vue` | Agent 列表与 CRUD |
| `Chat.vue` | 与 Agent 对话 |
| `WorkflowStudio.vue` | Vue Flow 可视化编排、保存、运行 |
| `WorkflowManagement.vue` | 工作流列表管理 |
| `coding/CodingIDE.vue` | 插件 IDE：Monaco 编辑器 + Agent 对话 + 运行 |

### Components

**Coding（`web/src/components/coding/`）：**

- `ProjectSidebar.vue`、`CodingFileTree.vue`、`CodingEditor.vue`（Monaco）
- `CopilotPanel.vue`、`AgentChatPanel.vue`、`CodingAssistant.vue`
- `ApplyChangesModal.vue`、`ChangePreview.vue`、`AgentMessage.vue`
- `CodingToolbar.vue`、`CodingConsole.vue`

**Workflow（`web/src/components/workflow/`）：**

- `WorkflowNode.vue` — Vue Flow 自定义节点

### API 层（`web/src/api/`）

| 文件 | 封装端点 |
|------|----------|
| `utils/request.ts` | axios 实例，`baseURL: http://localhost:8000`，自动带 Bearer token |
| `agent.ts` | `GET /agents/my` |
| `plugin.ts` | 插件项目/文件/运行/Agent/apply 全套 |
| `codegen.ts` | `POST /plugins/generate` |
| `coding.ts` | 空文件 |

多数 View（Chat、Plaza、Knowledge 等）仍直接使用 axios 硬编码 `http://127.0.0.1:8000`，未统一走 `request.ts`。

### Stores

- `coding.ts` — Pinia store，含 demo 项目数据；CodingIDE 主要直接用 API。

---

## 数据模型关系

```
User
 ├── Agent（一对多）
 │    ├── Memory / MemorySummary / ToolCall（按 user_id + agent_id 隔离）
 │    └── PluginProject（可选绑定）
 ├── Workflow
 │    ├── WorkflowNode
 │    └── WorkflowEdge
 └── Knowledge
      └── KnowledgeFile
           └── KnowledgeChunk（含 embedding）

PluginProject
 └── PluginFile（文件内容存 DB，运行时写入 temp dir 再进 Docker）
```

---

## 核心业务流程

### 1. Agent 对话

```
Chat.vue → POST /chat/{agent_id}
  → ai_service.chat_with_agent()
      1. 查 User/Agent
      2. 短期记忆（最近 20 条）+ 向量 RAG 相关记忆
      3. 长期摘要注入 system prompt
      4. OpenAI chat (qwen-max) + tools
      5. 若有 tool_call → execute_tool_call → 二次 LLM
      6. 保存消息 + 更新长期摘要
  → 返回 response
```

可用工具：`calculator`、`search`（Tavily）。

### 2. 工作流

```
WorkflowStudio.vue → POST /workflow/save
  → 持久化 Workflow / WorkflowNode / WorkflowEdge

POST /workflow/run/{id} { inputs }
  → WorkflowEngine.run()
      start → llm(call_qwen) → tool → output
      变量引用: constant / "node_id.field"
  → 返回 trace + context
```

### 3. 知识库

```
POST /kb/create
POST /kb/upload/{kb_id} → parse → split → embedding → KnowledgeChunk
POST /kb/search/{kb_id} → 余弦相似度 Top-K
```

支持 PDF/DOCX/TXT；文件存 `uploads/kb/`。

### 4. Plugin / Coding IDE

```
CodingIDE.vue (/coding)
  → Plugin API: 项目/文件 CRUD
  → bindAgent: PUT /plugins/{id}/agent/{agent_id}
  → agentChat: POST /plugins/agent
      → ProjectAgentService: 加载全部文件 + Agent prompt → LLM → 解析 FILE/ACTION 块
  → applyChanges: POST /plugins/apply
  → runProject: POST /plugins/{id}/run
      → 写 temp dir → SandboxService.run_python / run_web (Docker)
  → generateCode / editCode: CodeGenService
```

**PluginService.run_project** 入口检测逻辑：

- 有 `main.py` → `SandboxService.run_python(tmp, "main.py")`
- 有 `app.py` → `SandboxService.run_python(tmp, "app.py")`
- 有 `index.html` → `SandboxService.run_web(tmp)`，返回 preview_url
- 否则返回「未找到入口文件」

新建项目默认创建：`main.py`、`plugin.yaml`、`README.md`。

### 5. Docker 沙箱

`sandbox_service.py`：

- `run_python`：只读挂载、`network_disabled`、内存/CPU 限制、15s 超时
- `run_web`：启动 `python -m http.server`，返回 preview URL

---

## 测试覆盖

测试位于 `server/tests/`：

| 文件 | 类型 | 覆盖内容 |
|------|------|----------|
| `test_runtime.py` | 手动脚本 | WorkflowEngine 简单 start→llm→output 链 |
| `test_workflow_runtime.py` | 手动集成 | 从 DB 读 workflow 运行（依赖本地数据） |
| `test_docker.py` | 连通性检查 | `docker.from_env().version()` |

**缺失：** 无 pytest 结构化用例、无 API 层自动化测试、无前端测试。

---

## 模块依赖总览

```
main.py
 ├── api/* → services/* → models/* + core/*
 ├── runtime/workflow_engine ← workflow_service
 ├── tools/registry ← ai_service, tool_call_service
 └── sandbox_service ← plugin_service

前端 Plaza / Chat / Workflow → axios → 后端 REST
CodingIDE → api/plugin.ts + api/codegen.ts + api/agent.ts → 后端 /plugins
```

---

## 已知架构注意点

1. **前端路由不完整**：知识库相关 View 存在但未注册；Plaza 跳转 `/kb` 会失败。
2. **API 调用不统一**：Coding 模块用 `request.ts`，其余 View 硬编码 axios。
3. **Plugin API 无认证**：部分接口使用固定 `demo_user`，无 JWT 校验。
4. **`validateManifest`**：前端可能调用 `/plugins/{id}/manifest`，后端无对应路由。
5. **`knowledge_service.py`** 为遗留代码，与当前 `kb_service.py` + `Knowledge` 模型不一致。
6. **根 `requirements.txt`** 内容庞杂，实际核心依赖需结合运行环境确认。

---

## 启动方式

**后端：**

```bash
cd server
uvicorn app.main:app --reload --port 8000
```

**前端：**

```bash
cd web
npm run dev
```

- 前端默认端口：5173（占用时自动切换）
- 访问地址：http://localhost:5173/
- 后端地址：http://localhost:8000

详见 `memory/front-end-dev-server-startup.md`。

---

## memory 目录已有文档

| 文件 | 内容 |
|------|------|
| `unified-plaza-ui-implementation.md` | 统一广场 UI 实现记录 |
| `front-end-dev-server-startup.md` | 前端开发服务器启动命令 |
| `ai-agent-platform-overview.md` | 本文档：全项目结构总结 |
