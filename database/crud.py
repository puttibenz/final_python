from database.connection import get_connection


class UserRepository:
    """จัดการข้อมูล users"""

    def create_user(self, username, email, password_hash, full_name=None, phone=None):
        conn = get_connection()
        if not conn: return None
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO users (username, email, password_hash, full_name, phone) VALUES (%s, %s, %s, %s, %s)",
                    (username, email, password_hash, full_name, phone)
                )
                conn.commit()
                return cur.lastrowid
        except Exception as e:
            print(f"❌ Create User Error: {e}")
            return None
        finally:
            conn.close()

    def get_user_by_email(self, email):
        conn = get_connection()
        if not conn: return None
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM users WHERE email = %s", (email,))
                return cur.fetchone()
        except Exception as e:
            print(f"❌ Get User Error: {e}")
            return None
        finally:
            conn.close()

    def get_user_by_id(self, user_id):
        conn = get_connection()
        if not conn: return None
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
                return cur.fetchone()
        except Exception as e:
            print(f"❌ Get User Error: {e}")
            return None
        finally:
            conn.close()

    def update_user(self, user_id, **kwargs):
        allowed = {"username", "full_name", "avatar_url", "bio", "role", "phone"}
        data = {k: v for k, v in kwargs.items() if k in allowed}
        if not data:
            return None
        conn = get_connection()
        if not conn: return None
        try:
            sets = ", ".join(f"{k} = %s" for k in data)
            vals = list(data.values()) + [user_id]
            with conn.cursor() as cur:
                cur.execute(f"UPDATE users SET {sets} WHERE id = %s", vals)
                conn.commit()
                return True
        except Exception as e:
            print(f"❌ Update User Error: {e}")
            return None
        finally:
            conn.close()


class CampRepository:
    """จัดการข้อมูล camps"""

    def create(self, camp_data: dict):
        conn = get_connection()
        if not conn: return None
        if 'slots' in camp_data and 'available_slots' not in camp_data:
            camp_data['available_slots'] = camp_data['slots']
        try:
            keys = ", ".join(camp_data.keys())
            placeholders = ", ".join(["%s"] * len(camp_data))
            with conn.cursor() as cur:
                cur.execute(f"INSERT INTO camps ({keys}) VALUES ({placeholders})", list(camp_data.values()))
                conn.commit()
                return cur.lastrowid
        except Exception as e:
            print(f"❌ Create Camp Error: {e}")
            return None
        finally:
            conn.close()

    def get_all(self):
        conn = get_connection()
        if not conn: return []
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM camps ORDER BY created_at DESC")
                return cur.fetchall()
        except Exception as e:
            print(f"❌ Get All Camps Error: {e}")
            return []
        finally:
            conn.close()


class BookingRepository:
    """จัดการข้อมูล bookings"""

    def create_booking(self, user_id: int, camp_id: int):
        conn = get_connection()
        if not conn: return None
        try:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO bookings (user_id, camp_id) VALUES (%s, %s)", (user_id, camp_id))
                conn.commit()
                return cur.lastrowid
        except Exception as e:
            return {"error": str(e)}
        finally:
            conn.close()

    def get_user_bookings(self, user_id: int):
        """ดึง bookings ของ user พร้อมข้อมูล camp (JOIN)"""
        conn = get_connection()
        if not conn: return []
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT b.id, b.status, b.created_at AS booked_at,
                           c.name AS camp_name, c.location, c.price,
                           c.image_url, c.start_date, c.duration
                    FROM bookings b
                    JOIN camps c ON b.camp_id = c.id
                    WHERE b.user_id = %s
                    ORDER BY b.created_at DESC
                """, (user_id,))
                return cur.fetchall()
        except Exception as e:
            print(f"❌ Get User Bookings Error: {e}")
            return []
        finally:
            conn.close()

    def get_user_stats(self, user_id: int):
        """สถิติการจองของ user"""
        conn = get_connection()
        if not conn: return {}
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT
                        COUNT(*) AS total_bookings,
                        SUM(CASE WHEN b.status = 'confirmed' THEN 1 ELSE 0 END) AS confirmed,
                        SUM(CASE WHEN b.status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled,
                        COALESCE(SUM(c.price), 0) AS total_spent
                    FROM bookings b
                    JOIN camps c ON b.camp_id = c.id
                    WHERE b.user_id = %s
                """, (user_id,))
                return cur.fetchone()
        except Exception as e:
            print(f"❌ Get User Stats Error: {e}")
            return {}
        finally:
            conn.close()


# Global instances
user_repo = UserRepository()
camp_repo = CampRepository()
booking_repo = BookingRepository()
