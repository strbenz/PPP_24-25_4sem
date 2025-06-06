from fastapi import FastAPI
from .database import engine, Base
from .routers import users, posts

# При старте приложения создаём все таблицы (если их ещё нет)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Users and Posts API")

# Подключаем роутеры
app.include_router(users.router)
app.include_router(posts.router)
