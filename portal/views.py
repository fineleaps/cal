from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from .models import Campaign, Executive, ProspectCampaignRelation, Prospect
from django.core.exceptions import ObjectDoesNotExist


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


def prospect_get(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    prospects = Prospect.objects.filter(assigned_campaign=campaign, prospectcampaignrelation__released=False)
    if prospects.exists():
        prospect = prospects.first()
        prospect.prospectcampaignrelation.released = True
        prospect.prospectcampaignrelation.save()
        context = {'prospect': prospect}
    else:
        context = {'no_results': True}
    context.update({'campaign': campaign})

    return render(request, 'portal/prospect_get.html', context)


