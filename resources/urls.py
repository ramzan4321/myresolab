from .api import views
from django.urls import include, path
from rest_framework import routers

app_name = "resources"

urlpatterns = [
    path('users/', views.UserList.as_view()),
    path('new_user/', views.RegisterNewUser.as_view()),
    path('seeker_create/', views.SeekerCardCreate.as_view()),
    path('seekerservices_create/', views.SeekerServicesCardCreate.as_view()),
    path('users/<int:pk>/', views.UserRetrieveDestroyUpdate.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]