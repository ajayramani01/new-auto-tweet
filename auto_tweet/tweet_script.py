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

def tweet_with_image_with_login(bearer_token_x,consumer_key_x,consumer_secret_x,access_token_x,access_token_secret_x,tweet,image_path):
    client_x = tweepy.Client(bearer_token_x,consumer_key_x,consumer_secret_x,access_token_x,access_token_secret_x)
    # authentication of consumer key and secret 
    auth_x = tweepy.OAuthHandler(consumer_key_x, consumer_secret_x) 

    # authentication of access token and secret 
    auth_x.set_access_token(access_token_x, access_token_secret_x) 
    api_x = tweepy.API(auth_x)
  
    # to attach the media file 
    try:
        mediaId=api_x.media_upload(filename=image_path[1:]).media_id_string
    except:
        # image_path='/home/alkatraz019/Desktop/AplusTopper/AutoTweet/'+image_path[1:]
        image_path='C:/Users/ajayt/Desktop/Aplus Topper/New Task/AutoTweet__/AutoTweet/'+image_path[1:]
        mediaId=api_x.media_upload(filename=image_path).media_id_string
    print("TWEET IS DONE")
    client_x.create_tweet(text=tweet,media_ids=[mediaId])

# from PIL import Image
# from io import BytesIO
# import requests
# import os
# from datetime import datetime
# base_directory = 'C:/Users/ajayt/Desktop/Aplus Topper/New Task/AutoTweet__/AutoTweet/media/tweet'
# def fetch_profile_image_url(screen_name):
#     user = api.get_user(screen_name=screen_name)
#     return user.profile_image_url_https

# def download_image(url, save_path):
#     response = requests.get(url)
#     if response.status_code == 200:
#         img = Image.open(BytesIO(response.content))
#         img.save(save_path)
#         print(f"Image saved to {save_path}")
#     else:
#         print("Failed to retrieve image.")

# def save_image(screen_name):
#     current_date = datetime.today().strftime('%Y-%m-%d')
#     date_directory = os.path.join(base_directory, current_date)
#     if not os.path.exists(date_directory):
#         os.makedirs(date_directory)
#     image_url = fetch_profile_image_url(screen_name)
#     if '_normal' in image_url:
#         image_url = image_url.replace('_normal', '')
#     save_path = os.path.join(date_directory, screen_name + '.jpg')
#     download_image(image_url, save_path)