from django import forms
from portal.models import Campaign


class CampaignAddForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ('name', 'active_status', 'start_date', 'end_date',
                  'script', 'details', 'executives', 'prospects')
