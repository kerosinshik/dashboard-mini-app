from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database.models import init_db
from api.routes import router
import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Инициализация при старте приложения"""
    # Инициализация БД
    await init_db()
    print("✅ База данных инициализирована")
    yield
    # Cleanup при завершении
    print("👋 API сервер остановлен")


# Создание FastAPI приложения
app = FastAPI(
    title="Dashboard Mini App API",
    description="API для Telegram Mini App с дашбордом продаж",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware для работы с Mini App
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(router, prefix="/api", tags=["api"])


@app.get("/")
async def root():
    """Корневой эндпоинт"""
    return {
        "message": "Dashboard Mini App API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Проверка здоровья сервиса"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("API_PORT", 8000))
    debug = os.getenv("DEBUG", "True") == "True"

    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=port,
        reload=debug
    )
