from django.urls import path
from . import views

app_name = "EmailCampaign"

urlpatterns = [
    path("subscribe/", views.SubscribeView.as_view(), name="subscribe"),
    path("unsubscribe/", views.UnsubscribeView.as_view(), name="unsubscribe"),
    path("mail/", views.send_campaigns, name="send_compaigns"),
    path("", views.home, name="home"),
]
