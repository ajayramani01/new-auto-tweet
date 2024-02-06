from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import tweet_history,xlsxFiles
from .tweet_script import *
from datetime import datetime
import json
from .utils import return_json_of_xlsx,generateImageXlsx
# Create your views here.
class homePage(TemplateView):
    template_name = "auto_tweet/homePage.html"
    extra_context={}
    def get(self, *args, **kwargs):

        return super().get(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().get(*args, **kwargs)
      
class tweet_api(TemplateView):
    template_name = "auto_tweet/done.html"
    extra_context={}
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
    extra_context = {}
    
    def get(self, *args, **kwargs):
        return redirect("")
    
    def post(self, request, *args, **kwargs):
        tweet=request.POST['tweet']
        xlsxFile = request.FILES['xlsxFile']
        todaysXlsx = xlsxFiles.objects.create(xlsx=xlsxFile)
        generateImageXlsx(tweet)

        
        return redirect('/xlsx-data/')
        # return super().get(request,*args, **kwargs)
    
class tweet_with_xlsx_data(TemplateView):
    template_name = "auto_tweet/xlsx-data.html"
    extra_context = {}
    
    def get(self, *args, **kwargs):
        todaysXlsx=xlsxFiles.objects.last()
        jsons_list=return_json_of_xlsx(todaysXlsx)
        bank_nifty = [] 
        bank_nifty = json.loads(jsons_list[0]) 
        nifty = [] 
        nifty = json.loads(jsons_list[1]) 
        fin_nifty = [] 
        fin_nifty = json.loads(jsons_list[2]) 
        self.extra_context["bank_nifty"]=bank_nifty
        self.extra_context["nifty"]=nifty
        self.extra_context["fin_nifty"]=fin_nifty

        return super().get(*args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        
        return super().get(request,*args, **kwargs)
