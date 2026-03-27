import os
import sys
from dotenv import load_dotenv

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.apify_scraper import FacebookScraper
from src.clean_with_gemini import clean_raw_data_with_ai

load_dotenv()

def run_pipeline(group_url, limit=50):
    """
    Orchestrates the scraper -> cleaner pipeline.
    Saves results to JSON for seed_data.py to pick up.
    """
    output_file = 'clean_camps_ready_for_sql.json'
    print(f"--- 🚀 Starting Pipeline for {group_url} ---")
    
    # 1. Scrape
    scraper = FacebookScraper()
    raw_data = scraper.scrape_group(group_url, limit=limit)
    
    if not raw_data:
        print("❌ Scraper returned no data. Pipeline aborted.")
        return
    
    # Optional: Save raw data for backup
    scraper.save_to_json('apify_raw_data_latest.json')
    
    # 2. Clean with Gemini
    print("\n--- 🧠 Cleaning data with Gemini ---")
    # We pass output_file to match what seed_data.py expects
    cleaned_data = clean_raw_data_with_ai(
        raw_data=raw_data, 
        output_file=output_file, 
        save_to_file=True
    )
    
    if not cleaned_data:
        print("❌ Cleaning returned no data. Pipeline aborted.")
        return
    
    print(f"\n--- ✨ Pipeline Finished ---")
    print(f"✅ Cleaned {len(cleaned_data)} items and saved to: {output_file}")
    print(f"👉 Now run: python database/seed_data.py to insert into Database.")

if __name__ == "__main__":
    # Example URL (can be passed via command line or modified here)
    target_group = "https://www.facebook.com/groups/2334603449889400/"
    
    # Allow URL from command line argument
    if len(sys.argv) > 1:
        target_group = sys.argv[1]
        
    limit = 50 # Default to 50 for testing to save credits/tokens
    if len(sys.argv) > 2:
        limit = int(sys.argv[2])
        
    run_pipeline(target_group, limit=limit)
