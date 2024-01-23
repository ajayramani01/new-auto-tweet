from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import tweet_history,xlsxFiles
from .tweet_script import *
from datetime import datetime
from .utils import generateIMG
# Create your views here.
class homePage(TemplateView):
    template_name = "auto_tweet/homePage.html"
    extra_content={}
    def get(self, *args, **kwargs):

        return super().get(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().get(*args, **kwargs)
      
class tweet_api(TemplateView):
    template_name = "auto_tweet/done.html"
    extra_content={}
    def get(self, *args, **kwargs):
        return redirect("")

    def post(self, request, *args, **kwargs):
        tweet=request.POST['tweet']
        if 'tweet_img' in request.FILES:
            tweet_img=request.FILES['tweet_img']
        else:
            tweet_img=None
        x_msg=tweet_history.objects.create(tweet=tweet,tweet_img=tweet_img)
        if x_msg.tweet_img != None:
            tweet_with_image(x_msg.tweet,x_msg.tweet_img.url)
        else:
            tweet_text(x_msg.tweet)
        return super().get(request,*args, **kwargs)
    
class tweet_with_xlsx(TemplateView):
    template_name = "auto_tweet/done.html"
    extra_content = {}
    
    def get(self, *args, **kwargs):
        return redirect("")
    
    def post(self, request, *args, **kwargs):
        tweet=request.POST['tweet']
        xlsxFile = request.FILES['xlsxFile']
        todaysXlsx = xlsxFiles.objects.create(xlsx=xlsxFile)

        generateIMG(todaysXlsx,tweet)

        return super().get(request,*args, **kwargs)
