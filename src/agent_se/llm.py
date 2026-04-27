from __future__ import annotations

from dataclasses import dataclass

import httpx


@dataclass
class ChatRequest:
    prompt: str
    model: str
    api_key: str | None = None
    base_url: str = "https://integrate.api.nvidia.com/v1"


class LLMGateway:
    """OpenAI-compatible client with safe fallback when no API key is provided."""

    async def complete(self, request: ChatRequest) -> str:
        if not request.api_key:
            return self._offline_response(request.prompt, request.model)

        payload = {
            "model": request.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a senior software engineering AI agent.",
                },
                {"role": "user", "content": request.prompt},
            ],
            "temperature": 0.6,
            "top_p": 0.95,
            "max_tokens": 1200,
        }
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{request.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {request.api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]

    def _offline_response(self, prompt: str, model: str) -> str:
        return (
            f"[OFFLINE MODE - {model}]\n"
            f"Ricevuto prompt: {prompt[:400]}\n"
            "Suggerimento: imposta una API key per ottenere risposta reale dal provider."
        )
