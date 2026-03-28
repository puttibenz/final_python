import json
import os
import sys

# เพิ่ม root directory เข้า sys.path เพื่อให้ import database.crud ได้
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.crud import user_repo, camp_repo
from database.connection import get_connection

def insert_data():
    # 1. สร้าง User "Facebook Scraper" ถ้ายังไม่มี
    scraper_username = "facebook_scraper"
    scraper_email = "scraper@facebook.com"
    
    # เช็คว่ามีอยู่แล้วหรือยัง
    existing_user = user_repo.get_user_by_email(scraper_email)
    if existing_user:
        scraper_id = existing_user['id']
        print(f"✅ พบ User Scraper เดิม (ID: {scraper_id})")
    else:
        scraper_id = user_repo.create_user(
            username=scraper_username,
            email=scraper_email,
            password_hash="scraped_data_no_password",
            full_name="Facebook Scraper",
            phone="000-000-0000"
        )
        if scraper_id:
            # Update role to admin so it can be managed easily
            user_repo.update_user(scraper_id, role='admin')
            print(f"✨ สร้าง User Scraper ใหม่สำเร็จ (ID: {scraper_id})")
        else:
            print("❌ ไม่สามารถสร้าง User Scraper ได้")
            return

    # 2. อ่านข้อมูลจาก final_clean_camps.json
    input_file = 'final_clean_camps.json'
    if not os.path.exists(input_file):
        print(f"❌ ไม่พบไฟล์ {input_file}")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        camps = json.load(f)

    print(f"🚀 กำลังนำเข้าข้อมูล {len(camps)} รายการ...")

    success_count = 0
    duplicate_count = 0

    for camp in camps:
        # เช็คว่ามี link นี้ใน DB หรือยัง (กันซ้ำ)
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM camps WHERE facebook_link = %s", (camp.get('facebook_link'),))
                if cur.fetchone():
                    duplicate_count += 1
                    continue
        finally:
            conn.close()

        # เตรียมข้อมูล
        # ลบคีย์ที่ไม่ใช่คอลัมน์ใน DB (ถ้ามี)
        allowed_cols = {
            'name', 'location', 'start_date', 'duration', 'price', 
            'slots', 'available_slots', 'image_url', 'description', 
            'contact', 'facebook_link', 'status', 'created_by'
        }
        db_data = {k: v for k, v in camp.items() if k in allowed_cols}
        
        db_data['created_by'] = scraper_id
        if 'status' not in db_data:
            db_data['status'] = 'active'
        if 'available_slots' not in db_data and 'slots' in db_data:
            db_data['available_slots'] = db_data['slots']
            
        # Insert
        res = camp_repo.create(db_data)
        if res:
            success_count += 1
        else:
            print(f"⚠️ ไม่สามารถนำเข้า: {camp.get('name')}")

    print(f"\n📊 สรุปการนำเข้า:")
    print(f"✅ นำเข้าสำเร็จ: {success_count} รายการ")
    print(f"🔁 ซ้ำ (มีใน DB แล้ว): {duplicate_count} รายการ")
    print(f"❌ ผิดพลาด: {len(camps) - success_count - duplicate_count} รายการ")

if __name__ == "__main__":
    insert_data()
