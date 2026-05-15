import anthropic

from api.config import settings

_client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

_EXTRACT_TOOL = {
    "name": "extract_clip_data",
    "description": "Extract structured data from a web clip for a personal knowledge base.",
    "input_schema": {
        "type": "object",
        "properties": {
            "summary": {
                "type": "string",
                "description": "Concise 2-4 sentence summary of the content.",
            },
            "entities": {
                "type": "object",
                "properties": {
                    "keywords":     {"type": "array", "items": {"type": "string"}},
                    "technologies": {"type": "array", "items": {"type": "string"}},
                    "people":       {"type": "array", "items": {"type": "string"}},
                    "places":       {"type": "array", "items": {"type": "string"}},
                    "topics":       {"type": "array", "items": {"type": "string"}},
                },
                "required": ["keywords", "technologies", "people", "places", "topics"],
            },
        },
        "required": ["summary", "entities"],
    },
}


def process_clip(title: str, raw_text: str, url: str) -> dict:
    message = _client.messages.create(
        model=settings.claude_model,
        max_tokens=1024,
        tools=[_EXTRACT_TOOL],
        tool_choice={"type": "tool", "name": "extract_clip_data"},
        messages=[{
            "role": "user",
            "content": (
                f"Title: {title}\n"
                f"URL: {url}\n\n"
                f"Content:\n{raw_text[:12000]}"
            ),
        }],
    )

    tool_block = next(b for b in message.content if b.type == "tool_use")
    return tool_block.input

