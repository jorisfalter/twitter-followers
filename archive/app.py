import tweepy
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse
import os

# Disable HTTPS requirement for local development
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Twitter API keys (ensure these are correct)
client_id = 'amRoZ2N3Z1A5VnVfenNjcGdjMFA6MTpjaQ'
client_secret = '-eI07LGBfUhvV-ayWRNKOJ8n0P5QDBBnAyIi1lKGiE2klFjv0v'
redirect_uri = 'http://localhost:8000/callback'
authorization_response = None

# Create a simple HTTP handler to process the callback
class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global authorization_response
        authorization_response = self.path
        parsed_path = urlparse.urlparse(self.path)
        query_params = urlparse.parse_qs(parsed_path.query)

        # Extract the authorization code from the callback
        if 'code' in query_params:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Authorization code received! You can close this window.")
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Authorization code not found.")

# Function to start the local server to handle the callback
def start_local_server():
    server_address = ('', 8000)  # Listen on localhost, port 8000
    httpd = HTTPServer(server_address, CallbackHandler)
    print("Server running on http://localhost:8000/callback...")
    httpd.handle_request()  # This will handle one request (the callback) and then stop

try:
    # Set up OAuth2 user handler
    oauth2_user_handler = tweepy.OAuth2UserHandler(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=['tweet.read', 'users.read', 'follows.read']
    )

    # Get the authorization URL
    auth_url = oauth2_user_handler.get_authorization_url()
    print(f"Authorization URL: {auth_url}")

    # Open the URL in the default browser
    webbrowser.open(auth_url)

    print("Waiting for the authorization code...")

    # Start the local server to capture the authorization code
    start_local_server()

    if authorization_response:
        print(f"Authorization response received: {authorization_response}")

        # Exchange the authorization response (which includes the code) for the access token
        try:
            oauth2_user_handler.fetch_token(authorization_response=f"http://localhost:8000{authorization_response}")
            access_token = oauth2_user_handler.access_token
            print(f"Access token obtained successfully: {access_token}")
        except Exception as e:
            print(f"Error obtaining access token: {e}")
            exit(1)

        # Create a client instance with the obtained access token
        client = tweepy.Client(bearer_token=access_token)
        print("client")
        print(dir(client))


        # Test the client to verify authentication and get user info
        try:
            # Fetch the authenticated user information
            user_response = client.get_user(id='me')
            
            # Access the 'data' attribute in the response
            if user_response.data:
                print(f"Successfully authenticated as: {user_response.data.username}")
                print(user_response.data)
            else:
                print("Error: No data returned from the API.")
        except Exception as e:
            print(f"Error verifying authentication: {e}")
            exit(1)
    else:
        print("Failed to get the authorization code.")

except Exception as e:
    print(f"Error during setup: {e}")
    exit(1)

# Fetch your followers and how many followers they have
def fetch_followers_with_follower_counts():
    followers = []
    try:
        # Get authenticated user's ID
        user_id = user_response.data.id
        print("user_id")
        print(user_id)
        
        # Fetch followers (limited to 1000 per request)
        # for response in tweepy.Paginator(client.get_users_followers, 
        #                                  user_id, 
        #                                  max_results=1000):
        #     for follower in response.data:
        #         followers.append({
        #             'username': follower.username,
        #             'name': follower.name,
        #             'followers_count': follower.public_metrics['followers_count']
        #         })

        # # Display the followers and their follower counts
        # for follower in followers:
        #     print(f"Name: {follower['name']} | Handle: {follower['username']} | Followers: {follower['followers_count']}")


        ## I'm trying the below to see if I have access to my own data - it seems not, I probably don't have access to the V2 api?
        user_response2 = client.get_user(id=user_id)
        # Print the user data
        if user_response2.data:
            print(f"Username: {user_response2.data.username}")
            print(f"Name: {user_response2.data.name}")
            print(f"ID: {user_response2.data.id}")
            print(f"Public Metrics: {user_response2.data.public_metrics}")
        else:
            print("Error: No data returned for the user.")


    except tweepy.TweepyException as e:
        print(f"Error fetching followers: {e}")

# Call the function to fetch followers and their follower counts
fetch_followers_with_follower_counts()
