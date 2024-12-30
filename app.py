from flask import Flask, jsonify
import json

app = Flask(__name__)

# Load the data from the JSON file
with open('frontend_data.json', 'r') as json_file:
    frontend_data = json.load(json_file)

@app.route('/api/followers', methods=['GET'])
def get_followers():
    return jsonify(frontend_data)  # Serve the data as JSON

if __name__ == '__main__':
    app.run(debug=True)
