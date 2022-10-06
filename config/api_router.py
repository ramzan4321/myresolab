from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from resolab.resources.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("resources", UserViewSet)


app_name = "api"
urlpatterns = router.urls
