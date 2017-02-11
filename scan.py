import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from twitter import *
from grove_rgb_lcd import *
import os

nltk.download('vader_lexicon')

APP_NAME = os.getenv('APP_NAME', 'My App')
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')

MY_TWITTER_CREDS = os.path.expanduser('~/.my_app_credentials')

ANALYZER = SentimentIntensityAnalyzer()


def authenticated_stream():
    """
    Retrieves the Twitter stream. Will make you do stuff.
    """
    if not os.path.exists(MY_TWITTER_CREDS):
        oauth_dance(APP_NAME, CONSUMER_KEY, CONSUMER_SECRET, MY_TWITTER_CREDS)
    oauth_token, oauth_secret = read_token_file(MY_TWITTER_CREDS)
 
    return TwitterStream(auth=OAuth(oauth_token, oauth_secret, 
                                    CONSUMER_KEY, CONSUMER_SECRET))


def banner(user, text, sentiment):
    """
    Display text in a banner, colored with the sentiment
    """
    setRGB(int(sentiment['neg'] * 255), int(sentiment['pos'] * 255), int(sentiment['neu'] * 255))
    text = "%s %s " % (user, text)
    text_len = len(text)
    width = min([32, text_len])
    [setText(text[i:i+width]) or time.sleep(0.1) for i in range(0, text_len)]


if __name__ == "__main__":
    for message in authenticated_stream().statuses.filter(track="atlanta"):
        if 'text' in message:
            banner(message['user'], message['text'], ANALYZER.polarity_scores(message['text']))
