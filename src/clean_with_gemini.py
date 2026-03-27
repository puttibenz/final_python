import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
import time

load_dotenv()

# ตั้งค่า Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel('gemini-2.0-flash')

def clean_raw_data_with_ai(raw_data=None, input_file='apify_raw_data.json', output_file='final_camps_cleaned.json', save_to_file=True):
    # หากไม่ได้ส่ง raw_data มา ให้ลองอ่านจากไฟล์
    if raw_data is None:
        if not os.path.exists(input_file):
            print(f"❌ ไม่พบไฟล์ {input_file}")
            return []
        
        print(f"📖 กำลังอ่าน Raw Data จาก {input_file}...")
        with open(input_file, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)

    if not raw_data:
        print("⚠️ ไม่มีข้อมูลให้ประมวลผล")
        return []

    print(f"🧠 กำลังใช้ AI สกัดและคลีนข้อมูล {len(raw_data)} รายการ...")

    # ประหยัด Quota: ส่งรอบละ 10-15 รายการ + พัก 5 วินาที
    batch_size = 15
    cleaned_results = []

    prompt_instructions = """
    คุณเป็น Data Engineer ที่เชี่ยวชาญการทำความสะอาดข้อมูล (Data Cleaning)
    หน้าที่: สกัดข้อมูลแคมป์ปิ้งจากก้อนข้อมูลดิบ (Raw Data) ของ Facebook และแปลงเป็น JSON ที่สมบูรณ์
    
    โครงสร้างที่ต้องการ:
    - name: (string) ชื่อทริปที่น่าสนใจ
    - location: (string) ชื่อจังหวัดในไทย (เช่น 'เชียงใหม่')
    - start_date: (string) วันที่เริ่มทริป รูปแบบ YYYY-MM-DD (เช่น '2026-04-08') ถ้าข้อมูลเดิมเป็น '8 เมษา' ให้คำนวณเป็นปี 2026
    - duration: (int) จำนวนวันของทริป (ถ้าเจอ '2 วัน 1 คืน' ให้เป็น 2)
    - price: (int) ราคาตัวเลขเท่านั้น (ตัดเครื่องหมาย ฿ หรือคอมม่าออก)
    - slots: (int) จำนวนที่รับสมัครทั้งหมด (ถ้าไม่มีให้เดาจากบริบทหรือใส่ 20)
    - available_slots: (int) เท่ากับ slots
    - facebook_link: (string) ลิงก์โพสต์ Facebook เดิม
    - image_url: (string) URL รูปภาพหลักของโพสต์
    - description: (string) สรุปรายละเอียดสั้นๆ ไม่เกิน 100 ตัวอักษร
    - contact: (string) เบอร์โทรหรือ LINE ID ที่ระบุในโพสต์

    กฎเหล็ก:
    1. ถ้าข้อมูลไหนไม่มี/เดาไม่ได้ ให้ใส่ null
    2. ส่งกลับมาเป็น JSON Array ของ Object เท่านั้น ห้ามเขียนคำบรรยายอื่น
    3. ข้อมูลดิบที่จะให้ประมวลผลมีดังนี้:
    """

    for i in range(0, len(raw_data), batch_size):
        chunk = raw_data[i:i+batch_size]
        print(f"⏳ กำลังประมวลผลรายการที่ {i+1} ถึง {min(i+batch_size, len(raw_data))}...")
        
        try:
            # ส่งข้อมูลไปประมวลผล
            full_prompt = prompt_instructions + json.dumps(chunk, ensure_ascii=False)
            response = model.generate_content(full_prompt)
            
            # สกัดเฉพาะเนื้อหา JSON
            raw_text = response.text.strip()
            if "```json" in raw_text:
                raw_text = raw_text.split("```json")[1].split("```")[0].strip()
            elif "```" in raw_text:
                # Handle cases where it's just ``` without 'json'
                raw_text = raw_text.split("```")[1].split("```")[0].strip()
            
            cleaned_batch = json.loads(raw_text)
            cleaned_results.extend(cleaned_batch)
            
            # 💤 พัก 5 วินาทีเพื่อรักษาสุขภาพ API Quota
            print(f"✅ บันทึกแล้ว {len(cleaned_results)} รายการ... พัก 5 วินาที...")
            time.sleep(5)
            
        except Exception as e:
            print(f"⚠️ เกิดข้อผิดพลาดในรอบนี้: {e}")

    # บันทึกเป็นไฟล์ใหม่ที่คลีนแล้ว (ถ้าต้องการ)
    if save_to_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(cleaned_results, f, ensure_ascii=False, indent=2)
        print(f"\n✨ เสร็จสมบูรณ์! ข้อมูลถูกคลีนและบันทึกไว้ที่ {output_file}")
    
    return cleaned_results

if __name__ == "__main__":
    clean_raw_data_with_ai()
