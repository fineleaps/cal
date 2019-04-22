from django.conf.urls import url
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView, logout_then_login

urlpatterns = [
    url(r'^login/$', LoginView.as_view(template_name='portal/login.html'), name='login'),
    url(r'^logout/$', logout_then_login, name='logout'),
    url(r'^$', views.home, name='home'),

    url(r'^profile/$', views.profile, name='profile'),


    url(r'^campaign/list/$', views.CampaignListView.as_view(), name='campaign_list'),
    path('campaign/detail/<int:pk>/', views.CampaignDetailView.as_view(), name='campaign_detail')


]