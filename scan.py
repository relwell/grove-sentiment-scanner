from twitter import *
from grove_rgb_lcd import *
import os


APP_NAME = os.getenv('APP_NAME', 'My App')
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')

MY_TWITTER_CREDS = os.path.expanduser('~/.my_app_credentials')

def authenticated_stream():
    """
    Retrieves the Twitter stream. Will make you do stuff.
    """
    if not os.path.exists(MY_TWITTER_CREDS):
        oauth_dance(APP_NAME, CONSUMER_KEY, CONSUMER_SECRET, MY_TWITTER_CREDS)
    oauth_token, oauth_secret = read_token_file(MY_TWITTER_CREDS)
 
    return TwitterStream(auth=OAuth(oauth_token, oauth_secret, 
                                    CONSUMER_KEY, CONSUMER_SECRET),
                         domain="userstream.twitter.com")




if __name__ == "__main__":
    for message in authenticated_stream().user():
        print message
