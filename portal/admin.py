from django.contrib import admin
from .models import Campaign, Prospect, Executive, ProspectCampaignRelation, AttemptResult, CampaignSepration
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect

# pull changes
# bdifsdiufh
# class ExecutiveInline(admin.TabularInline):
#     model = Executive


class CampaignAdmin(admin.ModelAdmin):
    class Media:
        js = ['admin/js/mselect-to-mcheckbox.js', ]
        css = {
            'all': ('admin/css/mselect-to-mcheckbox.css', )
        }
    #   TO MAKE SELECT-MULTIPLE WIDGET CLEAN

    list_display = ('name', 'active_status', 'start_date', 'end_date')
    # inlines = [ExecutiveInline, ]


admin.site.register(Campaign, CampaignAdmin)


class ProspectAdmin(admin.ModelAdmin):

    list_filter = ('job_title', 'emp_size', 'industry_type', 'state')
    list_display = ('full_name', 'job_title', 'industry_type', 'state')

    actions = ('assign_campaign', )

    def assign_campaign(self, request, queryset):
        if 'assign' in request.POST:
            campaign = get_object_or_404(Campaign, id=request.POST['campaign_id'])
            ProspectCampaignRelation.objects.bulk_create((ProspectCampaignRelation(prospect=prospect, campaign=campaign)
                                                          for prospect in  queryset))
            prospect_variable = 'prospects' if queryset.count() > 1 else 'prospect'
            self.message_user(request,
                              "Successfully {prospect_count} {prospect_variable} assigned to campaign {campaign_name}.".format(
                                  prospect_count=queryset.count(),
                                  prospect_variable=prospect_variable,
                                  campaign_name=campaign.name))
            return HttpResponseRedirect(request.get_full_path())

        return render(request, 'portal/assign_campaign.html', context={'prospects': queryset,
                                                                       'campaigns': Campaign.objects.all()})


class ProspectCampaignRelationAdmin(admin.ModelAdmin):
    list_display = ('prospect', 'campaign', 'attempted')


class AttemptResultAdmin(admin.ModelAdmin):
    list_display = ('prospect_campaign_relation', 'on', 'by', 'result')
    list_filter = ('prospect_campaign_relation', 'on', 'by', 'result')


admin.site.register(Prospect, ProspectAdmin)
admin.site.register(Executive)
admin.site.register(ProspectCampaignRelation, ProspectCampaignRelationAdmin)
admin.site.register(AttemptResult, AttemptResultAdmin)
admin.site.register(CampaignSepration)

class myModelAdmin(admin.ModelAdmin):
  class Media:
    js = ['admin/js/mselect-to-mcheckbox.js']
    css = {
      'all': ('admin/css/mselect-to-mcheckbox.css')
    }