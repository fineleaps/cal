# Generated by Django 2.0 on 2019-04-29 02:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0016_auto_20190429_0225'),
    ]

    operations = [
        migrations.AddField(
            model_name='attemptresult',
            name='prospect_campaign_relation',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='portal.ProspectCampaignRelation'),
            preserve_default=False,
        ),
    ]
