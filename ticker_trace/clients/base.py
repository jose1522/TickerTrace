import httpx


class AsyncHTTPClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def add_header(self, key: str, value: str):
        self.headers[key] = value

    async def get(self, url: str, **kwargs):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}{url}", headers=self.headers, **kwargs
            )
            response.raise_for_status()
            return response.json()

    async def post(self, url: str, data: dict, **kwargs):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}{url}", data=data, headers=self.headers, **kwargs
            )
            response.raise_for_status()
            return response.json()

    async def put(self, url: str, data: dict, **kwargs):
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{self.base_url}{url}", data=data, headers=self.headers, **kwargs
            )
            response.raise_for_status()
            return response.json()

    async def delete(self, url: str, **kwargs):
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{self.base_url}{url}", headers=self.headers, **kwargs
            )
            response.raise_for_status()
            return response.json()
