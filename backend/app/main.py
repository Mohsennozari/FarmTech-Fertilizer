# Platform-v3\backend\app\main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router
import logging

# تنظیم لاگینگ
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ایجاد اپلیکیشن FastAPI
app = FastAPI(
    title="FarmTech API",
    description="سیستم هوشمند نسخه‌دهی کود دیجیتال",
    version="3.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# تنظیم CORS برای ارتباط با فرانت‌اند
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# اضافه کردن router با prefix /api/v1
app.include_router(router)

# مسیر اصلی برای تست
@app.get("/")
def root():
    return {
        "message": "FarmTech API is running",
        "version": "3.1.0",
        "docs": "/docs",
        "api": "/api/v1"
    }

# مسیر سلامت ساده بدون prefix (برای تست سریع)
@app.get("/health")
def simple_health():
    return {"status": "ok", "server": "running"}

# رویداد استارتاپ
@app.on_event("startup")
async def startup_event():
    logger.info("FarmTech API Server Started Successfully")
    logger.info("API Documentation available at /docs")

# رویداد شات‌داون
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("FarmTech API Server Shutting Down")