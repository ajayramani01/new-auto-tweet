from django.urls import path
from .views import *
app_name="verifiedBySensiBull"
urlpatterns = [
    path('scrape-x/', scrape_x.as_view(),name="scrape_x"),
    path('get-data-from-X/', scrape_data.as_view(),name="scrape_X"),
    path('export-xlsx/', scrape_x.as_view(),name="export_xlsx"),
    path('test/', generate.as_view(),name="generate_winner"),
]
