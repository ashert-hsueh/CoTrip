from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from database.database import engine, Base
from presentation.user_routes import router as user_router

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI()

# 健康检查端点
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该限制为特定的源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册用户路由
app.include_router(user_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)