from core.database import session_factory
from schemas.user import UserCreate, UserResponse
from services import UserService


async def init_admin():
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
