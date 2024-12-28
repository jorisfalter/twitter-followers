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
    # "maxFollowers": 100,
    # "maxFollowings": 100,
    "getFollowers": True,
    "getFollowing": False,
}

# Run the Actor and wait for it to finish
run = client.actor("C2Wk3I6xAqC4Xi63f").call(run_input=run_input)

# Fetch Actor results from the run's dataset (if there are any)
items = client.dataset(run["defaultDatasetId"]).iterate_items()

# Export results to a CSV file
with open('results.csv', mode='w', newline='') as csv_file:  # Open a CSV file for writing
    items_list = list(items)  # Convert the generator to a list
    if items_list:  # Check if the list is not empty
        # Collect all unique field names from all items
        fieldnames = set()
        for item in items_list:
            fieldnames.update(item.keys())  # Add keys from each item to the set
        fieldnames = list(fieldnames)  # Convert the set back to a list

        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)  # Create a CSV writer object
        writer.writeheader()  # Write the header row
        for item in items_list:  # Iterate through the items
            writer.writerow(item)  # Write each item as a row in the CSV file
    else:
        print("No items to write to CSV.")  # Handle the case where there are no items

# Prepare to collect specific fields into a list
extracted_data = []  # Initialize an empty list to store extracted data

# Iterate through the items and extract specified fields
for item in items_list:  # Iterate through the items
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

# Optionally, you can print or save the extracted data
# print(extracted_data)  # Print the extracted data