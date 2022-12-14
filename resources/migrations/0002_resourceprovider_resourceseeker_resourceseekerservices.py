# Generated by Django 3.2.16 on 2022-10-06 06:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResourceSeekerServices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('citizenship', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('location_state', models.CharField(max_length=255)),
                ('location_district', models.CharField(max_length=255)),
                ('min_salary', models.IntegerField()),
                ('max_salary', models.IntegerField()),
                ('phone_number', models.CharField(max_length=255)),
                ('alternate_phone_number', models.CharField(max_length=255)),
                ('is_user_active', models.BooleanField(default=True)),
                ('make_into_as_public', models.TextField(blank=True, null=True)),
                ('organization_name', models.CharField(max_length=255)),
                ('legal_status', models.CharField(max_length=255)),
                ('select_category', models.CharField(max_length=255)),
                ('person_name', models.CharField(max_length=255)),
                ('person_designation', models.CharField(max_length=255)),
                ('person_email', models.EmailField(max_length=254)),
                ('manager_name', models.CharField(max_length=255)),
                ('manager_designation', models.CharField(max_length=255)),
                ('manager_email', models.EmailField(max_length=254)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ResourceSeeker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('citizenship', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('location_state', models.CharField(max_length=255)),
                ('location_district', models.CharField(max_length=255)),
                ('min_salary', models.IntegerField()),
                ('max_salary', models.IntegerField()),
                ('phone_number', models.CharField(max_length=255)),
                ('alternate_phone_number', models.CharField(max_length=255)),
                ('is_user_active', models.BooleanField(default=True)),
                ('make_into_as_public', models.TextField(blank=True, null=True)),
                ('organization_name', models.CharField(max_length=255)),
                ('legal_status', models.CharField(max_length=255)),
                ('select_category', models.CharField(max_length=255)),
                ('person_name', models.CharField(max_length=255)),
                ('person_designation', models.CharField(max_length=255)),
                ('person_id', models.CharField(max_length=255)),
                ('person_email', models.EmailField(max_length=254)),
                ('manager_name', models.CharField(max_length=255)),
                ('manager_designation', models.CharField(max_length=255)),
                ('manager_email', models.EmailField(max_length=254)),
                ('job_role', models.CharField(max_length=255)),
                ('minimum_qualification', models.CharField(max_length=255)),
                ('preferred_qualification_if_any', models.CharField(max_length=255)),
                ('is_experience_required', models.BooleanField(default=False)),
                ('additional_requirement', models.CharField(max_length=255)),
                ('joining_requirements', models.CharField(max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ResourceProvider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('citizenship', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('location_state', models.CharField(max_length=255)),
                ('location_district', models.CharField(max_length=255)),
                ('min_salary', models.IntegerField()),
                ('max_salary', models.IntegerField()),
                ('phone_number', models.CharField(max_length=255)),
                ('alternate_phone_number', models.CharField(max_length=255)),
                ('is_user_active', models.BooleanField(default=True)),
                ('make_into_as_public', models.TextField(blank=True, null=True)),
                ('category_role', models.CharField(max_length=255)),
                ('job_role', models.CharField(max_length=255)),
                ('education_q', models.CharField(max_length=255)),
                ('degree', models.CharField(max_length=255)),
                ('achievements', models.CharField(max_length=255)),
                ('microfinance_exp', models.IntegerField()),
                ('other_exp', models.IntegerField()),
                ('first_Org_exp', models.IntegerField()),
                ('first_desig', models.CharField(max_length=70)),
                ('first_duration', models.CharField(max_length=70)),
                ('second_Org_exp', models.IntegerField()),
                ('second_desig', models.CharField(max_length=70)),
                ('second_duration', models.CharField(max_length=70)),
                ('third_Org_exp', models.IntegerField()),
                ('third_desig', models.CharField(max_length=70)),
                ('third_duration', models.CharField(max_length=70)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
