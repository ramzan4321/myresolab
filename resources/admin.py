from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from .forms import UserAdminChangeForm, UserAdminCreationForm
from .models import ResourceProvider, ResourceSeeker, ResourceSeekerServices,SubscriptionPlan,SubscriptionPayment,SubscriptionOrder,UserSubscription
User = get_user_model()

admin.site.register(ResourceProvider)
admin.site.register(ResourceSeeker)
admin.site.register(ResourceSeekerServices)

admin.site.register(SubscriptionPlan)
admin.site.register(SubscriptionOrder)
admin.site.register(SubscriptionPayment)
admin.site.register(UserSubscription)

@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    readonly_fields = ["date_joined","last_login"]
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email","phone")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login","date_joined")}),
    )
    list_display = ["username", "first_name", "last_name", "is_superuser"]
    search_fields = ["username"]
