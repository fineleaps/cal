# Generated by Django 2.0 on 2019-04-10 14:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('active_status', models.BooleanField(default=True)),
                ('script', models.TextField(blank=True)),
                ('text', models.TextField(blank=True)),
                ('start_date', models.DateField(blank=True)),
                ('end_date', models.DateField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='DNC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True)),
                ('on', models.DateField(auto_now_add=True)),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal.Campaign')),
            ],
        ),
        migrations.CreateModel(
            name='Executive',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('details', models.TextField(blank=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True)),
                ('on', models.DateField(auto_now_add=True)),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal.Campaign')),
                ('executive', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal.Executive')),
            ],
        ),
        migrations.CreateModel(
            name='Prospect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=32)),
                ('last_name', models.CharField(max_length=32)),
                ('phone', models.CharField(blank=True, max_length=15)),
                ('direct_or_extension', models.CharField(blank=True, max_length=16)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('company', models.CharField(blank=True, max_length=128)),
                ('emp_size', models.CharField(blank=True, max_length=16)),
                ('website', models.CharField(blank=True, max_length=64)),
                ('job_title', models.CharField(blank=True, max_length=64)),
                ('industry_type', models.CharField(blank=True, max_length=64)),
                ('city', models.CharField(blank=True, max_length=32)),
                ('state', models.CharField(blank=True, max_length=32)),
                ('country', models.CharField(blank=True, max_length=32)),
                ('zip_code', models.IntegerField(blank=True)),
                ('assigned_campaign', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='portal.Campaign')),
            ],
        ),
        migrations.AddField(
            model_name='lead',
            name='prospect',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal.Prospect'),
        ),
        migrations.AddField(
            model_name='dnc',
            name='executive',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal.Executive'),
        ),
        migrations.AddField(
            model_name='dnc',
            name='prospect',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal.Prospect'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='executives',
            field=models.ManyToManyField(to='portal.Executive'),
        ),
        migrations.AlterUniqueTogether(
            name='lead',
            unique_together={('campaign', 'prospect')},
        ),
        migrations.AlterUniqueTogether(
            name='dnc',
            unique_together={('campaign', 'prospect')},
        ),
    ]
