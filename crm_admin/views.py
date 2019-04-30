from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse
from django.views.generic import ListView, DetailView
from portal.models import Campaign, Prospect
from .forms import CampaignAddForm
from .filters import ProspectFilter


crm_admin_login_url = '/crm_admin/login'


@login_required(login_url=crm_admin_login_url)
@user_passes_test(lambda u: u.is_superuser)
def home(request):
    return render(request, 'crm_admin/home.html')


@login_required(login_url=crm_admin_login_url)
@user_passes_test(lambda u: u.is_superuser)
def profile(request):
    return render(request, 'crm_admin/profile.html')


@login_required(login_url=crm_admin_login_url)
@user_passes_test(lambda u: u.is_superuser)
def campaign_add(request):
    if request.method == 'POST':
        form = CampaignAddForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            form = CampaignAddForm()
    else:
        form = CampaignAddForm()
    return render(request, 'crm_admin/campaign_add.html', {'form': form})


class CampaignListView(ListView):

    model = Campaign
    template_name = 'crm_admin/campaign_list.html'
    context_object_name = 'campaigns'


class ProspectListView(ListView):

    model = Prospect
    template_name = 'crm_admin/prospect_list.html'
    context_object_name = 'prospects'

#
# def prospect_list(request):
#     prospects = Prospect.objects.all()
#     prospect_filter = ProspectFilter(request.GET, queryset=prospects)
#     return render(request, 'crm_admin/prospect_list.html', {'filter': prospect_filter})


class CampaignDetailView(DetailView):
    model = Campaign
    template_name = 'portal/campaign_detail.html'
    context_object_name = 'campaign'

#
# def prospect_get(request, campaign_id):
#     campaign = get_object_or_404(Campaign, id=campaign_id)
#     prospect = campaign.prospect_get()
#     context = {'prospect': prospect} if prospect else {'no_results': True}
#     context.update({'campaign': campaign})
#     return render(request, 'portal/prospect_get.html', context)
#
#
# def prospect_attempt_result_add(request, campaign_id, prospect_id):
#     if request.method == 'POST':
#         post_dict = request.POST
#         pcr = get_object_or_404(ProspectCampaignRelation, campaign__id=campaign_id, prospect__id=prospect_id)
#         AttemptResult.objects.create(prospect_campaign_relation=pcr,
#                                      result=post_dict['result'],
#                                      by=request.user.executive,
#                                      details=post_dict['details'])
#         return redirect('prospect_get', campaign_id=pcr.campaign.id)
