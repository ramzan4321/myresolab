from django.contrib.auth import get_user_model
from rest_framework import serializers
from resources.models import ResourceSeeker , ResourceSeekerServices

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['is_active','is_superuser','is_admin','is_staff','user_permissions']


class SeekerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceSeeker
        exclude = ['user','is_user_active']


class SeekerServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceSeekerServices
        exclude = ['user','is_user_active']

      #  extra_kwargs = {
       #     "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        #}
