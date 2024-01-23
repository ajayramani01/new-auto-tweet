from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from datetime import datetime
from .utils import opendriver,getUserData
from .models import verifiedUser
import pandas as pd

from django.http import HttpResponse
from io import BytesIO

# Create your views here.
class scrape_x(TemplateView):
    template_name = "verifiedBySensiBull/scrape_x.html"
    extra_content={}
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
    extra_content={}
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        opendriver()
        return super().get(request,*args, **kwargs) 