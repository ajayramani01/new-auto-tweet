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
        print(WinnerLoser)
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

from .utils import *
from django.db.models import F
import pandas as pd
from django.urls import reverse
class New_View(TemplateView):
    template_name = "verifiedBySensiBull/new_view.html"
    extra_context = {}

    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        print(action)
        if action == 'scrape':
            helper()
            return redirect(reverse('verifiedBySensiBull:show_data', kwargs={'date': datetime.today().strftime('%Y-%m-%d')}))

        elif action == 'show':
            return redirect(reverse('verifiedBySensiBull:show_data', kwargs={'date': datetime.today().strftime('%Y-%m-%d')}))

        elif action == 'download':
            # Download data
            df = pd.DataFrame(list(verifiedUser.objects.all().values()))
            df['date'] = pd.to_datetime(df['date'])
            df.drop(['id'], axis=1, inplace=True)
            df.sort_values(by='date', ascending=False, inplace=True)
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            # response = HttpResponse(content_type='application/xlsx')
            response['Content-Disposition'] = 'attachment; filename="X_data.xlsx"'
            with pd.ExcelWriter(response) as writer:
                df.to_excel(writer, sheet_name='verifiedbysensibull', index=False)
            return response
        return super().get(request, *args, **kwargs)

class ShowDataView(TemplateView):
    template_name = "verifiedBySensiBull/show_data.html"
    extra_context = {}

    def get(self, request, *args, **kwargs):
        provided_date = datetime.strptime(kwargs['date'], '%Y-%m-%d').date()
        df = pd.DataFrame(list(verifiedUser.objects.all().values()))
        df["date"] = df['date'].map(lambda date: date.date())
        df = df[df.date == provided_date]
        df = df[df.totalPL != '']
        df["totalPL"] = df['totalPL'].map(lambda totalPL: totalPL.replace(',',''))
        df["totalPL"] = df['totalPL'].map(lambda totalPL: totalPL.replace('L','*10e5'))
        df["totalPL"] = df['totalPL'].map(lambda totalPL: totalPL.replace('Cr','*10e7'))
        df["totalPL"] = df['totalPL'].map(lambda totalPL: eval(totalPL))
        profit_entries = df[df['totalPL'] > 0].sort_values(by='totalPL', ascending=False).head(5)
        lose_entries = df[df['totalPL'] < 0].sort_values(by='totalPL').head(5)
        # profit_ids = profit_entries['id'].tolist()
        # lose_ids = lose_entries['id'].tolist()
        # print(profit_ids)
        # print(lose_ids)
        self.extra_context['Winner'] = profit_entries.to_dict(orient='records')
        self.extra_context['Loser'] = lose_entries.to_dict(orient='records')
        self.extra_context['date'] = provided_date

        return super().get(request, *args, **kwargs)

from datetime import datetime
def leaderboard_profit(request):
    traders = web_scrap('pl_desc')
    try:
        date = datetime.today().strftime("%a %b %d %Y")
    except:
        date = datetime.datetime.strftime("%a %b %d %Y")
    return render(request, 'verifiedBySensiBull/leaderboard.html', {'traders': traders,'date':date})

def leaderboard_loss(request):
    traders = web_scrap('pl_asc')
    try:
        date = datetime.today().strftime("%a %b %d %Y")
    except:
        date = datetime.datetime.today().strftime("%a %b %d %Y")
    return render(request, 'verifiedBySensiBull/leaderboard.html', {'traders': traders,'date':date})

def Individual_trader_performance(request,twitter_username, sensibull_username):
    traders = [{
        'month':'MONTH',
        'total_value': 'NET',
        'record_count':'DAYS'
    }]
    sensibull_url = 'https://web.sensibull.com/verified-pnl/' + sensibull_username
    traders += history(sensibull_url)
    try:
        date = datetime.today().strftime("%a %b %d %Y")
    except:
        date = datetime.datetime.strftime("%a %b %d %Y")
    return render(request, 'verifiedBySensiBull/performance.html', {'traders': traders,'username':twitter_username})