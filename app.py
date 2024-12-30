from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

import os
import json

app = Flask(__name__, static_folder='frontend/build')
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})


# API endpoint
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
