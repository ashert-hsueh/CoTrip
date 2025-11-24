from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from database.user_database import create_tables
from presentation.user_routes import router as user_router

# 创建FastAPI应用
app = FastAPI()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],  # Vue开发服务器地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(user_router)

# 应用启动事件
@app.on_event("startup")
def startup_event():
    # 创建数据库表
    create_tables()
    print("数据库表创建完成")

# 根路径
@app.get("/")
def read_root():
    return {"message": "CoTrip API 服务运行中"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)