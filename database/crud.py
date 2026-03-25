from database.connection import supabase

class CampRepository:
    """
    A class-based Repository for managing Camping Trip data in Supabase.
    Follows CRUD (Create, Read, Update, Delete) patterns.
    """
    def __init__(self):
        self.table_name = "camps"

    def create(self, camp_data: dict):
        """
        Inserts a new camp record into Supabase.
        Ensures available_slots is initially equal to total slots.
        """
        if not supabase:
            print("❌ Database not connected.")
            return None
            
        # Initialize available_slots to be equal to slots if not provided
        if 'slots' in camp_data and 'available_slots' not in camp_data:
            camp_data['available_slots'] = camp_data['slots']
            
        try:
            result = supabase.table(self.table_name).insert(camp_data).execute()
            return result
        except Exception as e:
            print(f"❌ CRUD Error (create): {e}")
            return None

    def get_all(self):
        """Retrieves all camp records from the database."""
        if not supabase:
            return []
            
        try:
            result = supabase.table(self.table_name).select("*").order("created_at", desc=True).execute()
            return result.data
        except Exception as e:
            print(f"❌ CRUD Error (get_all): {e}")
            return []

class BookingRepository:
    """
    A class-based Repository for managing Bookings in Supabase.
    """
    def __init__(self):
        self.table_name = "bookings"

    def create_booking(self, user_name: str, camp_id: int):
        """
        Creates a new booking record. 
        Note: Slot reduction is handled by the SQL Trigger in Supabase.
        """
        if not supabase:
            return None
            
        try:
            data = {
                "user_name": user_name,
                "camp_id": camp_id
            }
            result = supabase.table(self.table_name).insert(data).execute()
            return result
        except Exception as e:
            # Captures the RAISE EXCEPTION '❌ ขออภัยครับ ทริปนี้เต็มแล้ว!' from the trigger
            return {"error": str(e)}

# Global instances
camp_repo = CampRepository()
booking_repo = BookingRepository()
