from fastapi import FastAPI
import uvicorn
from presentation.user_routes import router as user_router
from presentation.ledger_routes import router as ledger_router
from database import create_tables
from fastapi.middleware.cors import CORSMiddleware

# 创建FastAPI应用
app = FastAPI(title="CoTrip API", version="1.0.0")

# 添加跨域中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建数据库表
create_tables()

# 包含路由
app.include_router(user_router)
app.include_router(ledger_router)

# 根路径
@app.get("/")
async def root():
    return {"message": "Welcome to CoTrip API"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
