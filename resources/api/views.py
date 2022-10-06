import email
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

from rest_framework.generics import ListAPIView,ListCreateAPIView,CreateAPIView, RetrieveUpdateDestroyAPIView

from resources.models import ResourceSeeker, ResourceSeekerServices
from .serializers import UserSerializer , SeekerSerializer , SeekerServiceSerializer

User = get_user_model()

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