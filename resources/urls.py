from .api import views
from django.urls import include, path
from rest_framework import routers

app_name = "resources"

urlpatterns = [
    ############################    Start Registration Block    ################################

    path('users/', views.UserList.as_view()),
    path('new_user/', views.RegisterNewUser.as_view()),
    path('provider_create/', views.ProviderCardCreate.as_view()),
    path('seeker_create/', views.SeekerCardCreate.as_view()),
    path('seekerservices_create/', views.SeekerServicesCardCreate.as_view()),

    ############################    End Registration Block   ####################################

    ############################    Start Specific Data Retrieving Block   ######################

    path('users/<int:pk>/', views.UserRetrieveDestroyUpdate.as_view()),
    path('provider_details/<int:pk>/', views.ProviderViewDetails.as_view()),
    path('seeker_details/<int:pk>/', views.SeekerViewDetails.as_view()),

    path('provider_view/<str:state>/', views.StateWiseProviderView.as_view()),
    path('provider_view/<str:state>/<str:city>/', views.StateWiseProviderView.as_view()),
    path('provider_view/<str:state>/<str:city>/<str:category>', views.StateWiseProviderView.as_view()),
    path('provider_view/<str:state>/<str:city>/<str:category>/<str:jobrole>', views.StateWiseProviderView.as_view()),

    path('provider_cityview/<str:city>/', views.StateWiseProviderView.as_view()),
    path('provider_cityview/<str:city>/<str:category>/', views.StateWiseProviderView.as_view()),
    path('provider_cityview/<str:city>/<str:category>/<str:jobrole>', views.StateWiseProviderView.as_view()),
   
    path('provider_categoryview/<str:category>/', views.StateWiseProviderView.as_view()),
    path('provider_categoryview/<str:state>/<str:category>/', views.StateWiseProviderView.as_view()),
    path('provider_categoryview/<str:state>/<str:category><str:jobrole>/', views.StateWiseProviderView.as_view()),
    
    path('provider_jobview/<str:jobrole>/', views.StateWiseProviderView.as_view()),
    path('provider_jobview/<str:city>/<str:jobrole>/', views.StateWiseProviderView.as_view()),
    path('provider_jobview/<str:state>/<str:jobrole>/', views.StateWiseProviderView.as_view()),
    path('provider_jobview/<str:category>/<str:jobrole>/', views.StateWiseProviderView.as_view()),

    ############################    End Specific Data Retrieving Block   ########################

    ############################    Start Whole Data Retrieving Block   #########################

    path('resource_provider/', views.ProviderCardView.as_view()),
    path('resource_required/', views.ResourceRequiredCardView.as_view()),

    ############################    End Whole Data Retrieving Block   ###########################

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]