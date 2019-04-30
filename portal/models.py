from django.db import models
from django.conf import settings
import datetime
from django.core.validators import ValidationError
from django.db.models.signals import pre_save, post_save
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse


class Executive(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    date_of_birth = models.DateField(blank=True, null=True)
    details = models.TextField(blank=True)

    def take_age(self):
        return datetime.date.today() - self.date_of_birth

    def __str__(self):
        return self.user.username


class Campaign(models.Model):
    name = models.CharField(max_length=64)
    active_status = models.BooleanField(default=True)
    script = models.TextField(blank=True)
    details = models.TextField(blank=True)
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)
    executives = models.ManyToManyField(Executive, blank=True)
    prospects = models.ManyToManyField('Prospect', blank=True, through='ProspectCampaignRelation')

    def __str__(self):
        return self.name

    def prospects_attempted(self):
        return self.prospects.filter(prospectcampaignrelation__attempted=True)

    def prospects_non_attempted(self):
        return self.prospects.filter(prospectcampaignrelation__attempted=False)

    def prospect_get(self):
        f_prospect = self.prospects_non_attempted().first()
        if f_prospect:
            f_prospect.make_campaign_attempted(self.id)
            return f_prospect
        else:
            return False


class ProspectCampaignRelation(models.Model):
    prospect = models.ForeignKey('Prospect', on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    from_date = models.DateField(auto_now_add=True)
    attempted = models.BooleanField(default=False)
    details = models.TextField(blank=True)

    def __str__(self):
        return "{} -- {}".format(self.prospect, self.campaign)

    class Meta:
        unique_together = ('prospect', 'campaign')


AttemptResultChoices = (('Lead', 'Lead'), ('View', 'View'), ('DNC', 'DNC'))


class AttemptResult(models.Model):
    prospect_campaign_relation = models.OneToOneField(ProspectCampaignRelation, on_delete=models.CASCADE)
    on = models.DateTimeField(auto_now_add=True)
    by = models.ForeignKey(Executive, on_delete=models.CASCADE)
    result = models.CharField(max_length=20, choices=AttemptResultChoices)
    details = models.TextField(blank=True)

    def __str__(self):
        return "{} -{} - {}".format(self.prospect_campaign_relation.prospect, self.prospect_campaign_relation.campaign,
                              self.result)

    def clean(self):
        if not self.prospect_campaign_relation.attempted:
            raise ValidationError('Prospect must be attempted to save attempt result')


class Prospect(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    phone = models.CharField(max_length=15, blank=True)
    direct_or_extension = models.CharField(max_length=16, blank=True)
    email = models.EmailField(blank=True)
    company = models.CharField(max_length=128, blank=True)
    emp_size = models.CharField(max_length=16, blank=True)
    website = models.CharField(max_length=64, blank=True)
    job_title = models.CharField(max_length=64, blank=True)
    industry_type = models.CharField(max_length=64, blank=True)
    city = models.CharField(max_length=32, blank=True)
    state = models.CharField(max_length=32, blank=True)
    country = models.CharField(max_length=32, blank=True)
    zip_code = models.IntegerField(blank=True, null=True)
    details = models.TextField(blank=True)

    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return self.full_name

    def campaigns_assigned(self):
        return self.campaign_set.all()

    def make_campaign_attempted(self, campaign_id):
        pcr = self.prospectcampaignrelation_set.get(campaign_id=campaign_id)
        pcr.attempted = True
        pcr.save()
        """ Remember to use .filter with update method if this got slow"""


class CampaignSepration(models.Model):
    name = models.CharField(max_length=32)
    file = models.FileField(upload_to='separation_files/')
    details = models.TextField(blank=True)
    campaign = models.ManyToManyField(Campaign, blank=True)

    def __str__(self):
        return self.name