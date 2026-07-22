import json

import httpx

from app.core.config import get_settings
from app.services.summarization.base import SummarizationProvider, SummaryOutput


SYSTEM_PROMPT = (
    "You are a neutral news briefing assistant. Use only the provided metadata and snippet. "
    "Return strict JSON with keys: summary, why_this_matters, key_impact. "
    "summary must be 50-60 words, factual and concise. Do not copy the headline wording."
)


class OpenAISummarizationProvider(SummarizationProvider):
    provider_name = "openai"

    def summarize(self, title: str, snippet: str | None, source_name: str) -> SummaryOutput:
        settings = get_settings()
        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY is not configured")

        user_prompt = (
            f"Source: {source_name}\nTitle: {title}\nSnippet: {snippet or 'N/A'}\n"
            "Respond in JSON only."
        )
        response = httpx.post(
            "https://api.openai.com/v1/responses",
            headers={
                "Authorization": f"Bearer {settings.openai_api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-4.1-mini",
                "input": [
                    {"role": "system", "content": [{"type": "text", "text": SYSTEM_PROMPT}]},
                    {"role": "user", "content": [{"type": "text", "text": user_prompt}]},
                ],
            },
            timeout=20.0,
        )
        response.raise_for_status()
        payload = response.json()
        text = payload["output"][0]["content"][0]["text"]
        parsed = json.loads(text)
        return SummaryOutput(
            summary=" ".join(parsed["summary"].split()[:60]),
            why_this_matters=parsed["why_this_matters"],
            key_impact=parsed.get("key_impact"),
            quality_flags=[],
        )
