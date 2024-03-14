from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from datetime import datetime
from .utils import opendriver,generateWinnerLoser,generateimageWinLos
from .models import verifiedUser
import pandas as pd

from django.http import HttpResponse


# Create your views here.
class scrape_x(TemplateView):
    template_name = "verifiedBySensiBull/scrape_x.html"
    extra_context={}
    def get(self, *args, **kwargs):

        return super().get(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        df = pd.DataFrame(list(verifiedUser.objects.all().values()))
        df.drop(['id'],axis=1,inplace=True)
        response = HttpResponse(content_type='application/xlsx')
        response['Content-Disposition'] = f'attachment; filename="X_data.xlsx"'
        with pd.ExcelWriter(response) as writer:
            df.to_excel(writer, sheet_name='verifiedbysensibull',index=False)

        return response
        return super().get(*args, **kwargs) 
    
class scrape_data(TemplateView):
    template_name = "verifiedBySensiBull/scrape_x.html"
    extra_context={}
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        opendriver()
        return super().get(request,*args, **kwargs)

class generate(TemplateView):
    template_name = "verifiedBySensiBull/WinnerLoser.html"
    extra_context={}
    def get(self, *args, **kwargs):
        # date=datetime(2024,2,5).date()
        # date=datetime.today().date()
        date=(datetime.strptime(self.kwargs['date'],'%Y-%m-%d')).date()
        
        WinnerLoser=generateWinnerLoser(date)
        list_of_winlose=[]
        for i in WinnerLoser:
            list_of_winlose.append(verifiedUser.objects.get(id=i))
        self.extra_context['Winner']=list_of_winlose[0:5]
        self.extra_context['Loser']=list_of_winlose[5:]
        self.extra_context['date']=date
        return super().get(*args, **kwargs)

    def post(self, *args, **kwargs):
        # date=datetime(2024,1,31).date()
        # date=datetime.today().date()

        # WinnerLoser=generateWinnerLoser(date)
        # list_of_winlose=[]
        # for i in WinnerLoser:
        #     list_of_winlose.append(verifiedUser.objects.get(id=i))
        # self.extra_context['Winner']=list_of_winlose[0:5]
        # self.extra_context['Loser']=list_of_winlose[5:]
        # self.extra_context['date']=date
        return super().get(self,*args, **kwargs) 