from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI

from app.api.user import router as user_router
from app.api.chat import router as chat_router
from app.api.agent import router as agent_router
from app.api.workflow import router as workflow_router
from app.api.knowledge import router as knowledge_router
from app.api.plugin import router as plugin_router


from app.core.database import Base,engine

from app.models.user import User
from app.models.memory import Memory
from app.models.agent import Agent
from app.models.memory_summary import MemorySummary
from app.models.plugin_project import PluginProject
from app.models.plugin_file import PluginFile

from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)

app.include_router(
    chat_router, 
    prefix="/chat", 
    tags=["Chat"]
)

app.include_router(
    agent_router,
    prefix="/agents",
    tags=["Agents"]
)

app.include_router(
    workflow_router,
    prefix="/workflow",
    tags=["Workflow"]
)

app.include_router(
    knowledge_router,
    prefix="/kb",
    tags=["Knowledge Base"]
)

app.include_router(
    plugin_router,
    tags=["Plugins"]
)


@app.get("/")
def root():
    return {
        "message": "AI Agent Platform Backend Running"
    }
