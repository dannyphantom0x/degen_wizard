import os
from dotenv import load_dotenv
import tweepy

load_dotenv()
BEARER_TOKEN = os.getenv('BEARER_TOKEN')

def get_latest_tweet_v2(username):
    """
    Fetch the most recent tweet from a user using API v2.

    Args:
        username (str): The Twitter handle of the user (without @).

    Returns:
        dict: A dictionary containing the tweet ID and text of the latest tweet.
    """
    try:
        # Create a Tweepy client for API v2
        client = tweepy.Client(bearer_token=BEARER_TOKEN)

        # Get user details to fetch user ID
        user = client.get_user(username=username)
        user_id = user.data.id

        # Fetch the most recent tweets (minimum valid value for max_results is 5)
        tweets = client.get_users_tweets(id=user_id, max_results=5)
        if tweets.data:
            # Get the most recent tweet
            latest_tweet = tweets.data[0]
            print("Tweet fetched successfully.")
            return {
                'id': latest_tweet.id,
                'text': latest_tweet.text
            }
        else:
            print(f"No tweets found for @{username}.")
            return None
    except tweepy.TweepyException as e:
        print(f"Error fetching tweet: {e}")
        return None

def reply_to_tweet_v2(tweet_id, message):
    """
    Replies to a specific tweet using API v2.

    Args:
        tweet_id (int): The ID of the tweet to reply to.
        message (str): The reply message.

    Returns:
        None
    """
    try:
        # Create a Tweepy client for API v2
        client = tweepy.Client(
            bearer_token=BEARER_TOKEN,
            consumer_key=os.getenv('API_KEY'),
            consumer_secret=os.getenv('API_SECRET_KEY'),
            access_token=os.getenv('ACCESS_TOKEN'),
            access_token_secret=os.getenv('ACCESS_TOKEN_SECRET')
        )

        # Post a reply
        client.create_tweet(text=message, in_reply_to_tweet_id=tweet_id)
        print("Reply posted successfully!")
    except tweepy.TweepyException as e:
        print(f"Error posting reply: {e}")


if __name__ == "__main__":
    username = ""
    reply_message = ""

    latest_tweet = get_latest_tweet_v2(username)

    if latest_tweet:
        print(f"\nMost recent tweet by @{username}:")
        print(f"{latest_tweet['text']}\n")

        reply_to_tweet_v2(tweet_id=latest_tweet['id'], message=reply_message)
    else:
        print("Failed to retrieve the latest tweet.")
