import django_filters
from portal.models import Prospect
from django import forms


# from django.forms import CheckboxSelectMultiple
# from smart_selects.widgets import JqueryMediaMixin
# class ChainedCheckboxSelectMultiple(JqueryMediaMixin, CheckboxSelectMultiple):
#     pass


IND_CHOICES = [(i, i) for i in Prospect.objects.all().values_list('industry_type', flat=True).distinct()]
IND_CHOICES[IND_CHOICES.index(('', ''))] = ('', 'Blank')


class ProspectFilter(django_filters.FilterSet):

    industry_type = django_filters.MultipleChoiceFilter(choices=IND_CHOICES, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Prospect
        fields = ['industry_type', 'job_title', 'state', 'emp_size']
