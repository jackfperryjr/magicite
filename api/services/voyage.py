import voyageai

from api.config import settings

_client = voyageai.Client(api_key=settings.voyage_api_key)


def embed(text: str) -> list[float]:
    result = _client.embed([text[:30000]], model="voyage-3")
    return result.embeddings[0]

