from pickle import TRUE
from tokenize import group
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

class MyuserManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, email, password=None):
        user = self.model(
            username = username, 
            first_name = first_name, 
            last_name = last_name, 
            email = self.normalize_email(email),
            )
        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, first_name, last_name, email, password=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            username = username, 
            first_name = first_name, 
            last_name = last_name,
            email = self.normalize_email(email),
            password=password,
        )
        user.save(using=self._db)
        return user