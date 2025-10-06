from supabase import create_client, Client
from app.core.config import settings

class SupabaseConnection:
    def __init__(self):
        try:
            self.client: Client = create_client(
                settings.SUPABASE_URL,
                settings.SUPABASE_SERVICE_KEY
            )
        except Exception as e:
            print(f"Error conectado a Supabase: {e}")

    def get_client(self) -> Client:
        return self.client
    

# Instancia
supabase_db = SupabaseConnection()
supabase = supabase_db.get_client()