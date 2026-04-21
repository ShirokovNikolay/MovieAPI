from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from dependencies.auth import (
    get_admin_by_access_token,
    get_user_by_access_token,
    get_user_by_refresh_token,
)

AuthUserByAccessTokenDep = Annotated[
    int,
    Depends(
        get_user_by_access_token,
    ),
]

AuthAdminByAccessTokenDep = Annotated[
    int,
    Depends(
        get_admin_by_access_token,
    ),
]

AuthUserByRefreshTokenDep = Annotated[
    int,
    Depends(
        get_user_by_refresh_token,
    ),
]

OAuth2Dep = Annotated[
    OAuth2PasswordRequestForm,
    Depends(),
]
