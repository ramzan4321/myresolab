from dataclasses import fields
import email
from unicodedata import category
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework.exceptions import ValidationError
from django.core.validators import RegexValidator
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from django.utils.encoding import smart_str, force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
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


#---------------------------------- Password Changed / Reset -------------------------------------------

class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255,style={'input_type' : 'password'},write_only=True)
    password2 = serializers.CharField(max_length=255,style={'input_type' : 'password2'},write_only=True)
    class Meta:
        fields = ['password', 'password2']
        
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        print(user)
        if password != password2:
            raise ValidationError("password and password2 does not match")
        user.set_password(password)
        user.save()
        return super().validate(attrs)


class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        fields = ['email']
        
    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print('Encoded UID:',uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('Password Reset Token:',token)
            link = 'http://localhost:8000/api/user/reset-password/'+uid+'/'+token
            print('Password Reset Link:',link)
            
            #send email
            body = 'Click Following Link to Reset Your Password'+link
            data = {
                'subject': 'Reset Your Password',
                'body': body,
                'to_email': user.email,
            }
            return attrs
        else:
            raise ValidationError('You are not a Registered User')


class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255,style={'input_type' : 'password'},write_only=True)
    password2 = serializers.CharField(max_length=255,style={'input_type' : 'password2'},write_only=True)
    class Meta:
        fields = ['password', 'password2']
        
    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise ValidationError("The Password and Confirmed Password does not match")
            id = smart_str( urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise ValidationError("Token is not Valid or Expired")
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            uid = self.context.get('uid')
            token = self.context.get('token')
            id = smart_str( urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            PasswordResetTokenGenerator().check_token(user,token)
            raise ValidationError("Token is not Valid or Expired")
