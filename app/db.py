from supabase import Client, create_client

from app.config import settings

# Service-role client bypasses RLS; always scope writes to the authenticated user_id.
_client: Client = create_client(settings.supabase_url, settings.supabase_service_role_key)


def get_supabase() -> Client:
    return _client
