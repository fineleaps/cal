import django_filters
from portal.models import Prospect
from django import forms


# from django.forms import CheckboxSelectMultiple
# from smart_selects.widgets import JqueryMediaMixin
# class ChainedCheckboxSelectMultiple(JqueryMediaMixin, CheckboxSelectMultiple):
#     pass


IND_CHOICES = [(i, i) for i in Prospect.objects.all().values_list('industry_type', flat=True).distinct()]
if ('', '') in IND_CHOICES:
    IND_CHOICES[IND_CHOICES.index(('', ''))] = ('', 'Blank')

JOB_TITLE_CHOICES = [(i, i) for i in Prospect.objects.all().values_list('job_title', flat=True).distinct()]
if ('', '') in JOB_TITLE_CHOICES:
    JOB_TITLE_CHOICES[JOB_TITLE_CHOICES.index(('', ''))] = ('', 'Blank')

STATE_CHOICES = [(i, i) for i in Prospect.objects.all().values_list('state', flat=True).distinct()]
if ('', '') in STATE_CHOICES:
    STATE_CHOICES[STATE_CHOICES.index(('', ''))] = ('', 'Blank')

EMP_SIZE_CHOICES = [(i, i) for i in Prospect.objects.all().values_list('emp_size', flat=True).distinct()]
if ('', '') in EMP_SIZE_CHOICES:
    EMP_SIZE_CHOICES[EMP_SIZE_CHOICES.index(('', ''))] = ('', 'Blank')


class ProspectFilter(django_filters.FilterSet):
    #
    # industry_type = django_filters.MultipleChoiceFilter(choices=IND_CHOICES, widget=forms.CheckboxSelectMultiple(
    #     attrs={'style': "height: 200px; overflow: scroll"}))
    # job_title = django_filters.MultipleChoiceFilter(choices=JOB_TITLE_CHOICES,  widget=forms.CheckboxSelectMultiple(
    #     attrs={'style': "height: 200px; overflow: scroll"}))
    # state = django_filters.MultipleChoiceFilter(choices=STATE_CHOICES,  widget=forms.CheckboxSelectMultiple(
    #     attrs={'style': "height: 200px; overflow: scroll"}))
    # emp_size = django_filters.MultipleChoiceFilter(choices=EMP_SIZE_CHOICES,  widget=forms.CheckboxSelectMultiple(
    #     attrs={'style': "height: 200px; overflow: scroll"}))

    industry_type = django_filters.MultipleChoiceFilter(choices=IND_CHOICES, widget=forms.CheckboxSelectMultiple)
    job_title = django_filters.MultipleChoiceFilter(choices=JOB_TITLE_CHOICES,  widget=forms.CheckboxSelectMultiple)
    state = django_filters.MultipleChoiceFilter(choices=STATE_CHOICES,  widget=forms.CheckboxSelectMultiple)
    emp_size = django_filters.MultipleChoiceFilter(choices=EMP_SIZE_CHOICES,  widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Prospect
        fields = ['industry_type', 'job_title', 'state', 'emp_size']
