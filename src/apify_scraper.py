import os
import json
from dotenv import load_dotenv
from apify_client import ApifyClient

load_dotenv()

class FacebookScraper:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('APIFY_API_KEY')
        self.client = ApifyClient(self.api_key)
        self.dataset_items = []

    def scrape_group(self, group_url, limit=50):
        """Runs the Apify actor to scrape a Facebook group."""
        run_input = {
            "resultsLimit": limit,
            "startUrls": [{"url": group_url}],
            "viewOption": "CHRONOLOGICAL"
        }

        print(f"🚀 Starting the Apify Actor for: {group_url}...")
        try:
            run = self.client.actor('apify/facebook-groups-scraper').call(run_input=run_input)
            self.dataset_items = self.client.dataset(run['defaultDatasetId']).list_items().items
            print(f"✅ Finished scraping! Total posts scraped: {len(self.dataset_items)}")
            return self.dataset_items
        except Exception as e:
            print(f"❌ Error during scraping: {e}")
            return []

    def save_to_json(self, filename='apify_raw_data_latest.json'):
        """Saves the scraped data to a JSON file."""
        if not self.dataset_items:
            print("⚠️ No data to save.")
            return

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.dataset_items, f, ensure_ascii=False, indent=2)
        print(f"💾 Data saved to {filename}")

    def preview_data(self, count=5):
        """Prints a preview of the scraped posts."""
        for post in self.dataset_items[:count]:
            print(f'Post ID: {post.get("id")}')
            print(f'Content: {post.get("text", "No Text")[:100]}...')
            print(f'Likes: {post.get("likes")}')
            print('-' * 30)

if __name__ == "__main__":
    scraper = FacebookScraper()
    group_url = "https://www.facebook.com/groups/2334603449889400/"
    scraper.scrape_group(group_url, limit=50)
    scraper.save_to_json()
    scraper.preview_data()
