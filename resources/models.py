from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


import os
from django.db import models
from django.utils import timezone
from django.utils.timezone import now as timezone_now
from .manager import MyuserManager
from django.contrib.auth.models import Group
from django.core.validators import RegexValidator
#from django.contrib.auth.base_user import BaseUserManager
#from django.contrib.auth.models import PermissionsMixin

phone_regex = RegexValidator(regex=r'^\+?1?\d{0,12}$',  message="Invalid phone number entered.")

class User(AbstractUser):
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]
    EMAIL_FIELD = "email"
    USERNAME_FIELD = 'email'

    objects = MyuserManager()

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    phone = models.CharField(unique=True,validators=[phone_regex], max_length=17,blank=True)
    #name = CharField(_("Name of User"), blank=True, max_length=255)
    image = models.ImageField(upload_to = 'images',default='images/default_image.jpg')
    industry_type = models.CharField(max_length=100,default="Microfinance")
    category = models.CharField(max_length=100,default="Resource Provider")
    state = models.CharField(max_length=100,default='Gujarat')
    city = models.CharField(max_length=100,default='Kanpur')
    date_of_birth = models.DateField(null=False,blank=False,default='2001-01-01')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="my_user",default="1")
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_recruiter = models.BooleanField(default=False)
    is_candidate = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.email)
    def has_perm(self, perm, obj=None):
        return self.is_admin
    def has_module_perms(self, app_label):
        return self.is_staff


class GeneralProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    citizenship = models.CharField(max_length=255, blank=False, null=False)
    address = models.CharField(max_length=255, blank=False, null=False)
    location_state = models.CharField(max_length=255, blank=False, null=False)
    location_district = models.CharField(max_length=255, blank=False, null=False)
    min_salary = models.IntegerField() # work as current_salary for ResourceProvider
    max_salary = models.IntegerField() # work as expected_salary for ResourceProvider
    phone_number = models.CharField(max_length=255,validators=[phone_regex], blank=False, null=False)
    alternate_phone_number = models.CharField(max_length=255,validators=[phone_regex], blank=False, null=False)
    is_user_active = models.BooleanField(default=True)
    make_into_as_public = models.TextField(null=True, blank=True) # work as description for ResourceProvide

    # About the organization
    organization_name = models.CharField(max_length=255, blank=False, null=False)
    legal_status = models.CharField(max_length=255, blank=False, null=False)
    select_category =models.CharField(max_length=255, blank=False, null=False)
    
    #Contact Details of Person posting Requirement
    person_name = models.CharField(max_length=255, blank=False, null=False)
    person_designation = models.CharField(max_length=255, blank=False, null=False)
    person_id = models.CharField(max_length=255, blank=False, null=False)
    #person_contact = phone_number
    person_email = models.EmailField()
    #Alternate Person Contact Details
    manager_name =models.CharField(max_length=255, blank=False, null=False)
    manager_designation =models.CharField(max_length=255, blank=False, null=False)
    #manager_contact = alternate_phone_number
    manager_email = models.EmailField()
    is_verified = models.BooleanField(default=False)

    class Meta:
       abstract = True

class ResourceProvider(GeneralProfile):
    category_role = models.CharField(max_length=255, blank=False, null=False)
    job_role = models.CharField(max_length=255, blank=False, null=False)
    education_q = models.CharField(max_length=255, blank=False, null=False)
    degree = models.CharField(max_length=255, blank=False, null=False)

    achievements = models.CharField(max_length=255, blank=False, null=False)

    microfinance_exp = models.IntegerField()
    other_exp = models.IntegerField()
    first_Org_exp = models.IntegerField()
    first_desig = models.CharField(max_length=70, blank=False, null=False)
    first_duration = models.CharField(max_length=70, blank=False, null=False)
    second_Org_exp = models.IntegerField()
    second_desig = models.CharField(max_length=70, blank=False, null=False)
    second_duration = models.CharField(max_length=70, blank=False, null=False)
    third_Org_exp = models.IntegerField()
    third_desig = models.CharField(max_length=70, blank=False, null=False)
    third_duration = models.CharField(max_length=70, blank=False, null=False)

    docs_urls_1 = models.TextField(blank=True)
    doc_name_1 = models.CharField(blank=True, max_length=100)
    verified_1= models.BooleanField(default=False)
    docs_urls_2 = models.TextField(blank=True)
    doc_name_2 = models.CharField(blank=True, max_length=100)
    verified_2= models.BooleanField(default=False)
    docs_urls_3 = models.TextField(blank=True)
    doc_name_3 = models.CharField(blank=True, max_length=100)
    verified_3= models.BooleanField(default=False)
    docs_urls_4 = models.TextField(blank=True)
    doc_name_4 = models.CharField(blank=True, max_length=100)
    verified_4= models.BooleanField(default=False)
    docs_urls_5 = models.TextField(blank=True)
    doc_name_5 = models.CharField(blank=True, max_length=100)  
    verified_5= models.BooleanField(default=False)
    docs_urls_6 = models.TextField(blank=True)
    doc_name_6 = models.CharField(blank=True, max_length=100)  
    verified_6= models.BooleanField(default=False)
    docs_urls_7 = models.TextField(blank=True)
    doc_name_7 = models.CharField(blank=True, max_length=100)  
    verified_7= models.BooleanField(default=False)
    docs_urls_8 = models.TextField(blank=True)
    doc_name_8 = models.CharField(blank=True, max_length=100)  
    verified_8= models.BooleanField(default=False)
    docs_urls_9 = models.TextField(blank=True)
    doc_name_9 = models.CharField(blank=True, max_length=100)  
    verified_9= models.BooleanField(default=False)
    docs_urls_10 = models.TextField(blank=True)
    doc_name_10 = models.CharField(blank=True, max_length=100)  
    verified_10= models.BooleanField(default=False)


    organization_name = None
    legal_status = None
    person_contact = None
    person_designation = None
    person_email = None
    person_name = None
    person_id = None
    manager_contact = None
    manager_designation = None
    manager_email = None
    manager_name = None
    select_category = None


class ResourceSeeker(GeneralProfile):
    #Resource Required Summary
    job_role =models.CharField(max_length=255, blank=False, null=False)
    minimum_qualification =models.CharField(max_length=255, blank=False, null=False)
    preferred_qualification_if_any =models.CharField(max_length=255, blank=False, null=False)
    is_experience_required =models.BooleanField(default=False)
    additional_requirement =models.CharField(max_length=255, blank=False, null=False)
    joining_requirements =models.CharField(max_length=255, blank=False, null=False)

    core_business= models.CharField(max_length=200, blank=True)
    registered_year=models.CharField(max_length=4, blank=True)
    org_head= models.CharField(max_length=200, blank=True)



class ResourceSeekerServices(GeneralProfile):
    person_id = None



class Industry(models.Model):
    industry_name = models.CharField(unique=True, max_length=120)

    def __str__(self):
        return self.industry_name

class ResourceType(models.Model):
    industry = models.ForeignKey(Industry, related_name='types',on_delete=models.CASCADE)
    type_name = models.CharField(max_length=120)

    def __str__(self):
        return self.type_name

class ResourceCategory(models.Model):
    resource_type = models.ForeignKey(ResourceType, related_name='categories', on_delete=models.CASCADE)
    category_name = models.CharField(max_length=120)

    def __str__(self):
        return self.category_name

class Job(models.Model):
    category = models.ForeignKey(ResourceCategory, related_name='jobs', on_delete=models.CASCADE)
    job_name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.job_name





class SubscriptionPlan(models.Model):
    DURATION = (
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('semiannual', 'Semi-Annual'),
        ('annual', 'Annual'),
    )
    CATEGORY = (
        ('individual', 'Individual'),
        ('institutional', 'Institutional')
    )
    plan_name = models.CharField(max_length=100 , blank=True , null=True)
    plan_code = models.CharField(max_length=100 , unique=True , blank=True , null=True)
    plan_duration = models.CharField(choices=DURATION , max_length=20, null=True , blank=True)
    plan_category = models.CharField(choices=CATEGORY , max_length=20 , null=True , blank=True)
    plan_amount = models.FloatField(null=True , blank=True)
    tax = models.FloatField(null=True , blank=True)
    currency = models.CharField(max_length=100 , blank=True , null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=False , auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True , auto_now_add=False)
    
    def __str__(self):
        return self.plan_name

class UserSubscription(models.Model):
    plan_id = models.ForeignKey(SubscriptionPlan , related_name="subscription_plan_id", blank=True , null=True , on_delete=models.CASCADE)
    user_id = models.ForeignKey(User , related_name="user_subscription_id", blank=True , null=True , on_delete=models.CASCADE)    
    is_expired = models.BooleanField(default=False ,blank=True , null=True)
    start_date = models.DateTimeField(blank=True , null=True)
    end_date = models.DateTimeField(blank=True , null=True)
    created_at = models.DateTimeField(auto_now=False , auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True , auto_now_add=False)
    is_newly_registered = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.plan_id)


class SubscriptionOrder(models.Model):
    STATUS = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled')
    )
    AMOUNT_UNIT = (
        ('paise', 'Paise'),
        ('rupee', 'Rupee')
    )
    order_id = models.CharField(max_length=100 , blank=True , null=True, unique=True)
    plan_id = models.ForeignKey(SubscriptionPlan, related_name='subscription_plan_order_plan_id', 
        blank=True, null=True, on_delete=models.CASCADE)
    amount = models.FloatField(null=True , blank=True)
    currency = models.CharField(max_length=100 , blank=True , null=True)
    amount_unit = models.CharField(choices=AMOUNT_UNIT, max_length=100 , blank=True , null=True)
    status = models.CharField(choices=STATUS, max_length=20, null=True, blank=True)
    order_by = models.ForeignKey(User , related_name="subscription_order_order_by", 
        blank=True , null=True , on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=False , blank=True)
    updated_at = models.DateTimeField(blank=True , auto_now_add=False)
    updated_by = models.ForeignKey(User , related_name="subscription_order_updated_by", 
        blank=True , null=True , on_delete=models.CASCADE)

    def __str__(self):
        return str(self.order_id)


class SubscriptionPayment(models.Model):
    AMOUNT_UNIT = (
        ('paise', 'Paise'),
        ('rupee', 'Rupee')
    )
    
    payment_id = models.CharField(max_length=100 , blank=True , null=True, unique=True)
    entity = models.CharField(max_length=100 , blank=True , null=True)
    amount = models.FloatField(null=True , blank=True)
    currency = models.CharField(max_length=100 , blank=True , null=True)
    status = models.CharField(max_length=20, null=True, blank=True)
    order_id = models.CharField(max_length=100 , blank=True , null=True)
    invoice_id = models.CharField(max_length=100 , blank=True , null=True)
    international = models.BooleanField(default=False)
    method = models.CharField(max_length=100 , blank=True , null=True)
    amount_refunded = models.FloatField(null=True , blank=True)
    refund_status = models.CharField(max_length=100 , blank=True , null=True)
    captured = models.BooleanField(default=False)
    description = models.CharField(max_length=100 , blank=True , null=True)
    card_id = models.CharField(max_length=100 , blank=True , null=True)
    card_entity = models.CharField(max_length=100 , blank=True , null=True)
    card_name = models.CharField(max_length=100 , blank=True , null=True)
    card_last4 = models.CharField(max_length=100 , blank=True , null=True)
    card_network = models.CharField(max_length=100 , blank=True , null=True)
    card_type = models.CharField(max_length=100 , blank=True , null=True)
    card_issuer = models.CharField(max_length=100 , blank=True , null=True)
    card_international = models.BooleanField(default=False)
    card_emi = models.BooleanField(default=False)
    card_sub_type = models.CharField(max_length=100 , blank=True , null=True)
    bank = models.CharField(max_length=100 , blank=True , null=True)
    wallet = models.CharField(max_length=100 , blank=True , null=True)
    vpa = models.CharField(max_length=100 , blank=True , null=True)
    email = models.CharField(max_length=100 , blank=True , null=True)
    contact = models.CharField(max_length=100 , blank=True , null=True)
    notes = models.CharField(max_length=100 , blank=True , null=True)
    fee = models.FloatField(null=True , blank=True)
    tax = models.FloatField(null=True , blank=True)
    error_code = models.CharField(max_length=100 , blank=True , null=True)
    error_description = models.CharField(max_length=500 , blank=True , null=True)
    error_source = models.CharField(max_length=500 , blank=True , null=True)
    error_step = models.CharField(max_length=500 , blank=True , null=True)
    error_reason = models.CharField(max_length=500 , blank=True , null=True)
    created_at = models.DateTimeField(auto_now=False , blank=True)
    amount_unit = models.CharField(choices=AMOUNT_UNIT, max_length=100 , blank=True , null=True)
