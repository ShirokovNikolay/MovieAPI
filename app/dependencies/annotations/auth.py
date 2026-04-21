from typing import Annotated

from fastapi import Depends

from dependencies.auth import (
    get_admin_by_access_token,
    get_user_by_access_token,
    get_user_by_refresh_token,
)

AuthUserIdByAccessTokenDep = Annotated[
    int,
    Depends(
        get_user_by_access_token,
    ),
]

AuthAdminIdByAccessTokenDep = Annotated[
    int,
    Depends(
        get_admin_by_access_token,
    ),
]

AuthUserIdByRefreshTokenDep = Annotated[
    int,
    Depends(
        get_user_by_refresh_token,
    ),
]
