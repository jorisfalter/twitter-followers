# Set up OAuth 1.0a User Context (requires user authorization)
auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret)

# Redirect the user to the authorization page and get a request token
redirect_url = auth.get_authorization_url()
print(f"Go to this URL to authorize: {redirect_url}")

# After authorization, the user will get a PIN, enter it here
verifier = input('Enter the authorization PIN: ')

# Exchange the request token for an access token
auth.get_access_token(verifier)

# Now you can use the access token to make requests
api = tweepy.API(auth)

# Get authenticated user’s profile information
user_profile = api.verify_credentials()
print(f"My profile: {user_profile.screen_name}, Followers count: {user_profile.followers_count}")

# Fetch your followers and how many followers they have
def fetch_followers_with_follower_counts():
    followers = []
    try:
        # Get up to 200 followers per request (this is the limit per request)
        for follower in tweepy.Cursor(api.get_followers, screen_name=user_profile.screen_name, count=200).items():
            followers.append({
                'screen_name': follower.screen_name,
                'name': follower.name,
                'followers_count': follower.followers_count
            })

        # Display the followers and their follower counts
        for follower in followers:
            print(f"Name: {follower['name']} | Handle: {follower['screen_name']} | Followers: {follower['followers_count']}")

    except tweepy.TweepyException as e:
        print(f"Error fetching followers: {e}")

# Call the function to fetch followers and their follower counts
fetch_followers_with_follower_counts()