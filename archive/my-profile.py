import requests

BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAFS5nQEAAAAAfQ9uEuikJGe4cOYVH4SW2zN31%2B8%3DAOQzdSTefe0ZzOAw3g3xfo6hgO9wnmGsOiqCdvDZYQJoxaN4ny'

# Function to create headers for API v2 requests
def create_headers(bearer_token):
    headers = {"Authorization": f"Bearer {bearer_token}"}
    return headers

# Function to get user ID based on username
def get_user_id(username):
    url = f"https://api.twitter.com/2/users/by/username/{username}"
    headers = create_headers(BEARER_TOKEN)
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        user_data = response.json()
        return user_data['data']['id']
    else:
        raise Exception(f"Error fetching user ID: {response.status_code}, {response.text}")

# Function to get followers of a user by user ID
def get_followers(user_id):
    url = f"https://api.twitter.com/2/users/{user_id}/"
    headers = create_headers(BEARER_TOKEN)
    params = {
        "max_results": 100,  # Max is 100 followers per request
        "user.fields": "public_metrics"  # This will include follower counts in the response
    }
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching followers: {response.status_code}, {response.text}")

# Main execution
try:
    # Replace with your Twitter username
    username = "jorisfalter"
    
    # Get the user ID for the given username
    user_id = get_user_id(username)
    print(f"User ID for {username}: {user_id}")
    
    # Get followers and their follower counts
    followers_data = get_followers(user_id)
    for follower in followers_data['data']:
        screen_name = follower['username']
        name = follower['name']
        followers_count = follower['public_metrics']['followers_count']
        print(f"Name: {name} | Handle: {screen_name} | Followers: {followers_count}")
        
except Exception as e:
    print(e)