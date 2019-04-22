from django.contrib import admin
from .models import Campaign, Prospect, Lead, DNC, Executive
from django.shortcuts import get_object_or_404, render
from  django.http import HttpResponseRedirect

# pull changes
# class ExecutiveInline(admin.TabularInline):
#     model = Executive


class CampaignAdmin(admin.ModelAdmin):

    list_display = ('name', 'active_status', 'start_date', 'end_date')
    # inlines = [ExecutiveInline, ]


admin.site.register(Campaign, CampaignAdmin)


class ProspectAdmin(admin.ModelAdmin):

    list_filter = ('job_title', 'emp_size', 'industry_type', 'state')

    actions = ('assign_campaign', )

    def assign_campaign(self, request, queryset):
        if 'assign' in request.POST:
            campaign_id = request.POST['campaign_id']
            campaign = get_object_or_404(Campaign, id=campaign_id)
            for prospect in queryset:
                prospect.assigned_campaign = campaign
                prospect.save()
            if queryset.count() < 2:
                prospect_variable = 'prospect'
            else:
                prospect_variable = 'prospects'
            self.message_user(request,
                              "Successfully {prospect_count} {prospect_variable} assigned to campaign {campaign_name}.".format(
                                  prospect_count=queryset.count(),
                                  prospect_variable=prospect_variable,
                                  campaign_name=campaign.name))
            return HttpResponseRedirect(request.get_full_path())

        return render(request, 'portal/assign_campaign.html', context={'prospects': queryset,
                                                                       'campaigns': Campaign.objects.all()})


admin.site.register(Prospect, ProspectAdmin)
admin.site.register(Lead)
admin.site.register(DNC)
admin.site.register(Executive)
