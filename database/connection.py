import os
import gspread
from dotenv import load_dotenv
from pathlib import Path

# หาที่อยู่ของโฟลเดอร์หลักอัตโนมัติ และชี้ไปที่ไฟล์ .env
BASE_DIR = Path(__file__).resolve().parent.parent
env_path = os.path.join(BASE_DIR, '.env')

# โหลดไฟล์ .env จาก Path ที่กำหนดอย่างเจาะจง
load_dotenv(dotenv_path=env_path)

def get_db_connection():
    cred_path = os.getenv("GOOGLE_CRED_PATH")
    if not cred_path:
        raise ValueError("❌ ไม่พบ GOOGLE_CRED_PATH ในไฟล์ .env")

    try:
        gc = gspread.service_account(filename=cred_path)
        sh = gc.open("Database_camp")
        print("✅ เชื่อมต่อ Google Sheets สำเร็จ!")
        return sh
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาดในการเชื่อมต่อ: {e}")
        raise