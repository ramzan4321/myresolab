import email
import io
from functools import partial
import socket, requests ,geocoder,json
from isort import stream
from django.http import HttpResponse
from urllib import response
from itertools import chain
from urllib.request import urlopen
from telnetlib import AUTHENTICATION
from django.contrib.auth import get_user_model
from django.urls import path , include
from django.contrib import admin
from django.contrib.auth import authenticate
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_422_UNPROCESSABLE_ENTITY, HTTP_406_NOT_ACCEPTABLE
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Q
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import UpdateAPIView ,ListAPIView,ListCreateAPIView,CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from yaml import serialize
from resources.renderers import MyRenderer
from resources.models import ResourceProvider, ResourceSeeker, ResourceSeekerServices
from .serializers import UserPasswordResetSerializer, SendPasswordResetEmailSerializer, UserChangePasswordSerializer, UserUpdateSerializer, LoginSerializer, ProviderSerializer, UserSerializer , SeekerSerializer , SeekerServiceSerializer, SeekerSerializerCardView, ProviderCardViewSerializer, ProviderCardCreateSerializer

User = get_user_model()

'''hostname = socket.gethostname()    
IPAddr = socket.gethostbyname(hostname)
response = requests.get('https://api64.ipify.org?format=json').json()
ip = response["ip"]
res = requests.get(f'https://ipapi.co/{ip}/json/').json()
GeoIp = geocoder.ip("me")
print(GeoIp.city)
print(GeoIp.state)
print(res['ip'])
print(res['city'])
print(res['region'])
'''

class AdminUserListCreate(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


'''
# Authentication and User
class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        self.serializer = self.get_serializer(data=request.data)
        self.serializer.is_valid(raise_exception=True)
        
        self.serializer.save()
        user = UserProfile.objects.get(email=self.serializer.data.get('email'))
        user_subscription_free_trial = UserSubscription.objects.create(
            user_id = user,
            start_date = datetime.now(),
            end_date = datetime.now() + timedelta(days=30),
            is_newly_registered=True
        )
        
        return Response({
            'response': 'User Registered!'
        }, HTTP_200_OK)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        try:
            self.serializer = self.get_serializer(data=request.data)
            self.serializer.is_valid(raise_exception=True)
            token, user_profile = self.serializer.get_token_and_user()
            return Response({
                'token': token,
                'user_profile': UserProfileSerializer(user_profile).data
            }, HTTP_200_OK)
        except Exception as error:
            return Response({'error': str(error)}, 401)
'''

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


### We Register New User Here

class RegisterNewUser(ListCreateAPIView):
    authentication_classes = []
    permission_classes = []
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def perform_create(self, serializer):
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(email=user)


### After SignUP or SignIn User Land on this API

class UserList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def get_queryset(self):
        """
        This view should return a list of all the information
        for the currently authenticated user.
        """
        user = self.request.user
        return User.objects.filter(email=user)


class UserLoginView(APIView):
    authentication_classes = []
    permission_classes = []
    renderer_classes = [MyRenderer]
    def post(self,request,format=None):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                access_token = token['access']
                gets = requests.get("http://127.0.0.1:8000/api/users/", headers={"Authorization": "Bearer "+access_token})
                strings = gets.json()
                return Response({'data':strings,'token':token})


### User can update, retrieve and delete with this API

class UserRetrieveDestroyUpdate(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer

    def put(self,request,format=None,pk=None):
        if request.method == 'PUT':
            json_data = request.body
            stream = io.BytesIO(json_data)
            python_data = JSONParser().parse(stream)
            if 'phone' not in python_data:
                getphone = User.objects.filter(id=pk).values('phone')
                python_data.update(getphone[0])
                print(python_data)
            user = self.request.user
            query = User.objects.get(email=user) 
            serializer = UserUpdateSerializer(query,data=python_data,partial=True)
            if serializer.is_valid():
                serializer.save()
                res =  {'msg':'Data Updated Successfully!'}
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data,content_type='application/json')
            json_data = JSONRenderer().render(serializer.errors)
            return HttpResponse(json_data,content_type='application/json')

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(email=user)


class SeekerRetrieveDestroyUpdate(RetrieveUpdateDestroyAPIView):
    queryset = ResourceSeeker.objects.all()
    serializer_class = SeekerSerializer

    def put(self,request,format=None,pk=None):
        if request.method == 'PUT':
            json_data = request.body
            stream = io.BytesIO(json_data)
            python_data = JSONParser().parse(stream)
            print(python_data)
            user = self.request.user
            query = ResourceSeeker.objects.get(user_id=user) 
            serializer = SeekerSerializer(query,data=python_data,partial=True)
            if serializer.is_valid():
                serializer.save()
                res =  {'msg':'Data Updated Successfully!'}
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data,content_type='application/json')
            json_data = JSONRenderer().render(serializer.errors)
            return HttpResponse(json_data,content_type='application/json')

    def get_queryset(self):
        user = self.request.user
        return ResourceSeeker.objects.filter(user_id=user)


class ProviderRetrieveDestroyUpdate(RetrieveUpdateDestroyAPIView):
    queryset = ResourceProvider.objects.all()
    serializer_class = ProviderSerializer

    def put(self,request,format=None,pk=None):
        if request.method == 'PUT':
            json_data = request.body
            stream = io.BytesIO(json_data)
            python_data = JSONParser().parse(stream)
            user = self.request.user
            query = ResourceProvider.objects.get(user_id=user) 
            serializer = ProviderSerializer(query,data=python_data,partial=True)
            if serializer.is_valid():
                serializer.save()
                res =  {'msg':'Data Updated Successfully!'}
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data,content_type='application/json')
            json_data = JSONRenderer().render(serializer.errors)
            return HttpResponse(json_data,content_type='application/json')

    def get_queryset(self):
        user = self.request.user
        return ResourceProvider.objects.filter(user_id=user)


### Here User can create their card for Resource Provider

class ProviderCardCreate(ListCreateAPIView):
    queryset = ResourceProvider.objects.all()
    serializer_class = ProviderCardCreateSerializer

    def get_queryset(self):
        user = self.request.user
        candidate = User.objects.get(email=user)
        if candidate.is_candidate == True:
            return ResourceProvider.objects.filter(user_id=user)
        else:
            raise AuthenticationFailed('Only Candidate are elegible for resource providing')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

### Admin verified the Resource Provider & Seeker Card

class IsVerifiedProvider(ListAPIView):
    queryset = ResourceProvider.objects.all()
    serializer_class = ProviderSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous != True and (user.is_admin == True or user.is_staff == True or user.is_superuser == True):
            query = ResourceProvider.objects.get(id=self.kwargs['pk'])
            query.is_verified = True
            query.save()
            return ResourceProvider.objects.filter(pk=self.kwargs['pk'])
        else:
            return "Only Admin Access..."

class IsVerifiedSeeker(ListAPIView):
    queryset = ResourceSeeker.objects.all()
    serializer_class = SeekerSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous != True and (user.is_admin == True or user.is_staff == True or user.is_superuser == True):
            query = ResourceSeeker.objects.get(id=self.kwargs['pk'])
            query.is_verified = True
            query.save()
            return ResourceSeeker.objects.filter(pk=self.kwargs['pk'])
        else:
            return "Only Admin Access..."

class IsVerifiedProviderView(ListAPIView):
    queryset = ResourceProvider.objects.all()
    serializer_class = ProviderSerializer

    def get_queryset(self):
        user = self.request.user
        if ((user.is_anonymous != True) and (user.is_admin == True or user.is_staff == True or user.is_superuser == True)):
            query = ResourceProvider.objects.filter(is_verified=False)
            return query
        else:
            return "Only Admin Access..."

class IsVerifiedSeekerView(ListAPIView):
    queryset = ResourceSeeker.objects.all()
    serializer_class = SeekerSerializer

    def get_queryset(self):
        user = self.request.user
        if ((user.is_anonymous != True) and (user.is_admin == True or user.is_staff == True or user.is_superuser == True)):
            query = ResourceSeeker.objects.filter(is_verified=False)
            return query
        else:
            return "Only Admin Access..."

### Here User or Anyone can view Resource Provider List

class ProviderCardView(ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = ResourceProvider.objects.all()
    serializer_class = ProviderCardViewSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous != True:
            query = User.objects.filter(email=user).first()
            state = query.state
            chk = ResourceProvider.objects.filter(location_state = state)
            if not chk:
                GeoIp = geocoder.ip("me")
                state = GeoIp.state
            cate = query.category
            qs1 = ResourceProvider.objects.filter(is_verified = True,location_state = state, category_role=cate).all()
            qs2 = ResourceProvider.objects.filter(is_verified = True,location_state=state).exclude(location_state = state, category_role=cate)
            qs3 = ResourceProvider.objects.filter(is_verified = True).exclude(location_state = state)
            qs4 = chain(qs1,qs2,qs3)
            return qs4
        else:
            GeoIp = geocoder.ip("me")
            ipstate = GeoIp.state
            qs1 = ResourceProvider.objects.filter(is_verified = True,location_state = ipstate).all()
            qs2 = ResourceProvider.objects.filter(is_verified = True).exclude(location_state = ipstate)
            qs3 = chain(qs1,qs2)
            return qs3



### Here User can create their card for Resource Seeker in People category

class SeekerCardCreate(ListCreateAPIView):
    serializer_class = SeekerSerializer
    queryset = ResourceSeeker.objects.all()

    def get_queryset(self):
        user = self.request.user
        recruiter = User.objects.get(email=user)
        if recruiter.is_recruiter == True:
            return ResourceSeeker.objects.filter(user_id=user)
        else:
            raise AuthenticationFailed('Only Recruiter are elegible for job posting')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    
### Here User can create their card for Resource Seeker in Services category

class SeekerServicesCardCreate(ListCreateAPIView):
    queryset = ResourceSeekerServices.objects.all()
    serializer_class = SeekerServiceSerializer

    def get_queryset(self):
        user = self.request.user
        recruiter = User.objects.get(email=user)
        if recruiter.is_recruiter == True:
            return ResourceSeekerServices.objects.filter(user_id=user)
        else:
            raise AuthenticationFailed('Only Recruiter are elegible for job posting')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


### Here User or Anyone can view ResourceRequired List

class ResourceRequiredCardView(ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = ResourceSeeker.objects.select_related('user').all()
    serializer_class = SeekerSerializerCardView

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous != True:
            query = User.objects.filter(email=user).first()
            state = query.state
            chk = ResourceSeeker.objects.filter(location_state = state)
            if not chk:
                GeoIp = geocoder.ip("me")
                state = GeoIp.state
            cate = query.category
            qs1 = ResourceSeeker.objects.filter(location_state = state, select_category=cate).all()
            qs2 = ResourceSeeker.objects.filter(location_state=state).exclude(location_state = state, select_category=cate)
            qs3 = ResourceSeeker.objects.filter(is_verified = True).exclude(location_state = state)
            qs4 = chain(qs1,qs2,qs3)
            return qs4
        else:
            GeoIp = geocoder.ip("me")
            ipstate = GeoIp.state
            qs1 = ResourceSeeker.objects.filter(location_state = ipstate).all()
            qs2 = ResourceSeeker.objects.filter(is_verified = True).exclude(location_state = ipstate)
            qs3 = chain(qs1,qs2)
            return qs3


### Get further more details of Resource Provider by providing Id

class ProviderViewDetails(ListAPIView):
    queryset = ResourceProvider.objects.all()
    serializer_class = ProviderSerializer
    def get_queryset(self):
        return ResourceProvider.objects.filter(id=self.kwargs['pk'])


### Get further more details of Resource Seeker by providing Id

class SeekerViewDetails(ListAPIView):
    queryset = ResourceSeeker.objects.all()
    serializer_class = SeekerSerializer
    def get_queryset(self):
        return ResourceSeeker.objects.filter(id=self.kwargs['pk'])

### Here we do all type of data filteration on the basis of State , City , Category and Job role

class StateWiseProviderView(ListAPIView):
    queryset = ResourceSeeker.objects.all()
    serializer_class = SeekerSerializer
    def get_queryset(self):
        if 'state' and 'jobrole' in self.kwargs:
            return ResourceSeeker.objects.filter(location_state=self.kwargs['state'],job_role=self.kwargs['jobrole'])
        
        elif 'city' and 'jobrole' in self.kwargs:
            return ResourceSeeker.objects.filter(location_district=self.kwargs['city'],job_role=self.kwargs['jobrole'])

        elif 'state' and 'jobrole' in self.kwargs:
            return ResourceSeeker.objects.filter(location_state=self.kwargs['state'],job_role=self.kwargs['jobrole'])
        
        elif 'city' and 'category' and 'jobrole' in self.kwargs:
            return ResourceSeeker.objects.filter(location_district=self.kwargs['city'],select_category=self.kwargs['category'],job_role=self.kwargs['jobrole'])
        
        elif 'state' and 'category' and 'jobrole' in self.kwargs:
            return ResourceSeeker.objects.filter(location_state=self.kwargs['state'],select_category=self.kwargs['category'],job_role=self.kwargs['jobrole'])
        
        elif 'state' and 'city' and 'category' and 'jobrole'in self.kwargs:
            return ResourceSeeker.objects.filter(location_state=self.kwargs['state'],location_district=self.kwargs['city'],select_category=self.kwargs['category'],job_role=self.kwargs['jobrole'])
        
        else:
            return ResourceSeeker.objects.all()

    
class StateWiseRequiredView(ListAPIView):
    queryset = ResourceProvider.objects.all()
    serializer_class = ProviderSerializer
    def get_queryset(self):
        if 'state' and 'jobrole' in self.kwargs:
            return ResourceProvider.objects.filter(location_state=self.kwargs['state'],job_role=self.kwargs['jobrole'])

        elif 'city' and 'jobrole' in self.kwargs:
            return ResourceProvider.objects.filter(location_district=self.kwargs['city'],job_role=self.kwargs['jobrole'])
        
        elif 'city' and 'category' and 'jobrole' in self.kwargs:
            return ResourceProvider.objects.filter(location_district=self.kwargs['city'],category_role=self.kwargs['category'],job_role=self.kwargs['jobrole'])
        
        elif 'state' and 'category' and 'jobrole' in self.kwargs:
            return ResourceProvider.objects.filter(location_state=self.kwargs['state'],category_role=self.kwargs['category'],job_role=self.kwargs['jobrole'])
        
        elif 'state' and 'city' and 'category' and 'jobrole'in self.kwargs:
            return ResourceProvider.objects.filter(location_state=self.kwargs['state'],location_district=self.kwargs['city'],category_role=self.kwargs['category'],job_role=self.kwargs['jobrole'])
        
        else:
            return ResourceProvider.objects.all()

#--------------------------------------------------UserChangePasswordView----------------------------------------------------------

class UserChangePasswordView(APIView):
    renderer_classes = [MyRenderer]
    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(data = request.data,
        context={'user': request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password changed successfully'},status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class SendPasswordResetEmailView(APIView):
    authentication_classes = []
    permission_classes = []
    renderer_classes = [MyRenderer]
    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Reset link send. Please check your Email'},status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
    

class UserPasswordResetView(APIView):
    renderer_classes = [MyRenderer]
    permission_classes = []
    authentication_classes = []
    def post(self, request,uid,token, format=None):
        serializer = UserPasswordResetSerializer(data=request.data, context = {'uid':uid,'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Reset successfully'},status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        
    