# database/crud.py
import gspread

class DatabaseCRUD:
    def __init__(self, sh):
        self.sh = sh
        self.camp_sheet = self.sh.worksheet("Camp")
        self.users_sheet = self.sh.worksheet("Users")
        self.booking_sheet = self.sh.worksheet("Booking")
        
        try:
            self.payment_sheet = self.sh.worksheet("Payments")
        except gspread.exceptions.WorksheetNotFound:
            self.payment_sheet = None

    # ==========================================
    # หมวดหมู่: Camp
    # ==========================================
    def get_all_camps(self):
        try:
            return self.camp_sheet.get_all_values()
        except Exception as e:
            print(f"❌ ดึงข้อมูล Camps ไม่สำเร็จ: {e}")
            return []

    def add_new_camp(self, camp_data):
        try:
            self.camp_sheet.append_row(camp_data)
            return True
        except Exception as e:
            print(f"❌ เพิ่มข้อมูล Camp ไม่สำเร็จ: {e}")
            return False

    def delete_camp(self, row_index):
        try:
            self.camp_sheet.delete_rows(row_index)
            return True
        except Exception as e:
            print(f"❌ ลบค่ายไม่สำเร็จ: {e}")
            return False

    def update_camp(self, row_index, camp_data):
        try:
            end_col_letter = chr(64 + len(camp_data)) 
            cell_range = f"A{row_index}:{end_col_letter}{row_index}"
            self.camp_sheet.update(range_name=cell_range, values=[camp_data])
            return True
        except Exception as e:
            print(f"❌ แก้ไขค่ายไม่สำเร็จ: {e}")
            return False

    # ==========================================
    # หมวดหมู่: Users
    # ==========================================
    def get_all_users(self):
        try:
            return self.users_sheet.get_all_values()
        except Exception as e:
            print(f"❌ ดึงข้อมูล Users ไม่สำเร็จ: {e}")
            return []

    def add_new_user(self, user_data):
        try:
            self.users_sheet.append_row(user_data)
            return True
        except Exception as e:
            print(f"❌ เพิ่มข้อมูล User ไม่สำเร็จ: {e}")
            return False

    # ==========================================
    # หมวดหมู่: Bookings
    # ==========================================
    def get_all_bookings(self):
        try:
            return self.booking_sheet.get_all_values()
        except Exception as e:
            print(f"❌ ดึงข้อมูล Bookings ไม่สำเร็จ: {e}")
            return []

    def add_new_booking(self, booking_data):
        try:
            self.booking_sheet.append_row(booking_data)
            return True
        except Exception as e:
            print(f"❌ เพิ่มข้อมูล Booking ไม่สำเร็จ: {e}")
            return False

    # ==========================================
    # หมวดหมู่: Payments
    # ==========================================
    def get_all_payments(self):
        try:
            if not self.payment_sheet:
                return []
            return self.payment_sheet.get_all_values()
        except Exception as e:
            print(f"❌ ดึงข้อมูล Payments ไม่สำเร็จ: {e}")
            return []

    def add_new_payment(self, payment_data):
        try:
            if not self.payment_sheet:
                print("⚠️ Worksheet 'Payment' ไม่พบในฐานข้อมูล")
                return False
            self.payment_sheet.append_row(payment_data)
            return True
        except Exception as e:
            print(f"❌ เพิ่มข้อมูล Payment ไม่สำเร็จ: {e}")
            return False