import email
import socket, requests ,geocoder
from itertools import chain
from urllib.request import urlopen
from telnetlib import AUTHENTICATION
from django.contrib.auth import get_user_model
from django.urls import path , include
from django.contrib import admin
from rest_framework import status , routers
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Q

from rest_framework.generics import ListAPIView,ListCreateAPIView,CreateAPIView, RetrieveUpdateDestroyAPIView

from resources.models import ResourceProvider, ResourceSeeker, ResourceSeekerServices
from .serializers import ProviderSerializer, UserSerializer , SeekerSerializer , SeekerServiceSerializer, SeekerSerializerCardView, ProviderCardViewSerializer, ProviderCardCreateSerializer

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

### User can update, retrieve and delete with this API

class UserRetrieveDestroyUpdate(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(email=user)


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
            cate = query.category
            qs1 = ResourceProvider.objects.filter(location_state = state, select_category=cate).all()
            qs2 = ResourceProvider.objects.filter(location_state=state).exclude(location_state = state, select_category=cate)
            qs3 = ResourceProvider.objects.all().exclude(location_state = state)
            qs4 = chain(qs1,qs2,qs3)
            return qs4
        else:
            GeoIp = geocoder.ip("me")
            ipstate = GeoIp.state
            qs1 = ResourceProvider.objects.filter(location_state = ipstate).all()
            qs2 = ResourceProvider.objects.all().exclude(location_state = ipstate)
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
    queryset = ResourceSeeker.objects.all()
    serializer_class = SeekerSerializerCardView

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous != True:
            query = User.objects.filter(email=user).first()
            state = query.state
            cate = query.category
            qs1 = ResourceSeeker.objects.filter(location_state = state, select_category=cate).all()
            qs2 = ResourceSeeker.objects.filter(location_state=state).exclude(location_state = state, select_category=cate)
            qs3 = ResourceSeeker.objects.all().exclude(location_state = state)
            qs4 = chain(qs1,qs2,qs3)
            return qs4
        else:
            GeoIp = geocoder.ip("me")
            ipstate = GeoIp.state
            qs1 = ResourceSeeker.objects.filter(location_state = ipstate).all()
            qs2 = ResourceSeeker.objects.all().exclude(location_state = ipstate)
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
        if 'state' in self.kwargs:
            return ResourceSeeker.objects.filter(location_state=self.kwargs['state'])

        elif 'city' in self.kwargs:
            return ResourceSeeker.objects.filter(location_district=self.kwargs['city'])

        elif 'category' in self.kwargs:
            return ResourceSeeker.objects.filter(select_category=self.kwargs['category'])

        elif 'jobrole' in self.kwargs:
            return ResourceSeeker.objects.filter(job_role=self.kwargs['jobrole'])

        elif 'city' and 'jobrole' in self.kwargs:
            return ResourceSeeker.objects.filter(location_district=self.kwargs['city'],job_role=self.kwargs['jobrole'])

        elif 'state' and 'jobrole' in self.kwargs:
            return ResourceSeeker.objects.filter(location_state=self.kwargs['state'],job_role=self.kwargs['jobrole'])
        
        elif 'category' and 'jobrole' in self.kwargs:
            return ResourceSeeker.objects.filter(select_category=self.kwargs['category'],job_role=self.kwargs['jobrole'])
        
        elif 'city' and 'category' in self.kwargs:
            return ResourceSeeker.objects.filter(location_district=self.kwargs['city'],select_category=self.kwargs['category'])
        
        elif 'state' and 'category' in self.kwargs:
            return ResourceSeeker.objects.filter(location_state=self.kwargs['state'],select_category=self.kwargs['category'])
        
        elif 'state' and 'city' in self.kwargs:
            return ResourceSeeker.objects.filter(location_state=self.kwargs['state'],location_district=self.kwargs['city'])
        
        elif 'state' and 'city' and 'category' in self.kwargs:
            return ResourceSeeker.objects.filter(location_state=self.kwargs['state'],location_district=self.kwargs['city'],select_category=self.kwargs['category'])
        
        elif 'city' and 'category' and 'jobrole' in self.kwargs:
            return ResourceSeeker.objects.filter(location_district=self.kwargs['city'],select_category=self.kwargs['category'],job_role=self.kwargs['jobrole'])
        
        elif 'state' and 'category' and 'jobrole' in self.kwargs:
            return ResourceSeeker.objects.filter(location_state=self.kwargs['state'],select_category=self.kwargs['category'],job_role=self.kwargs['jobrole'])
        
        elif 'state' and 'city' and 'category' and 'jobrole'in self.kwargs:
            return ResourceSeeker.objects.filter(location_state=self.kwargs['state'],location_district=self.kwargs['city'],select_category=self.kwargs['category'],job_role=self.kwargs['jobrole'])
        
        else:
            return ResourceSeeker.objects.all()
        