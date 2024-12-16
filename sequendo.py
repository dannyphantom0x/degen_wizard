import os
import random
from dotenv import load_dotenv
import tweepy

# Load environment variables from .env file
load_dotenv()

# Twitter API credentials
API_KEY = os.getenv('API_KEY')
API_SECRET_KEY = os.getenv('API_SECRET_KEY')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')


def authenticate():
    """
    Authenticate to the Twitter API and return a Tweepy API object.
    """
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return tweepy.API(auth)


def send_random_message(api, username, message):
    """
    Send a direct message to a random follower of the specified user.

    Args:
        api: Tweepy API object.
        username (str): Twitter handle (without @) of the target user.
        message (str): The message to send.
    """
    try:
        # Get followers
        followers = api.followers(screen_name=username)
        if not followers:
            print(f"No followers found for @{username}.")
            return

        # Choose a random follower
        random_follower = random.choice(followers)
        follower_name = random_follower.screen_name

        # Send direct message
        api.send_direct_message(recipient_id=random_follower.id, text=message)
        print(f"Message sent to @{follower_name}: {message}")
    except Exception as e:
        print(f"Error sending message: {e}")


def follow_random_person(api, target_user):
    """
    Follow a random person that the target user is following.

    Args:
        api: Tweepy API object.
        target_user (str): Twitter handle (without @) of the target user.
    """
    try:
        # Get people the target user is following
        friends = api.friends(screen_name=target_user)
        if not friends:
            print(f"No friends found for @{target_user}.")
            return

        # Choose a random friend to follow
        random_friend = random.choice(friends)
        friend_name = random_friend.screen_name

        # Follow the chosen user
        api.create_friendship(screen_name=friend_name)
        print(f"Followed @{friend_name}")
    except Exception as e:
        print(f"Error following user: {e}")


if __name__ == "__main__":
    api = authenticate()
    target_username = ''
    message = ''
    send_random_message(api, username=target_username, message=message)
    follow_random_person(api, target_user=target_username)
