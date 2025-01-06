# use this to fetch a limited amount
# probably archive

from apify_client import ApifyClient
import os  # Import the os module to access environment variables
from dotenv import load_dotenv  # Import load_dotenv to load environment variables from .env file
import csv  # Import the csv module to handle CSV file operations
import json  # Import the json module to handle JSON file operations

load_dotenv()  # Load environment variables from .env file

# Initialize the ApifyClient with your API token from an environment variable
client = ApifyClient(os.getenv("APIFY_API_TOKEN"))  # Use the environment variable
# Prepare the Actor input
run_input = {
    "user_names": ["jorisfalter"],
    # "user_ids": [1846987139428635000],
    "maxFollowers": 26,
    # "maxFollowings": 100,
    "getFollowers": True,
    "getFollowing": False,
}

# Initialize an empty list to store all items
all_items = []  # This will hold all fetched items

# Fetch items without pagination
run = client.actor("C2Wk3I6xAqC4Xi63f").call(run_input=run_input)  # Call the API once

# Fetch Actor results from the run's dataset
items = client.dataset(run["defaultDatasetId"]).iterate_items()
items_list = list(items)  # Convert the generator to a list

print(f"Received {len(items_list)} items.")  # Log the number of items received

if items_list:  # Check if the list is not empty
    all_items.extend(items_list)  # Add the fetched items to the all_items list
    print(f"Next cursor: '{run.get('nextCursor', '')}'")  # Log the next cursor value
else:
    print("No items to write to CSV.")  # Handle the case where there are no items

# Export results to a CSV file
with open('results.csv', mode='w', newline='') as csv_file:  # Open a CSV file for writing
    if all_items:  # Check if the list is not empty
        # Collect all unique field names from all items
        fieldnames = set()
        for item in all_items:
            fieldnames.update(item.keys())  # Add keys from each item to the set
        fieldnames = list(fieldnames)  # Convert the set back to a list

        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)  # Create a CSV writer object
        writer.writeheader()  # Write the header row
        for item in all_items:  # Iterate through the items
            writer.writerow(item)  # Write each item as a row in the CSV file
    else:
        print("No items to write to CSV.")  # Handle the case where there are no items

# Prepare to collect specific fields into a list
extracted_data = []  # Initialize an empty list to store extracted data

# Iterate through the items and extract specified fields
for item in all_items:  # Iterate through the items
    extracted_item = {
        "Location": item.get("location"),
        "Followers_count": item.get("followers_count"),
        "Url": item.get("url"),
        "Status": item.get("status"),
        "Description": item.get("description"),
        "profile_background_image_url": item.get("profile_background_image_url"),
        "normal_followers_count": item.get("normal_followers_count"),
        "screen_name": item.get("screen_name"),
        "profile_banner_url": item.get("profile_banner_url"),
        "entities": item.get("entities"),
        "profile_image_url_https": item.get("profile_image_url_https"),
        "profile_image_url": item.get("profile_image_url"),
        "pinned_tweet_ids": item.get("pinned_tweet_ids"),
        "name": item.get("name"),
    }
    extracted_data.append(extracted_item)  # Add the extracted item to the list

# Save the extracted data to a JSON file
with open('extracted_data.json', 'w') as json_file:  # Open a JSON file for writing
    json.dump(extracted_data, json_file, indent=4)  # Write the data to the file with indentation

# Extract the top 5 items with the highest followers_count
top_items = sorted(all_items, key=lambda x: x.get("followers_count", 0), reverse=True)[:10]  # Sort and slice the top 5

# Prepare the data for the top items
top_extracted_data = []  # Initialize an empty list for top extracted data
for item in top_items:  # Iterate through the top items
    extracted_item = {
        "Location": item.get("location"),
        "Followers_count": item.get("followers_count"),
        "Url": item.get("url"),
        "Status": item.get("status"),
        "Description": item.get("description"),
        "profile_background_image_url": item.get("profile_background_image_url"),
        "normal_followers_count": item.get("normal_followers_count"),
        "screen_name": item.get("screen_name"),
        "profile_banner_url": item.get("profile_banner_url"),
        "entities": item.get("entities"),
        "profile_image_url_https": item.get("profile_image_url_https"),
        "profile_image_url": item.get("profile_image_url"),
        "pinned_tweet_ids": item.get("pinned_tweet_ids"),
        "name": item.get("name"),
    }
    top_extracted_data.append(extracted_item)  # Add the extracted item to the list

# New code to filter the data for the frontend
frontend_data = []  # Initialize an empty list for frontend data
for item in top_extracted_data:  # Iterate through the top extracted data
    frontend_item = {
        "profile_image_url_https": item["profile_image_url_https"],
        "name": item["name"],
        "followers_count": item["Followers_count"],
        "screen_name": item["screen_name"],
        "location": item["Location"],
        "description": item["Description"],
    }
    frontend_data.append(frontend_item)  # Add the filtered item to the frontend data list

# Now you can send `frontend_data` to the frontend
# For example, you might return it in a web response or API response

# Save the top extracted data to a separate JSON file
with open('top_extracted_data.json', 'w') as top_json_file:  # Open a JSON file for writing
    json.dump(top_extracted_data, top_json_file, indent=4)  # Write the top data to the file with indentation

# Optionally, you can print or save the extracted data
# print(extracted_data)  # Print the extracted data

# New code to save the frontend data to a JSON file
with open('frontend_data.json', 'w') as frontend_json_file:  # Open a JSON file for writing
    json.dump(frontend_data, frontend_json_file, indent=4)  # Write the frontend data to the file with indentation
