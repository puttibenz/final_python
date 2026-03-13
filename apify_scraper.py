import os
from dotenv import load_dotenv
from apify_client import ApifyClient

load_dotenv()

client = ApifyClient(os.getenv('APIFY_API_KEY'))

# Setting Input for the Actor
run_input = {
    'startUrls': [
        {'url': 'https://www.facebook.com/groups/2334603449889400/'}
    ],
    'maxPosts': 50,
    'viewOption':'CHRONOLOGICAL',
}

# Run the Actor and wait for it to finish
print("🚀 Starting the Apify Actor...")
run = client.actor('apify/facebook-groups-scraper').call(run_input=run_input)

dataset_items = client.dataset(run['defaultDatasetId']).list_items().items

print(f"✅ Finished scraping! Total posts scraped: {len(dataset_items)}")

# Example 
for post in dataset_items[:5]:  # Print first 5 posts
    print(f'Post ID: {post["id"]}')
    print(f'Content: {post.get("text","No Text"[:100])}...')
    print(f'Likes: {post.get("likes")}')
    print('-'*30)