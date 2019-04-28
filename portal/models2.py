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
    # executives = models.ManyToManyField(Executive, through='CampaignExecutiveRelation', blank=True)
    executives = models.ManyToManyField(Executive, blank=True)

    def __str__(self):
        return self.name


class CampaignExecutiveRelation(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    executive = models.ForeignKey(Executive, on_delete=models.CASCADE)
    # active = models.BooleanField(default=False, validators=[active_status_validate])
    active = models.BooleanField(default=False)
    from_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)
    details = models.TextField(blank=True)

    def __str__(self):
        return "{} -- {}".format(self.campaign.name, self.executive.user)


def executive_campaign_active_check(instance, sender, *args, **kwargs):
    if instance.campaign_executive_relation_set.filter(active=True).count > 0:
        raise ValidationError


pre_save.connect(executive_campaign_active_check, CampaignExecutiveRelation)


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

    assigned_campaign = models.ForeignKey(Campaign, on_delete=models.SET_NULL, blank=True, null=True)

    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return self.full_name

    @property
    def released(self):
        return self.prospectcampaignrelation.released


def save_campaign_relation(sender, instance, *args, **kwargs):
    try:
        pcr = ProspectCampaignRelation.objects.get(prospect=instance)
        print(pcr)
        if pcr.campaign != instance.assigned_campaign:
            pcr.campaign = instance.assigned_campaign
            pcr.released = False
            pcr.save()
    except ObjectDoesNotExist:
        print(555)
        # ProspectCampaignRelation.objects.create(prospect=instance, campaign=instance.assigned_campaign)


post_save.connect(save_campaign_relation, sender=Prospect)


class ProspectCampaignRelation(models.Model):
    prospect = models.OneToOneField(Prospect, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    from_date = models.DateField(auto_now_add=True)
    released = models.BooleanField(default=False)

    def __str__(self):
        return "{} -- {}".format(self.prospect, self.campaign)

    # class Meta:
    #     unique_together = ('prospect', 'campaign')
    #

# def make_unreleased(sender,changed, instance, *args, **kwargs):
#     if changed:
#         instance.rel


class Lead(models.Model):
    prospect = models.ForeignKey(Prospect, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    executive = models.ForeignKey(Executive, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    on = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('campaign', 'prospect')

    def __str__(self):
        return "{} -- {}".format(self.prospect, self.campaign.name)


class DNC(models.Model):
    prospect = models.ForeignKey(Prospect, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    executive = models.ForeignKey(Executive, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    on = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('campaign', 'prospect')

    def __str__(self):
        return "{} -- {}".format(self.prospect, self.campaign.name)
