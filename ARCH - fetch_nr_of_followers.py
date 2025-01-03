# ARCHIVE

from flask import Flask, jsonify, request
from flask_cors import CORS
import os  # Import the os module to access environment variables
from apify_client import ApifyClient
from dotenv import load_dotenv  # Import load_dotenv to load environment variables from .env file
import json  # Import the json module to handle JSON file operations

load_dotenv()  # Load environment variables from .env file
# Initialize the ApifyClient with your API token from an environment variable
client = ApifyClient(os.getenv("APIFY_API_TOKEN"))  # Use the environment variable

app = Flask(__name__)
CORS(app)

# Mock function to fetch follower count from an API
def fetch_followers_from_api(twitter_handle):

    run_input = { "usernames": [twitter_handle] }
    # Run the Actor and wait for it to finish
    run = client.actor("nD89ddq3SgUPchsIO").call(run_input=run_input)
    # Fetch and print Actor results from the run's dataset (if there are any)
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        print(item)
        result_data = item
    return {
        "handle": twitter_handle,
        "sub_count": result_data["sub_count"]
    }

@app.route('/api/fetch_followers', methods=['GET'])
def fetch_nr_of_followers():
    twitter_handle = request.args.get('handle')
    # twitter_handle = "jorisfalter"
    # twitter_handle = "elonmusk"

    if not twitter_handle:
        return jsonify({"error": "Twitter handle is required"}), 400

    try:
        # Fetch follower count from the API
        result = fetch_followers_from_api(twitter_handle)
        print("printing from route")
        print(result)
        return jsonify(result)
    except Exception as e:
        # Log the error and return a JSON error response
        app.logger.error(f"Error fetching followers: {e}")
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 50

if __name__ == '__main__':
    app.run(debug=True)










