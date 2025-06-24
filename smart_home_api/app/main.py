from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from .database import engine, Base, get_db
from .routers import users, homes, devices, device_usage, security_events, analytics, feedback

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 初始化FastAPI
app = FastAPI(
    title="智能家居系统API",
    description="智能家居系统的REST API接口，用于管理智能家居设备、用户、住宅及相关数据分析",
    version="1.0.0",
    openapi_tags=[
        {"name": "用户管理", "description": "用户相关的操作，包括注册、认证、信息管理等"},
        {"name": "住宅管理", "description": "住宅相关的操作，包括添加、更新和删除住宅信息"},
        {"name": "设备管理", "description": "智能设备相关的操作，包括注册、状态监控和控制"},
        {"name": "设备使用记录", "description": "记录和查询设备使用历史"},
        {"name": "安防事件", "description": "记录和处理安全事件"},
        {"name": "用户反馈", "description": "收集和回复用户反馈"},
        {"name": "数据分析", "description": "设备使用频率、能源消耗和使用模式分析"}
    ],
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1, 
        "deepLinking": True, 
        "displayRequestDuration": True,
        "docExpansion": "none"
    }
)

# 挂载静态文件
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/visualizations", StaticFiles(directory="visualizations"), name="visualizations")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该限制为特定域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含各路由
app.include_router(users.router, prefix="/api/users", tags=["用户管理"])
app.include_router(homes.router, prefix="/api/homes", tags=["住宅管理"])
app.include_router(devices.router, prefix="/api/devices", tags=["设备管理"])
app.include_router(device_usage.router, prefix="/api/device-usage", tags=["设备使用记录"])
app.include_router(security_events.router, prefix="/api/security-events", tags=["安防事件"])
app.include_router(feedback.router, prefix="/api/feedback", tags=["用户反馈"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["数据分析"])

@app.get("/")
def read_root():
    return {"message": "欢迎使用智能家居系统API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
