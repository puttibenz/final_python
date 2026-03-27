import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

class SupabaseManager:
    """
    A class to manage the connection to Supabase.
    Uses the Singleton pattern to ensure only one client exists.
    """
    _client: Client = None

    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        
        if not self.url or not self.key:
            print("⚠️ Warning: SUPABASE_URL or SUPABASE_KEY not found in .env file.")

    def get_client(self) -> Client:
        """Returns the Supabase client, initializing it if necessary."""
        if not self._client and self.url and self.key:
            try:
                self._client = create_client(self.url, self.key)
                print("✅ Supabase client initialized successfully.")
            except Exception as e:
                print(f"❌ Error initializing Supabase client: {e}")
        return self._client

# Create a global instance
db_manager = SupabaseManager()
supabase = db_manager.get_client()
