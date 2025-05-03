import os
import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, request

load_dotenv()

app = Flask(__name__)

cookie = os.getenv('ROBLOX_COOKIE')

# Set up the headers for the request
headers = {
    "Cookie": cookie,  # This is the authentication cookie
    "User-Agent": "Roblox/WinInet",  # Standard User-Agent for Roblox requests
    "X-CSRF-Token": "",  # Optional CSRF token for some requests (not needed for GET requests)
}

@app.route("/<int:user_id>/followings", methods=["GET"])
def get_followings(user_id):
    # Get query parameters, with defaults if not provided
    limit = request.args.get('limit', default=100, type=int)  # Default to 100 if not provided
    cursor = request.args.get('cursor', default=None, type=str)  # Default to None if not provided
    
    # Build the URL with the query parameters
    url = f"https://friends.roblox.com/v1/users/{user_id}/followings?limit={limit}"
    if cursor:
        url += f"&cursor={cursor}"

    # Send a GET request to the Roblox API
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # If successful, return the JSON response to the client
        return jsonify(response.json())
    else:
        # If the request failed, return an error message
        return jsonify({"error": f"Failed to fetch followings for user {user_id}: {response.status_code}"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
