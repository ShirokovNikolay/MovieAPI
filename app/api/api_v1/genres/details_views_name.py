from typing import Annotated

from fastapi import Depends, APIRouter, status
from dependencies.auth import get_admin_by_access_token
from dependencies.services import get_genre_service
from schemas.genre import GenreResponse
from services import GenreService

router = APIRouter(
    prefix="/{genre_name}",
)


@router.get(
    "/",
    response_model=GenreResponse,
    status_code=status.HTTP_200_OK,
)
async def search_genres_by_name(
    genre_name: str,
    genre_service: Annotated[
        GenreService,
        Depends(get_genre_service),
    ],
):
    return await genre_service.search_genres_by_name(genre_name)
