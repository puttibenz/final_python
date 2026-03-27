from database.connection import supabase

class ProfileRepository:
    """
    Manages extra user information in the 'profiles' table.
    Links to Supabase Auth via the user ID.
    """
    def __init__(self):
        self.table_name = "profiles"

    def create_profile(self, user_id, username, email, full_name=None):
        """Creates a new profile linked to a Supabase Auth user."""
        if not supabase: return None
        data = {
            "id": user_id,
            "username": username,
            "email": email,
            "full_name": full_name,
            "role": "user"
        }
        try:
            return supabase.table(self.table_name).insert(data).execute()
        except Exception as e:
            print(f"❌ Profile Create Error: {e}")
            return None

    def get_profile(self, user_id):
        """Retrieves a profile by user ID."""
        if not supabase: return None
        try:
            result = supabase.table(self.table_name).select("*").eq("id", user_id).maybe_single().execute()
            return result.data
        except Exception as e:
            print(f"❌ Get Profile Error: {e}")
            return None

class CampRepository:
    """Manages Camping Trip data in Supabase."""
    def __init__(self):
        self.table_name = "camps"

    def create(self, camp_data: dict):
        """Inserts a new camp and sets available_slots."""
        if not supabase: return None
        if 'slots' in camp_data and 'available_slots' not in camp_data:
            camp_data['available_slots'] = camp_data['slots']
        try:
            return supabase.table(self.table_name).insert(camp_data).execute()
        except Exception as e:
            print(f"❌ Create Camp Error: {e}")
            return None

    def get_all(self):
        """Retrieves all camp records."""
        if not supabase: return []
        try:
            result = supabase.table(self.table_name).select("*").order("created_at", desc=True).execute()
            return result.data
        except Exception as e:
            print(f"❌ Get All Error: {e}")
            return []

class BookingRepository:
    """Manages Bookings in Supabase."""
    def __init__(self):
        self.table_name = "bookings"

    def create_booking(self, user_id: str, camp_id: int):
        """Creates a booking record. Slot reduction handled by SQL Trigger."""
        if not supabase: return None
        try:
            data = {"user_id": user_id, "camp_id": camp_id}
            return supabase.table(self.table_name).insert(data).execute()
        except Exception as e:
            return {"error": str(e)}

# Global instances
profile_repo = ProfileRepository()
camp_repo = CampRepository()
booking_repo = BookingRepository()
