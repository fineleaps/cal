# Generated by Django 2.0 on 2019-04-22 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0005_campaignexecutiverelation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prospect',
            name='zip_code',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
