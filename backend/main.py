from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from database.user_database import init_db
from presentation.user_routes import router as user_router

# 创建FastAPI应用
app = FastAPI(
    title="CoTrip API",
    description="CoTrip旅行规划应用后端API",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 前端地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化数据库
@app.on_event("startup")
def startup_event():
    init_db()

# 注册路由
app.include_router(user_router)

# 根路径
@app.get("/")
def read_root():
    return {"message": "Welcome to CoTrip API"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)