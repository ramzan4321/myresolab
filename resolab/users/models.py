'''from django.contrib.auth.models import AbstractUser
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
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin


class User(AbstractUser):
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]
    EMAIL_FIELD = "email"
    USERNAME_FIELD = 'email'

    objects = MyuserManager()

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    name = CharField(_("Name of User"), blank=True, max_length=255)
    image = models.ImageField(upload_to = 'images',default='images/default_image.jpg')
    industry_type = models.CharField(max_length=100,default="Microfinance")
    category = models.CharField(max_length=100,default="Resource Provider")
    state = models.CharField(max_length=100,default='Gujarat')
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

    
    """
    Default custom user model for Resolab.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    def get_absolute_url(self):
        Get url for user's detail view.

        Returns:
            str: URL for user detail.
        return reverse("users:detail", kwargs={"username": self.username})"""
'''