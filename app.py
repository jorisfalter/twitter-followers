from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from apify_client import ApifyClient
import os
import json

# Load environment variables
load_dotenv()

# Initialize ApifyClient
client = ApifyClient(os.getenv("APIFY_API_TOKEN"))

# Initialize Flask app
app = Flask(__name__, static_folder='frontend/build')
CORS(app, resources={r"/api/*": {"origins": "*"}})



# Function to fetch follower count from an API - currently mock
def fetch_followers_amount(twitter_handle, mock_result):
    
    ## Old API
    run_input = {"usernames": [twitter_handle]}
    # if not mock_result:
    #     run = client.actor("nD89ddq3SgUPchsIO").call(run_input=run_input)

    #     # Fetch results from the dataset
    #     result_data = {}
    #     for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    #         result_data = item

    # elif mock_result:
    #     result_data = {"sub_count":"333"}

    # new API

    # Prepare the Actor input
    run_input = {
    "user_names": [twitter_handle],
    }
    # Run the Actor and wait for it to finish
    run = client.actor("tLs1g71YVTPoXAPnb").call(run_input=run_input)

    # Get only the first item from the dataset
    result_data = next(client.dataset(run["defaultDatasetId"]).iterate_items(), None)
    if result_data is None:
        result_data = {}  # Fallback if no items are found

    return {
        "handle": twitter_handle,
        "sub_count": result_data.get("relationship_counts", {}).get("followers", 0)
    }

def fetch_followers_list(twitter_handle, preview_run, limitOn):
    
    if limitOn is True:
        maxFollowers = 200;
        print("limit is on")
    elif limitOn is False:
        maxFollowers = 8000; # change this when in production!
        print("limit is off")


    if preview_run is True:
        maxFollowers = 200;

    print(maxFollowers)

    run_input = {
        "user_names": [twitter_handle],
        # "user_ids": [1846987139428635000],
        "maxFollowers": maxFollowers,
        "maxFollowings": 200, # has to be on apparently 
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
        print("No items")  # Handle the case where there are no items

    # print(all_items)

    # # Export results to a CSV file
    # with open('results.csv', mode='w', newline='') as csv_file:  # Open a CSV file for writing
    #     if all_items:  # Check if the list is not empty
    #         # Collect all unique field names from all items
    #         fieldnames = set()
    #         for item in all_items:
    #             fieldnames.update(item.keys())  # Add keys from each item to the set
    #         fieldnames = list(fieldnames)  # Convert the set back to a list

    #         writer = csv.DictWriter(csv_file, fieldnames=fieldnames)  # Create a CSV writer object
    #         writer.writeheader()  # Write the header row
    #         for item in all_items:  # Iterate through the items
    #             writer.writerow(item)  # Write each item as a row in the CSV file
    #     else:
    #         print("No items to write to CSV.")  # Handle the case where there are no items

    # # Prepare to collect specific fields into a list
    # extracted_data = []  # Initialize an empty list to store extracted data

    # # Iterate through the items and extract specified fields
    # for item in all_items:  # Iterate through the items
    #     extracted_item = {
    #         "Location": item.get("location"),
    #         "Followers_count": item.get("followers_count"),
    #         "Url": item.get("url"),
    #         "Status": item.get("status"),
    #         "Description": item.get("description"),
    #         "profile_background_image_url": item.get("profile_background_image_url"),
    #         "normal_followers_count": item.get("normal_followers_count"),
    #         "screen_name": item.get("screen_name"),
    #         "profile_banner_url": item.get("profile_banner_url"),
    #         "entities": item.get("entities"),
    #         "profile_image_url_https": item.get("profile_image_url_https"),
    #         "profile_image_url": item.get("profile_image_url"),
    #         "pinned_tweet_ids": item.get("pinned_tweet_ids"),
    #         "name": item.get("name"),
    #     }
    #     extracted_data.append(extracted_item)  # Add the extracted item to the list

    # # Save the extracted data to a JSON file
    # with open('extracted_data.json', 'w') as json_file:  # Open a JSON file for writing
    #     json.dump(extracted_data, json_file, indent=4)  # Write the data to the file with indentation

    # Sort to the highest followers_count
    top_items = sorted(all_items, key=lambda x: x.get("followers_count", 0), reverse=True)  # Sort
    print(f"Number of items after sorting: {len(top_items)}")  # Add this line to see array size


    # New code to filter the data for the frontend
    frontend_data = []
    for item in top_items:
        # Get the full status time
        full_status_time = item.get("status", {}).get("created_at")
        # Format the date if it exists, otherwise keep it as None
        formatted_date = None
        if full_status_time:
            try:
                # Split the string and take only the date part (Twitter dates typically come as "Dow MMM DD HH:MM:SS +0000 YYYY")
                date_parts = full_status_time.split()
                formatted_date = f"{date_parts[1]} {date_parts[2]} {date_parts[5]}"  # Month Day Year
            except:
                formatted_date = full_status_time  # Fallback to original if parsing fails

        frontend_item = {
            "profile_image_url_https": item["profile_image_url_https"],
            "name": item["name"],
            "followers_count": item["followers_count"],
            "screen_name": item["screen_name"],
            "location": item["location"],
            "description": item["description"],
            "statusTime": formatted_date,
            "statusText": item.get("status", {}).get("text")
        }
        frontend_data.append(frontend_item)

    return(frontend_data)


############################################################################

# API endpoint to fetch the amount of followers
@app.route('/api/fetch_followers', methods=['GET'])
def fetch_nr_of_followers():
    twitter_handle = request.args.get('handle')
    if not twitter_handle:
        return jsonify({"error": "Twitter handle is required"}), 400

    isMock = True;

    try:
        result = fetch_followers_amount(twitter_handle, isMock)
        return jsonify(result)
    except Exception as e:
        app.logger.error(f"Error fetching followers: {e}")
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500

# # API endpoint to fetch preloaded follower data
# with open('frontend_data.json', 'r') as json_file:
#     frontend_data = json.load(json_file)

# Get list of followers limited to 25 > not sure if this is technically possible!
@app.route('/api/followers', methods=['GET'])
def get_followers_preview():
    twitter_handle = request.args.get('handle')
  
    if not twitter_handle:
        print("no twitter handle here")
        return jsonify({"error": "Twitter handle is required"}), 400

    previewRun = True;
    limitOn = True; # shouldn't matter when setting preview run


    try:
        result = fetch_followers_list(twitter_handle, previewRun, limitOn)
        return jsonify(result)
    except Exception as e:
        app.logger.error(f"Error fetching followers: {e}")
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500

# Get full list of followers - 
@app.route('/api/followersFull', methods=['GET'])
def get_followers_full():
    twitter_handle = request.args.get('handle')
    if not twitter_handle:
        return jsonify({"error": "Twitter handle is required"}), 400

    previewRun = False;
    # limiting to 26 for now to test if this limit actually works
    limitOn = False; # Prevent High Costs, keep this on as long as we're testing!

    try:
        result = fetch_followers_list(twitter_handle, previewRun, limitOn)
        return jsonify(result)
    except Exception as e:
        app.logger.error(f"Error fetching followers: {e}")
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500
# Serve React frontend
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    if path and os.path.exists(f'frontend/build/{path}'):
        return send_from_directory('frontend/build', path)
    else:
        return send_from_directory('frontend/build', 'index.html')

if __name__ == '__main__':
    # app.run(debug=True)
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)