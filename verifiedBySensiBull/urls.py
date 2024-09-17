from django.urls import path
from .views import *
app_name="verifiedBySensiBull"
urlpatterns = [
    path('scrape-x/', scrape_x.as_view(),name="scrape_x"),
    path('get-data-from-X/', scrape_data.as_view(),name="scrape_X"),
    path('export-xlsx/', scrape_x.as_view(),name="export_xlsx"),
    path('image-gen/<str:date>/', generate.as_view(),name="generate_winner"),
    path('new-view', New_View.as_view(), name='new_view'),
    path('show-data/<str:date>/', ShowDataView.as_view(), name='show_data'),
    path('leaderboard-profit/', leaderboard_profit, name='leaderboard_profit'),
    path('leaderboard-loss/', leaderboard_loss, name='leaderboard_loss'),
    path('performance/<str:twitter_username>/<str:sensibull_username>/', Individual_trader_performance, name='performance'),
]
