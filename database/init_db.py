# database/init_db.py
from .models import TableHeaders

def _ensure_header(sheet, expected_headers, sheet_name, end_col_letter):
    """Helper function สำหรับเช็กและสร้างหัวตาราง"""
    try:
        current = sheet.row_values(1)
        if current != expected_headers:
            range_name = f"A1:{end_col_letter}1"
            sheet.update(range_name=range_name, values=[expected_headers])
            print(f"🛠️ สร้าง/ซ่อมแซมหัวตาราง {sheet_name} สำเร็จ!")
    except Exception as e:
        print(f"⚠️ ไม่สามารถตรวจสอบหัวตาราง {sheet_name} ได้: {e}")

def init_database(sh):
    """ฟังก์ชันหลักที่ใช้เช็กหัวตารางทั้งหมด"""
    try:
        camp_sheet = sh.worksheet("Camp")
        users_sheet = sh.worksheet("Users")
        booking_sheet = sh.worksheet("Booking")
        
        _ensure_header(camp_sheet, TableHeaders.CAMP, "Camp", "I")
        _ensure_header(users_sheet, TableHeaders.USERS, "Users", "E")
        _ensure_header(booking_sheet, TableHeaders.BOOKING, "Bookings", "G")

        try:
            payment_sheet = sh.worksheet("Payments")
            _ensure_header(payment_sheet, TableHeaders.PAYMENTS, "Payments", "F")
        except Exception:
            print("⚠️ ไม่พบ Worksheet 'Payments' จะข้ามการเช็กหัวตารางไป")
            
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาดในการ Init Database: {e}")