# Generated by Django 3.2.16 on 2022-10-18 04:49

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0007_auto_20221011_1507'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriptionPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('entity', models.CharField(blank=True, max_length=100, null=True)),
                ('amount', models.FloatField(blank=True, null=True)),
                ('currency', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.CharField(blank=True, max_length=20, null=True)),
                ('order_id', models.CharField(blank=True, max_length=100, null=True)),
                ('invoice_id', models.CharField(blank=True, max_length=100, null=True)),
                ('international', models.BooleanField(default=False)),
                ('method', models.CharField(blank=True, max_length=100, null=True)),
                ('amount_refunded', models.FloatField(blank=True, null=True)),
                ('refund_status', models.CharField(blank=True, max_length=100, null=True)),
                ('captured', models.BooleanField(default=False)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('card_id', models.CharField(blank=True, max_length=100, null=True)),
                ('card_entity', models.CharField(blank=True, max_length=100, null=True)),
                ('card_name', models.CharField(blank=True, max_length=100, null=True)),
                ('card_last4', models.CharField(blank=True, max_length=100, null=True)),
                ('card_network', models.CharField(blank=True, max_length=100, null=True)),
                ('card_type', models.CharField(blank=True, max_length=100, null=True)),
                ('card_issuer', models.CharField(blank=True, max_length=100, null=True)),
                ('card_international', models.BooleanField(default=False)),
                ('card_emi', models.BooleanField(default=False)),
                ('card_sub_type', models.CharField(blank=True, max_length=100, null=True)),
                ('bank', models.CharField(blank=True, max_length=100, null=True)),
                ('wallet', models.CharField(blank=True, max_length=100, null=True)),
                ('vpa', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.CharField(blank=True, max_length=100, null=True)),
                ('contact', models.CharField(blank=True, max_length=100, null=True)),
                ('notes', models.CharField(blank=True, max_length=100, null=True)),
                ('fee', models.FloatField(blank=True, null=True)),
                ('tax', models.FloatField(blank=True, null=True)),
                ('error_code', models.CharField(blank=True, max_length=100, null=True)),
                ('error_description', models.CharField(blank=True, max_length=500, null=True)),
                ('error_source', models.CharField(blank=True, max_length=500, null=True)),
                ('error_step', models.CharField(blank=True, max_length=500, null=True)),
                ('error_reason', models.CharField(blank=True, max_length=500, null=True)),
                ('created_at', models.DateTimeField(blank=True)),
                ('amount_unit', models.CharField(blank=True, choices=[('paise', 'Paise'), ('rupee', 'Rupee')], max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubscriptionPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_name', models.CharField(blank=True, max_length=100, null=True)),
                ('plan_code', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('plan_duration', models.CharField(blank=True, choices=[('monthly', 'Monthly'), ('quarterly', 'Quarterly'), ('semiannual', 'Semi-Annual'), ('annual', 'Annual')], max_length=20, null=True)),
                ('plan_category', models.CharField(blank=True, choices=[('individual', 'Individual'), ('institutional', 'Institutional')], max_length=20, null=True)),
                ('plan_amount', models.FloatField(blank=True, null=True)),
                ('tax', models.FloatField(blank=True, null=True)),
                ('currency', models.CharField(blank=True, max_length=100, null=True)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterField(
            model_name='resourceprovider',
            name='alternate_phone_number',
            field=models.CharField(max_length=255, validators=[django.core.validators.RegexValidator(message='Invalid phone number entered.', regex='^\\+?1?\\d{0,12}$')]),
        ),
        migrations.AlterField(
            model_name='resourceprovider',
            name='phone_number',
            field=models.CharField(max_length=255, validators=[django.core.validators.RegexValidator(message='Invalid phone number entered.', regex='^\\+?1?\\d{0,12}$')]),
        ),
        migrations.AlterField(
            model_name='resourceseeker',
            name='alternate_phone_number',
            field=models.CharField(max_length=255, validators=[django.core.validators.RegexValidator(message='Invalid phone number entered.', regex='^\\+?1?\\d{0,12}$')]),
        ),
        migrations.AlterField(
            model_name='resourceseeker',
            name='phone_number',
            field=models.CharField(max_length=255, validators=[django.core.validators.RegexValidator(message='Invalid phone number entered.', regex='^\\+?1?\\d{0,12}$')]),
        ),
        migrations.AlterField(
            model_name='resourceseekerservices',
            name='alternate_phone_number',
            field=models.CharField(max_length=255, validators=[django.core.validators.RegexValidator(message='Invalid phone number entered.', regex='^\\+?1?\\d{0,12}$')]),
        ),
        migrations.AlterField(
            model_name='resourceseekerservices',
            name='phone_number',
            field=models.CharField(max_length=255, validators=[django.core.validators.RegexValidator(message='Invalid phone number entered.', regex='^\\+?1?\\d{0,12}$')]),
        ),
        migrations.CreateModel(
            name='UserSubscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_expired', models.BooleanField(blank=True, default=False, null=True)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_newly_registered', models.BooleanField(default=False)),
                ('plan_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subscription_plan_id', to='resources.subscriptionplan')),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_subscription_id', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SubscriptionOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('amount', models.FloatField(blank=True, null=True)),
                ('currency', models.CharField(blank=True, max_length=100, null=True)),
                ('amount_unit', models.CharField(blank=True, choices=[('paise', 'Paise'), ('rupee', 'Rupee')], max_length=100, null=True)),
                ('status', models.CharField(blank=True, choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')], max_length=20, null=True)),
                ('created_at', models.DateTimeField(blank=True)),
                ('updated_at', models.DateTimeField(blank=True)),
                ('order_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subscription_order_order_by', to=settings.AUTH_USER_MODEL)),
                ('plan_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subscription_plan_order_plan_id', to='resources.subscriptionplan')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subscription_order_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]