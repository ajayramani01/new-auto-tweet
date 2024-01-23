from django.urls import path
from .views import *
app_name="auto_tweet"
urlpatterns = [
    path('', homePage.as_view()),
    path('tweet-api/', tweet_api.as_view(),name="tweet_api"),
    path('tweet-api-xlsx/', tweet_with_xlsx.as_view(),name="tweet_api_xlsx"),
]
