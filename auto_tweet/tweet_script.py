from core.settings import X_API_KEY,X_API_SECRET,X_ACCESS_TOKEN,X_ACCESS_TOKEN_SECRET,X_BEARER_TOKEN
# importing the module 
import tweepy 

# personal details 
consumer_key = X_API_KEY
consumer_secret = X_API_SECRET
bearer_token= X_BEARER_TOKEN
access_token = X_ACCESS_TOKEN
access_token_secret = X_ACCESS_TOKEN_SECRET

client = tweepy.Client(bearer_token,consumer_key,consumer_secret,access_token,access_token_secret)
# authentication of consumer key and secret 
auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 

# authentication of access token and secret 
auth.set_access_token(access_token, access_token_secret) 
api = tweepy.API(auth)

def tweet_with_image(tweet,image_path):
  
    # to attach the media file 
    mediaId=api.media_upload(filename=image_path[1:]).media_id_string

    client.create_tweet(text=tweet,media_ids=[mediaId])

  
def tweet_text(tweet):
    client.create_tweet(text=tweet)