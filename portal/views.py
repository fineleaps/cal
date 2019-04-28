from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from .models import Campaign, Executive, ProspectCampaignRelation, Prospect, AttemptResult
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
    prospect = campaign.prospect_get()
    context = {'prospect': prospect} if prospect else {'no_results': True}
    context.update({'campaign': campaign})
    return render(request, 'portal/prospect_get.html', context)


def prospect_attempt_result_add(request, campaign_id, prospect_id):
    if request.method == 'POST':
        post_dict = request.POST
        pcr = get_object_or_404(ProspectCampaignRelation, campaign__id=campaign_id, prospect__id=prospect_id)
        AttemptResult.objects.create(prospect_campaign_relation=pcr,
                                     result=post_dict['result'],
                                     by=request.user.executive,
                                     details=post_dict['details'])
        return redirect('prospect_get', campaign_id=pcr.campaign.id)
