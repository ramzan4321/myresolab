from .api import views
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import CheckoutSubscriptionData, SubscriptionCallbackEndpoint, Payment
app_name = "resources"

urlpatterns = [

    path('providerverify/', views.IsVerifiedProviderView.as_view()),
    path('providerverify/<int:pk>/', views.IsVerifiedProvider.as_view()),

    path('seekerverify/', views.IsVerifiedSeekerView.as_view()),
    path('seekerverify/<int:pk>/', views.IsVerifiedSeeker.as_view()),

    path('gettoken/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refreshtoken/', TokenRefreshView.as_view(), name='token_refresh'),
    #---------------------------    Start Registration Block    --------------------------------

    path('users/', views.UserList.as_view()),
    path('users/<int:pk>', views.UserRetrieveDestroyUpdate.as_view()),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('new_user/', views.RegisterNewUser.as_view(), name='signup'),
    path('provider_create/', views.ProviderCardCreate.as_view()),
    path('seeker_create/', views.SeekerCardCreate.as_view()),
    path('seekerservices_create/', views.SeekerServicesCardCreate.as_view()),
    path('seekerupdate/<int:pk>', views.SeekerRetrieveDestroyUpdate.as_view()),
    path('providerupdate/<int:pk>', views.ProviderRetrieveDestroyUpdate.as_view()),

    #---------------------------    End Registration Block   -----------------------------------

    #---------------------------    Start Specific Data Retrieving Block   ---------------------

    path('required_view/<str:state>/<str:city>/<str:category>/<str:jobrole>', views.StateWiseRequiredView.as_view()),

    path('required_cityview/<str:city>/<str:category>/<str:jobrole>', views.StateWiseRequiredView.as_view()),
   
    path('required_categoryview/<str:state>/<str:category><str:jobrole>/', views.StateWiseRequiredView.as_view()),

    path('required_jobview/<str:state>/<str:jobrole>/', views.StateWiseRequiredView.as_view()),
    path('required_jobview/<str:category>/<str:jobrole>/', views.StateWiseRequiredView.as_view()),

    
    path('provider_cityview/<str:city>/<str:category>/<str:jobrole>', views.StateWiseProviderView.as_view()),
    path('provider_categoryview/<str:state>/<str:category><str:jobrole>/', views.StateWiseProviderView.as_view()),
    
    path('provider_statejob/<str:state>/<str:jobrole>/', views.StateWiseProviderView.as_view()),
    path('provider_catejob/<str:category>/<str:jobrole>/', views.StateWiseProviderView.as_view()),



    #---------------------------    End Specific Data Retrieving Block   -----------------------

    #---------------------------    Start Whole Data Retrieving Block   ------------------------

    path('resource_provider/', views.ProviderCardView.as_view()),
    path('resource_required/', views.ResourceRequiredCardView.as_view()),

    #---------------------------    End Whole Data Retrieving Block   --------------------------

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('checkout/', CheckoutSubscriptionData.as_view(), name='checkout_subscription_data'),
    path('callback/', SubscriptionCallbackEndpoint.as_view(), name='callback'),
    
    path('paymentstatus/', Payment.as_view(), name='payment'),
]