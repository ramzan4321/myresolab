from dataclasses import fields
import email
from unicodedata import category
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework.exceptions import ValidationError
from django.core.validators import RegexValidator
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from rest_framework.status import HTTP_422_UNPROCESSABLE_ENTITY, HTTP_406_NOT_ACCEPTABLE
from resources.models import ResourceProvider, ResourceSeeker , ResourceSeekerServices, SubscriptionOrder, SubscriptionPayment,SubscriptionPlan,UserSubscription

User = get_user_model()

phone_regex = RegexValidator(regex=r'^\+?1?\d{0,12}$',  message="Invalid phone number entered.")

class UserSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(validators=[phone_regex], max_length=13)
    class Meta:
        model = User
        exclude = ['is_active','is_superuser','is_admin','is_staff','user_permissions']

    def validate(self, data):
        if User.objects.filter(username=data['email']).exists():
            print(User.objects.get(username=data['email']))
            raise ValidationError('This Email is already registered!', HTTP_406_NOT_ACCEPTABLE)
        if len(data['phone']) >= 14:
            raise ValidationError('Phone Number not valid!', HTTP_406_NOT_ACCEPTABLE)
        if User.objects.filter(phone=data['phone']).exists():
            print(User.objects.get(phone=data['phone']))
            raise ValidationError('This phone number is already registered!', HTTP_406_NOT_ACCEPTABLE)
        return data


class ProviderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceProvider
        exclude = ['is_active','is_superuser','is_admin','is_staff','user_permissions']
    def validate(self, data):
        if len(data['phone']) >= 14:
            raise ValidationError('Phone Number not valid!', HTTP_406_NOT_ACCEPTABLE)
        return data
    def update(self, instance, validated_data):
        instance.save()
        return instance


class SeekerUpdateSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(validators=[phone_regex], max_length=13)
    industry_type = serializers.CharField()
    state = serializers.CharField()
    city = serializers.CharField()
    image = serializers.ImageField()
    category = serializers.CharField()
    class Meta:
        model = ResourceSeeker
        exclude = ['is_active','is_superuser','is_admin','is_staff','user_permissions']
    def validate(self, data):
        if len(data['phone']) >= 14:
            raise ValidationError('Phone Number not valid!', HTTP_406_NOT_ACCEPTABLE)
        return data
    def update(self, instance, validated_data):
        instance.phone = validated_data.get('phone',instance.phone)
        instance.industry_type = validated_data.get('industry_type',instance.industry_type)
        instance.state = validated_data.get('state',instance.state)
        instance.city = validated_data.get('city',instance.city)
        instance.category = validated_data.get('category',instance.category)
        instance.image = validated_data.get('image',instance.image)
        instance.save()
        return instance


class UserUpdateSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(validators=[phone_regex], max_length=13)
    industry_type = serializers.CharField()
    state = serializers.CharField()
    city = serializers.CharField()
    image = serializers.ImageField()
    category = serializers.CharField()
    class Meta:
        model = User
        exclude = ['is_active','is_superuser','is_admin','is_staff','user_permissions']
    def validate(self, data):
        if len(data['phone']) >= 14:
            raise ValidationError('Phone Number not valid!', HTTP_406_NOT_ACCEPTABLE)
        return data
    def update(self, instance, validated_data):
        instance.phone = validated_data.get('phone',instance.phone)
        instance.industry_type = validated_data.get('industry_type',instance.industry_type)
        instance.state = validated_data.get('state',instance.state)
        instance.city = validated_data.get('city',instance.city)
        instance.category = validated_data.get('category',instance.category)
        instance.image = validated_data.get('image',instance.image)
        instance.save()
        return instance


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    class Meta:
        model = User
        fields = ['email','password']


    '''id_token = serializers.CharField(max_length=2400)
    def validate(self, data):
        try:
            jwt = auth.verify_id_token(data['id_token'])
            log.info(User.objects)
            try:
                user = User.objects.get(username=jwt['uid'])
            except User.DoesNotExist:
                raise ValidationError('This number is not registered. First register to login!', HTTP_406_NOT_ACCEPTABLE)
        except (ValueError, InvalidIdTokenError):
            raise ValidationError('Invalid Firebase ID Token', HTTP_422_UNPROCESSABLE_ENTITY)
        return data

    def get_token_and_user(self):
        id_token = self.data['id_token']
        jwt = auth.verify_id_token(id_token)
        user = User.objects.get(username=jwt['uid'])
        token, created = Token.objects.get_or_create(user=user)
        user_profile = user.userprofile
        return str(token), user_profile
'''

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['image','email']


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceProvider
        exclude = ['user','is_user_active']



class ProviderCardCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceProvider
        exclude = ['user','is_user_active','user_id','id']

class ProviderCardViewSerializer(serializers.ModelSerializer):
    user = ImageSerializer(read_only = True)
    class Meta:
        model = ResourceProvider
        fields = ['user_id','location_state', 'address', 'user', 'job_role', 'organization_name', 'is_user_active','min_salary', 'max_salary','make_into_as_public']

class SeekerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceSeeker
        exclude = ['user','is_user_active']


class SeekerSerializerCardView(serializers.ModelSerializer):
    user = ImageSerializer(read_only = True)
    class Meta:
        model = ResourceSeeker
        fields = ['user_id','location_state', 'address', 'user', 'job_role', 'organization_name', 'is_user_active','min_salary', 'max_salary','make_into_as_public']


class SeekerServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceSeekerServices
        exclude = ['user','is_user_active']



#--------------------------------Payment Gateway Integration-----------------------------------

class CheckoutSubscriptionDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = ('__all__')


class SubscriptionOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionOrder
        fields = ('__all__')


class SubscriptionPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPayment
        fields = ('__all__')
        
class UserSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubscription
        fields = ('__all__')
