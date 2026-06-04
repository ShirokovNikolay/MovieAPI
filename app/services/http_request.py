from typing import Any

from httpx import AsyncClient, Response

from core.constants import AnyPydanticType, MethodType, PrimitiveType


class HttpRequestService:
    def __init__(self, http_request_client: AsyncClient) -> None:
        self.http_request_client = http_request_client

    async def get(
        self,
        url: str,
        params: dict[str, PrimitiveType] | None = None,
        headers: dict[str, PrimitiveType] | None = None,
        cookies: dict[str, PrimitiveType] | None = None,
    ) -> Response:
        response = await self.http_request_client.get(
            url=url,
            params=params,
            headers=headers,  # type: ignore[arg-type]
            cookies=cookies,  # type: ignore[arg-type]
        )
        return response

    async def post(
        self,
        url: str,
        json: dict[str, PrimitiveType],
        params: dict[str, PrimitiveType] | None = None,
        headers: dict[str, PrimitiveType] | None = None,
        cookies: dict[str, PrimitiveType] | None = None,
    ) -> Response:
        response = await self.http_request_client.post(
            url=url,
            json=json,
            params=params,
            headers=headers,  # type: ignore[arg-type]
            cookies=cookies,  # type: ignore[arg-type]
        )
        return response

    async def put(
        self,
        url: str,
        json: dict[str, PrimitiveType],
        params: dict[str, PrimitiveType] | None = None,
        headers: dict[str, PrimitiveType] | None = None,
        cookies: dict[str, PrimitiveType] | None = None,
    ) -> Response:
        response = await self.http_request_client.put(
            url=url,
            json=json,
            params=params,
            headers=headers,  # type: ignore[arg-type]
            cookies=cookies,  # type: ignore[arg-type]
        )
        return response

    async def patch(
        self,
        url: str,
        json: dict[str, PrimitiveType],
        params: dict[str, PrimitiveType] | None = None,
        headers: dict[str, PrimitiveType] | None = None,
        cookies: dict[str, PrimitiveType] | None = None,
    ) -> Response:
        response = await self.http_request_client.patch(
            url=url,
            json=json,
            params=params,
            headers=headers,  # type: ignore[arg-type]
            cookies=cookies,  # type: ignore[arg-type]
        )
        return response

    async def delete(
        self,
        url: str,
        params: dict[str, PrimitiveType] | None = None,
        headers: dict[str, PrimitiveType] | None = None,
        cookies: dict[str, PrimitiveType] | None = None,
    ) -> Response:
        response = await self.http_request_client.delete(
            url=url,
            params=params,
            headers=headers,  # type: ignore[arg-type]
            cookies=cookies,  # type: ignore[arg-type]
        )
        return response

    async def get_schema_from_request(
        self,
        url: str,
        method: MethodType,
        response_schema: AnyPydanticType,
        **kwargs: Any,
    ) -> AnyPydanticType:
        methods = {
            MethodType.get.value: self.get,
            MethodType.post.value: self.post,
            MethodType.put.value: self.put,
            MethodType.patch.value: self.patch,
            MethodType.delete.value: self.delete,
        }
        service_method = methods[method]
        response = await service_method(url, **kwargs)  # type: ignore[operator]
        json = response.json()
        return response_schema(**json)  # type: ignore[no-any-return, operator]
