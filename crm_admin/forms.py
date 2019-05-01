from django import forms
from portal.models import Campaign, Executive


class CampaignAddForm(forms.ModelForm):

    # active_status = forms.BooleanField(widget=forms.CheckboxInput(attrs={"class": "form-check"}))

    executives = forms.ModelMultipleChoiceField(queryset=Executive.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Campaign
        fields = ('name', 'active_status', 'start_date', 'end_date',
                  'script', 'details', 'executives')
