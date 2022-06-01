from apify_client import ApifyClient
import os
import json

# Initialize the ApifyClient with your API token
API = os.environ['API_KEY']
client = ApifyClient(API)

# Prepare the actor input
run_input = {
    "searchTerms": ["nepal"],
    "searchMode": "",
    "mode": "own",
    "tweetsDesired": 2,
    "proxyConfig": { "useApifyProxy": True },
    "extendOutputFunction": """async ({ data, item, page, request, customData, Apify }) => {
  return item;
}""",
    "extendScraperFunction": """async ({ page, request, addSearch, addProfile, _, addThread, addEvent, customData, Apify, signal, label }) => {
 
}""",
    "customData": {},
    "handlePageTimeoutSecs": 5000,
    "maxRequestRetries": 3,
    "maxIdleTimeoutSecs": 30,
    "initialCookies": [],
}

# Run the actor and wait for it to finish
run = client.actor("vdrmota/twitter-scraper").call(run_input=run_input)

# Fetch and print actor results from the run's dataset (if there are any)
result = []
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    result.append(item)
    

with open("result.json","w+") as f:
	json.dump(result,f)
