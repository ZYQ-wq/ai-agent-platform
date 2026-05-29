from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 1. 【关键修改】使用 as 关键字给路由起别名，避免和 models 中的 user 重名
from app.api.v1.endpoints import user as user_router, chat as chat_router

# 2. 导入数据库和模型 (用于初始化表结构)
from app.core.database import engine, Base
from app.models import user, memory 

# 创建数据库表 (MVP 简单做法)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Agent Platform MVP", version="0.1.0")

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # MVP 阶段允许所有，生产环境请指定域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. 【关键修改】注册路由时使用我们刚刚定义的别名 (.router)
app.include_router(user_router.router, prefix="/api/v1/user", tags=["User"])
app.include_router(chat_router.router, prefix="/chat", tags=["Chat"])

@app.get("/")
def root():
    return {"message": "AI Agent Platform Backend Running"}