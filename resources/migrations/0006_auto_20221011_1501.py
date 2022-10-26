# Generated by Django 3.2.16 on 2022-10-11 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0005_industry_job_resourcecategory_resourcetype'),
    ]

    operations = [
        migrations.AddField(
            model_name='resourceprovider',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='resourceseeker',
            name='core_business',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='resourceseeker',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='resourceseeker',
            name='org_head',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='resourceseeker',
            name='registered_year',
            field=models.CharField(blank=True, max_length=4),
        ),
        migrations.AddField(
            model_name='resourceseekerservices',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]