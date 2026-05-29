import uvicorn
from app.main import app

if __name__ == "__main__":
    # 启动服务，热重载
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)