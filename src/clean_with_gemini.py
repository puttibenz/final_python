import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
import time

load_dotenv()

# ตั้งค่า Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel('models/gemini-2.5-flash')


def clean_raw_data_with_ai(raw_data=None, input_file='apify_raw_data_latest.json', output_file='clean_camps_ready_for_sql.json', save_to_file=True):
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

    # Load existing results to skip duplicates
    existing_links = set()
    if os.path.exists(output_file):
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
                existing_links = {item.get('facebook_link') for item in existing_data if item.get('facebook_link')}
                cleaned_results = existing_data
                print(f"✅ โหลดข้อมูลเดิม {len(cleaned_results)} รายการ (มี {len(existing_links)} ลิงก์ที่ไม่ซ้ำ)")
        except:
            cleaned_results = []
    else:
        cleaned_results = []

    # ประหยัด Quota: ส่งรอบละ 5 รายการ + พัก 10 วินาที
    batch_size = 5

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
        
        # กรองเอาเฉพาะรายการที่ยังไม่เคยทำ (เช็คจาก URL)
        filtered_chunk = []
        for item in chunk:
            url = item.get('url')
            if url not in existing_links:
                filtered_chunk.append(item)
        
        if not filtered_chunk:
            continue

        # Simplify chunk to save tokens and improve quality
        simplified_chunk = []
        for item in filtered_chunk:
            image_url = None
            if 'attachments' in item and item['attachments']:
                for att in item['attachments']:
                    if 'image' in att and 'uri' in att['image']:
                        image_url = att['image']['uri']
                        break
                    elif 'thumbnail' in att:
                        image_url = att['thumbnail']
                        break
            
            simplified_chunk.append({
                "text": item.get("text", ""),
                "url": item.get("url", ""),
                "image_url": image_url
            })

        print(f"⏳ กำลังประมวลผลรายการที่ {i+1} ถึง {min(i+batch_size, len(raw_data))}... (ข้ามที่ซ้ำแล้ว)")
        
        max_retries = 5
        for attempt in range(max_retries):
            try:
                # ส่งข้อมูลที่ย่อแล้วไปประมวลผล
                full_prompt = prompt_instructions + json.dumps(simplified_chunk, ensure_ascii=False)
                response = model.generate_content(full_prompt)
                
                # สกัดเฉพาะเนื้อหา JSON
                raw_text = response.text.strip()
                if "```json" in raw_text:
                    raw_text = raw_text.split("```json")[1].split("```")[0].strip()
                elif "```" in raw_text:
                    raw_text = raw_text.split("```")[1].split("```")[0].strip()
                
                cleaned_batch = json.loads(raw_text)
                
                # ป้องกันเบิ้ลในรอบเดียวกัน (เช็คทั้ง URL และข้อมูลทริป)
                for item in cleaned_batch:
                    link = item.get('facebook_link')
                    trip_key = f"{item.get('name')}|{item.get('location')}|{item.get('start_date')}"
                    
                    if link and link not in existing_links:
                        # เช็คว่ามีทริปชื่อนี้ วันนี้ จังหวัดนี้อยู่แล้วหรือยัง
                        is_duplicate_trip = any(
                            f"{res.get('name')}|{res.get('location')}|{res.get('start_date')}" == trip_key 
                            for res in cleaned_results
                        )
                        
                        if not is_duplicate_trip:
                            cleaned_results.append(item)
                            existing_links.add(link)

                print(f"✅ บันทึกรวมแล้ว {len(cleaned_results)} รายการ (ไม่ซ้ำทริป)... พัก 10 วินาที...")
                
                # บันทึกทุกครั้งที่จบ batch กันพลาด
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(cleaned_results, f, ensure_ascii=False, indent=2)
                
                time.sleep(10)
                break  # สำเร็จแล้ว ออกจาก retry loop
                
            except Exception as e:
                error_msg = str(e)
                if "429" in error_msg or "Resource has been exhausted" in error_msg:
                    wait_time = 30 * (2 ** attempt)  # 30s, 60s, 120s, 240s, 480s
                    print(f"⏳ ถูก Rate Limit (429) — รอ {wait_time} วินาทีแล้วลองใหม่ (ครั้งที่ {attempt+1}/{max_retries})...")
                    time.sleep(wait_time)
                else:
                    print(f"⚠️ เกิดข้อผิดพลาดในรอบนี้: {e}")
                    break  # error อื่นไม่ต้อง retry

    # บันทึกเป็นไฟล์ใหม่ที่คลีนแล้ว (ถ้าต้องการ)
    if save_to_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(cleaned_results, f, ensure_ascii=False, indent=2)
        print(f"\n✨ เสร็จสมบูรณ์! ข้อมูลถูกคลีนและบันทึกไว้ที่ {output_file}")
    
    return cleaned_results

if __name__ == "__main__":
    clean_raw_data_with_ai()
