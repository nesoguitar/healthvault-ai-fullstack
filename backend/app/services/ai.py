"""
AI provider abstraction for the chat assistant and embeddings.

AI_PROVIDER=mock   -> canned, deterministic responses. No API key needed;
                      this is the default so the API runs out of the box.
AI_PROVIDER=azure  -> Azure OpenAI (recommended for production: data stays
                      in your Azure tenant, supports BAA coverage).
AI_PROVIDER=openai -> public OpenAI, useful for local dev experimentation.

All three implement the same `AIProvider` interface, so `app/api/v1/endpoints/chat.py`
never branches on provider.
"""
from abc import ABC, abstractmethod

from app.core.config import settings

SYSTEM_PROMPT = """You are the HealthVault AI assistant. You answer questions about a \
single patient's own medical record using ONLY the context provided below \
(their conditions, medications, allergies, lab results, and timeline events). \

Rules:
- Ground every factual claim in the provided context. If the answer isn't in \
the context, say so plainly and suggest what the patient could upload or ask \
their care team.
- Never invent dates, values, or medication names.
- You are not a substitute for medical advice. For anything that sounds like \
a request for diagnosis, treatment changes, or an emergency, direct the \
patient to their care team or emergency services.
- Be concise and use plain language.
"""

MOCK_RESPONSES: dict[str, str] = {
    "when was my last colonoscopy?": (
        "I don't see a colonoscopy in your uploaded records or timeline. "
        "If you've had one elsewhere, upload the report and I'll add it."
    ),
    "what medications am i taking?": (
        "Based on your record, here are your active medications. "
        "(Connect a real AI provider to have this answer generated from your live data.)"
    ),
    "show my diabetes history.": (
        "Here's a summary of your diabetes-related events from your timeline. "
        "(Connect a real AI provider to have this answer generated from your live data.)"
    ),
    "what were my latest laboratory results?": (
        "Here are your most recent lab results. "
        "(Connect a real AI provider to have this answer generated from your live data.)"
    ),
}

DEFAULT_MOCK_RESPONSE = (
    "I looked through your health record, but I don't have enough context to "
    "answer that precisely in mock mode. Set AI_PROVIDER=azure or openai and "
    "configure credentials to enable real, record-grounded answers."
)


class AIProvider(ABC):
    @abstractmethod
    def chat_completion(self, *, system_prompt: str, context: str, user_message: str) -> str:
        ...

    @abstractmethod
    def embed(self, text: str) -> list[float]:
        ...


class MockAIProvider(AIProvider):
    def chat_completion(self, *, system_prompt: str, context: str, user_message: str) -> str:
        return MOCK_RESPONSES.get(user_message.strip().lower(), DEFAULT_MOCK_RESPONSE)

    def embed(self, text: str) -> list[float]:
        # Deterministic pseudo-embedding so pgvector similarity search still
        # "works" end-to-end in mock mode without calling any external API.
        import hashlib

        digest = hashlib.sha256(text.encode()).digest()
        values = [(b / 255.0) * 2 - 1 for b in digest]
        dim = settings.EMBEDDING_DIMENSIONS
        return (values * (dim // len(values) + 1))[:dim]


class AzureOpenAIProvider(AIProvider):
    def __init__(self) -> None:
        from openai import AzureOpenAI

        self._client = AzureOpenAI(
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
            api_key=settings.AZURE_OPENAI_API_KEY,
            api_version=settings.AZURE_OPENAI_API_VERSION,
        )

    def chat_completion(self, *, system_prompt: str, context: str, user_message: str) -> str:
        response = self._client.chat.completions.create(
            model=settings.AZURE_OPENAI_CHAT_DEPLOYMENT,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "system", "content": f"Patient record context:\n{context}"},
                {"role": "user", "content": user_message},
            ],
            temperature=0.2,
            max_tokens=600,
        )
        return response.choices[0].message.content or ""

    def embed(self, text: str) -> list[float]:
        response = self._client.embeddings.create(
            model=settings.AZURE_OPENAI_EMBEDDING_DEPLOYMENT, input=text
        )
        return response.data[0].embedding


class OpenAIProvider(AIProvider):
    def __init__(self) -> None:
        from openai import OpenAI

        self._client = OpenAI()  # reads OPENAI_API_KEY from env

    def chat_completion(self, *, system_prompt: str, context: str, user_message: str) -> str:
        response = self._client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "system", "content": f"Patient record context:\n{context}"},
                {"role": "user", "content": user_message},
            ],
            temperature=0.2,
            max_tokens=600,
        )
        return response.choices[0].message.content or ""

    def embed(self, text: str) -> list[float]:
        response = self._client.embeddings.create(model="text-embedding-3-small", input=text)
        return response.data[0].embedding


def get_ai_provider() -> AIProvider:
    if settings.AI_PROVIDER == "azure":
        return AzureOpenAIProvider()
    if settings.AI_PROVIDER == "openai":
        return OpenAIProvider()
    return MockAIProvider()
