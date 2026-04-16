import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.database import engine, Base
from app.routers import (
    auth, account, roles, subject_types, localities,
    statuses, change_types, employees, clients,
    addresses, requests, appointments, attachments,
    comments, history_logs,
)

# Создаём все таблицы при старте
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SkatEnergo API", version="1.0.0")

# CORS — разрешаем любые источники (как в оригинале)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Статические файлы для загрузок
UPLOADS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
os.makedirs(UPLOADS_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")

# Подключаем все роутеры
app.include_router(auth.router)
app.include_router(account.router)
app.include_router(roles.router)
app.include_router(subject_types.router)
app.include_router(localities.router)
app.include_router(statuses.router)
app.include_router(change_types.router)
app.include_router(employees.router)
app.include_router(clients.router)
app.include_router(addresses.router)
app.include_router(requests.router)
app.include_router(appointments.router)
app.include_router(attachments.router)
app.include_router(comments.router)
app.include_router(history_logs.router)
