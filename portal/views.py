from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from .models import Campaign, Executive


@login_required
def home(request):
    return render(request, 'portal/home.html')


@login_required
def profile(request):

    abcd = {}

    return render(request, 'portal/profile.html', abcd)


class CampaignListView(ListView):

    model = Campaign
    template_name = 'portal/campaign_list.html'
    context_object_name = 'campaigns'

    def get_queryset(self):
        return Campaign.objects.filter(executives__in=(self.request.user.executive, ))


class CampaignDetailView(DetailView):
    model = Campaign
    template_name = 'portal/campaign_detail.html'
    context_object_name = 'campaign'

