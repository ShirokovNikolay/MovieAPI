from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import session_factory
from schemas.user import UserCreate, UserResponse
from services import UserService


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Действия до старта приложения.
    """
    async with session_factory() as session:
        user_service = UserService(session)
        if not await user_service.user_login_exists("admin"):
            create_user_data = UserCreate(
                surname="admin",
                name="admin",
                login="admin",
                email="admin@admin.gmail.ru",
                password="admin",
            )
            await user_service.create_user(create_user_data)
            admin: UserResponse = await user_service.get_user_by_login("admin")
            await user_service.make_admin(admin.id)
    yield
    """
    Действия после заверения работы приложения.
    """
