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
        allowed = {"username", "full_name", "avatar_url", "bio", "role", "phone", "balance"}
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
                # 1. เช็คว่าเคยจองไปหรือยัง
                cur.execute("SELECT id FROM bookings WHERE user_id = %s AND camp_id = %s AND status != 'cancelled'", (user_id, camp_id))
                if cur.fetchone():
                    return {"error": "คุณได้จองทริปนี้ไปแล้ว"}

                # 2. เช็ค slot ว่างก่อน
                cur.execute("SELECT available_slots FROM camps WHERE id = %s", (camp_id,))
                camp = cur.fetchone()
                if not camp or camp["available_slots"] <= 0:
                    return {"error": "ทริปนี้เต็มแล้ว"}
                
                # 3. สร้าง booking + ลด slot
                cur.execute("INSERT INTO bookings (user_id, camp_id) VALUES (%s, %s)", (user_id, camp_id))
                booking_id = cur.lastrowid
                
                cur.execute("UPDATE camps SET available_slots = available_slots - 1 WHERE id = %s", (camp_id,))
                conn.commit()
                return booking_id
        except Exception as e:
            conn.rollback()
            return {"error": str(e)}
        finally:
            conn.close()

    def get_user_bookings(self, user_id: int):
        """ดึง camp_id ที่ user จองไว้ (สำหรับ Explore page)"""
        conn = get_connection()
        if not conn: return []
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT camp_id FROM bookings WHERE user_id = %s", (user_id,))
                return [row["camp_id"] for row in cur.fetchall()]
        except Exception as e:
            print(f"❌ Get User Bookings Error: {e}")
            return []
        finally:
            conn.close()

    def get_user_bookings_detail(self, user_id: int):
        """ดึง bookings ของ user พร้อมข้อมูล camp (สำหรับ Profile page)"""
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
            print(f"❌ Get User Bookings Detail Error: {e}")
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
                        SUM(CASE WHEN b.status = 'completed' THEN 1 ELSE 0 END) AS completed,
                        COALESCE(SUM(CASE WHEN b.status != 'cancelled' THEN c.price ELSE 0 END), 0) AS total_spent
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

    def get_all_bookings_detail(self):
        """ดึง bookings ทั้งหมดพร้อมข้อมูล camp และ user (สำหรับ Admin)"""
        conn = get_connection()
        if not conn: return []
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT b.id, b.status, b.created_at AS booked_at,
                           c.name AS camp_name, c.price, u.username, u.email
                    FROM bookings b
                    JOIN camps c ON b.camp_id = c.id
                    JOIN users u ON b.user_id = u.id
                    ORDER BY b.created_at DESC
                """)
                return cur.fetchall()
        except Exception as e:
            print(f"❌ Get All Bookings Detail Error: {e}")
            return []
        finally:
            conn.close()

    def get_booking_by_id(self, booking_id: int):
        """ดึงข้อมูล booking ตาม ID พร้อมข้อมูล camp"""
        conn = get_connection()
        if not conn: return None
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT b.*, c.name AS camp_name, c.price, c.created_by AS owner_id
                    FROM bookings b
                    JOIN camps c ON b.camp_id = c.id
                    WHERE b.id = %s
                """, (booking_id,))
                return cur.fetchone()
        except Exception as e:
            print(f"❌ Get Booking By ID Error: {e}")
            return None
        finally:
            conn.close()

    def complete_payment(self, booking_id: int):
        """ยืนยันการชำระเงิน และโอนเงินให้เจ้าของแคมป์ (Mock)"""
        conn = get_connection()
        if not conn: 
            print("❌ Complete Payment Error: No database connection")
            return False
        try:
            with conn.cursor() as cur:
                # 1. ดึงข้อมูล booking และราคา
                cur.execute("""
                    SELECT b.id, b.status, c.price, c.created_by AS owner_id
                    FROM bookings b
                    JOIN camps c ON b.camp_id = c.id
                    WHERE b.id = %s
                """, (booking_id,))
                booking = cur.fetchone()

                if not booking:
                    print(f"❌ Complete Payment Error: Booking ID {booking_id} not found")
                    return False
                
                if booking['status'] != 'pending_payment':
                    print(f"❌ Complete Payment Error: Booking status is '{booking['status']}', expected 'pending_payment'")
                    return False

                # 2. อัปเดตสถานะ booking เป็น confirmed
                cur.execute("UPDATE bookings SET status = 'confirmed' WHERE id = %s", (booking_id,))

                # 3. โอนเงินให้เจ้าของ (เพิ่ม balance)
                if booking['owner_id']:
                    # Ensure balance column exists and price is numeric
                    cur.execute("UPDATE users SET balance = balance + %s WHERE id = %s", (booking['price'] or 0, booking['owner_id']))

                conn.commit()
                return True
        except Exception as e:
            if conn: conn.rollback()
            print(f"❌ Complete Payment Error Exception: {e}")
            return False
        finally:
            if conn: conn.close()

    def update_booking_status(self, booking_id: int, status: str):
        """อัปเดตสถานะการจอง (confirmed, cancelled, completed)"""
        conn = get_connection()
        if not conn: return False
        try:
            with conn.cursor() as cur:
                # ถ้าเปลี่ยนเป็น cancelled ให้คืน slot
                if status == 'cancelled':
                    cur.execute("SELECT status, camp_id FROM bookings WHERE id = %s", (booking_id,))
                    booking = cur.fetchone()
                    if booking and booking['status'] != 'cancelled':
                        cur.execute("UPDATE camps SET available_slots = available_slots + 1 WHERE id = %s", (booking['camp_id'],))
                
                cur.execute("UPDATE bookings SET status = %s WHERE id = %s", (status, booking_id))
                conn.commit()
                return True
        except Exception as e:
            print(f"❌ Update Booking Status Error: {e}")
            return False
        finally:
            conn.close()


# Global instances
user_repo = UserRepository()
camp_repo = CampRepository()
booking_repo = BookingRepository()
