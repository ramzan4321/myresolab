# Generated by Django 3.2.16 on 2022-10-07 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0003_remove_user_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='city',
            field=models.CharField(default='Kanpur', max_length=100),
        ),
    ]