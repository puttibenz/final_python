import json
import os
import sys

# Ensure we can import from the project root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.crud import camp_repo

def seed_database():
    """Reads scraped camp data from JSON and inserts it into Supabase."""
    file_path = 'clean_camps_ready_for_sql.json'
    
    # รายการคอลัมน์ที่อนุญาตตามรูปภาพใน Supabase (White-list)
    ALLOWED_COLUMNS = [
        'name', 'location', 'start_date', 'duration', 'price', 
        'slots', 'available_slots', 'image_url', 'description', 
        'contact', 'status', 'created_by', 'facebook_link'
    ]

    if not os.path.exists(file_path):
        print(f"❌ Error: {file_path} not found.")
        return

    print(f"📖 Reading data from {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        camps_data = json.load(f)

    print(f"🚀 Found {len(camps_data)} camps. Cleaning and inserting...")

    success_count = 0
    error_count = 0

    for camp in camps_data:
        # 1. จัดการเรื่องชื่อฟิลด์ที่ไม่ตรงกัน (Mapping)
        if 'image' in camp and 'image_url' not in camp:
            camp['image_url'] = camp['image']
        
        if 'slots' in camp and 'available_slots' not in camp:
            camp['available_slots'] = camp['slots']

        # 2. กรองข้อมูล: เก็บไว้เฉพาะคอลัมน์ที่มีอยู่ในตาราง Supabase จริงๆ
        clean_data = {k: v for k, v in camp.items() if k in ALLOWED_COLUMNS}

        # 3. จัดการ Data Type เบื้องต้น
        if 'price' in clean_data and clean_data['price'] is not None:
            try:
                # แปลงราคาเป็นตัวเลข (ลบคอมม่าหรือสัญลักษณ์เงินถ้ามี)
                p = str(clean_data['price']).replace(',', '').replace('฿', '').strip()
                clean_data['price'] = int(float(p))
            except:
                clean_data['price'] = 0

        if not clean_data.get('name'):
            continue

        try:
            result = camp_repo.create(clean_data)
            if result:
                success_count += 1
                if success_count % 5 == 0:
                    print(f"✅ [{success_count}/{len(camps_data)}] Inserted: {clean_data['name'][:30]}...")
            else:
                error_count += 1
        except Exception as e:
            print(f"❌ Error for '{clean_data.get('name')}': {e}")
            error_count += 1

    print("\n" + "="*30)
    print("📊 SEEDING COMPLETE")
    print(f"✅ Success: {success_count}")
    print(f"❌ Failed:  {error_count}")
    print("="*30)

if __name__ == "__main__":
    # Check if --yes or -y is passed to skip confirmation
    force = False
    if len(sys.argv) > 1 and sys.argv[1] in ['--yes', '-y']:
        force = True

    if force:
        seed_database()
    else:
        confirm = input("⚠️ Start seeding data into Supabase? (yes/no): ")
        if confirm.lower() == 'yes':
            seed_database()
        else:
            print("Cancelled.")
