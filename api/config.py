from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    supabase_url: str
    supabase_service_role_key: str
    supabase_jwt_secret: str
    anthropic_api_key: str
    voyage_api_key: str
    claude_model: str = "claude-sonnet-4-6"

    model_config = {"env_file": ".env"}


settings = Settings()

