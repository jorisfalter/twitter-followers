from apify_client import ApifyClient
import os  # Import the os module to access environment variables
from dotenv import load_dotenv  # Import load_dotenv to load environment variables from .env file
import csv  # Import the csv module to handle CSV file operations

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