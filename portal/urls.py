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
    path('campaign/detail/<int:pk>/', views.CampaignDetailView.as_view(), name='campaign_detail'),


    url(r'^prospect/get/(?P<campaign_id>[0-9]+)$', views.prospect_get, name='prospect_get'),


    url(r'^prospect/attempt_result/add/(?P<campaign_id>[0-9]+)/(?P<prospect_id>[0-9]+)/$',
        views.prospect_attempt_result_add, name='prospect_attempt_result_add'),

]