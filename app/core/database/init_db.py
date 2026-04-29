from core.database import session_factory
from schemas.user import UserCreate
from services import UserService


async def init_admin() -> None:
    async with session_factory() as session:
        user_service = UserService(session)
        if not await user_service.user_login_exists("adminadmin"):
            create_user_data = UserCreate(
                surname="admin",
                name="admin",
                login="adminadmin",
                email="admin@admin.gmail.ru",
                password="adminadmin",  # noqa: S106
            )
            await user_service.create_user(create_user_data)
            admin = await user_service.get_user_by_login("adminadmin")
            await user_service.make_admin(admin.id)
