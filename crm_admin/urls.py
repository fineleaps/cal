from django.conf.urls import url
from django.contrib.auth.views import LoginView, logout_then_login
from . import views
from django.urls import path
from django_filters.views import FilterView
from .filters import ProspectFilter

app_name = 'crm_admin'

urlpatterns = [
    url(r'^login/$', LoginView.as_view(template_name='crm_admin/login.html'), name='login'),
    url(r'^logout/$', logout_then_login, {'login_url': '/crm_admin/login/'}, name='logout'),
    url(r'^$', views.home, name='home'),

    url(r'^profile/$', views.profile, name='profile'),


    url(r'^campaign/add/$', views.campaign_add, name='campaign_add'),
    url(r'^campaign/list/$', views.CampaignListView.as_view(), name='campaign_list'),
    path('campaign/detail/<int:pk>/', views.CampaignDetailView.as_view(), name='campaign_detail'),

    url(r'^prospect/list/$', views.ProspectListView.as_view(), name='prospect_list'),
    url(r'^prospect/search/$', FilterView.as_view(filterset_class=ProspectFilter,
                                                  template_name='crm_admin/prospect_search.html'), name='prospect_search')

    # url(r'^prospect/get/(?P<campaign_id>[0-9]+)$', views.prospect_get, name='prospect_get'),
    # url(r'^prospect/attempt_result/add/(?P<campaign_id>[0-9]+)/(?P<prospect_id>[0-9]+)/$',
    #     views.prospect_attempt_result_add, name='prospect_attempt_result_add'),

]
