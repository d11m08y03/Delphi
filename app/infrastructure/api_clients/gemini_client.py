import httpx


class GeminiClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key

    async def call_gemini(self, payload: dict) -> dict:
        headers = {"Authorization": f"Bearer {self.api_key}"}
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/endpoint", json=payload, headers=headers
            )
            response.raise_for_status()
            return response.json()
