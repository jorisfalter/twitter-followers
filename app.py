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
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

# Mock function to fetch follower count from an API
def fetch_followers_from_api(twitter_handle):
    run_input = {"usernames": [twitter_handle]}
    run = client.actor("nD89ddq3SgUPchsIO").call(run_input=run_input)

    # Fetch results from the dataset
    result_data = {}
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        result_data = item
    return {
        "handle": twitter_handle,
        "sub_count": result_data.get("sub_count", 0)  # Safely access sub_count
    }

# API endpoint to fetch followers from an external API
@app.route('/api/fetch_followers', methods=['GET'])
def fetch_nr_of_followers():
    twitter_handle = request.args.get('handle')
    if not twitter_handle:
        return jsonify({"error": "Twitter handle is required"}), 400

    try:
        result = fetch_followers_from_api(twitter_handle)
        return jsonify(result)
    except Exception as e:
        app.logger.error(f"Error fetching followers: {e}")
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500

# API endpoint to fetch preloaded follower data
with open('frontend_data.json', 'r') as json_file:
    frontend_data = json.load(json_file)

@app.route('/api/followers', methods=['GET'])
def get_followers():
    return jsonify(frontend_data)

# Serve React frontend
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    if path and os.path.exists(f'frontend/build/{path}'):
        return send_from_directory('frontend/build', path)
    else:
        return send_from_directory('frontend/build', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
