from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


import os
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timezone import now as timezone_now
from .manager import MyuserManager
from django.contrib.auth.models import Group
#from django.contrib.auth.base_user import BaseUserManager
#from django.contrib.auth.models import PermissionsMixin


class User(AbstractUser):
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]
    EMAIL_FIELD = "email"
    USERNAME_FIELD = 'email'

    objects = MyuserManager()

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
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
    phone_number = models.CharField(max_length=255, blank=False, null=False)
    alternate_phone_number = models.CharField(max_length=255, blank=False, null=False)
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

class ResourceSeekerServices(GeneralProfile):
    person_id = None