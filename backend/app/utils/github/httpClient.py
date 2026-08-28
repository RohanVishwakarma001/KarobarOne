import httpx

from app.core.configGithub import (
    SHIPROCKET_BASE_URL,
)

from app.utils.github.tokenManager import (
    getToken,
)


class ShiprocketHttpClient:

    def __init__(self):

        self.baseUrl = SHIPROCKET_BASE_URL

    def _headers(self):

        headers = {
            "Content-Type": "application/json"
        }

        token = getToken()

        if token:
            headers["Authorization"] = (
                f"Bearer {token}"
            )

        return headers

    async def get(
        self,
        endpoint: str,
        params=None
    ):

        async with httpx.AsyncClient(
            timeout=30
        ) as client:

            return await client.get(
                self.baseUrl + endpoint,
                params=params,
                headers=self._headers()
            )

    async def post(
        self,
        endpoint: str,
        data=None
    ):

        async with httpx.AsyncClient(
            timeout=30
        ) as client:

            return await client.post(
                self.baseUrl + endpoint,
                json=data,
                headers=self._headers()
            )

    async def put(
        self,
        endpoint: str,
        data=None
    ):

        async with httpx.AsyncClient(
            timeout=30
        ) as client:

            return await client.put(
                self.baseUrl + endpoint,
                json=data,
                headers=self._headers()
            )

    async def delete(
        self,
        endpoint: str
    ):

        async with httpx.AsyncClient(
            timeout=30
        ) as client:

            return await client.delete(
                self.baseUrl + endpoint,
                headers=self._headers()
            )


shiprocketHttpClient = ShiprocketHttpClient()