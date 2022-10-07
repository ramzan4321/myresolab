from dataclasses import fields
from django.contrib.auth import get_user_model
from rest_framework import serializers
from resources.models import ResourceProvider, ResourceSeeker , ResourceSeekerServices

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['is_active','is_superuser','is_admin','is_staff','user_permissions']


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceProvider
        exclude = ['user','is_user_active']



class ProviderCardCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceProvider
        exclude = ['user','is_user_active']

class ProviderCardViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceProvider
        fields = ['location_state', 'address', 'user', 'job_role', 'organization_name', 'is_user_active','min_salary', 'max_salary','make_into_as_public']

class SeekerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceSeeker
        exclude = ['user','is_user_active']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['image','email']


class SeekerSerializerCardView(serializers.ModelSerializer):
    user = ImageSerializer(read_only = True)
    class Meta:
        model = ResourceSeeker
        fields = ['location_state', 'address', 'user', 'job_role', 'organization_name', 'is_user_active','min_salary', 'max_salary','make_into_as_public']


class SeekerServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceSeekerServices
        exclude = ['user','is_user_active']

      #  extra_kwargs = {
       #     "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        #}
