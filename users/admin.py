from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

# user admin에서 직접 room을 추가하고 싶은 경우
# from rooms import models as room_models

# class RoomInline(admin.TabularInline):
#     model = room_models.Room


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):

    """ Custom User Admin """

    # user admin에서 직접 room을 추가하고 싶은 경우
    # inlines = (RoomInline,)

    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "birthdate",
                    "language",
                    "currency",
                    "superhost",
                )
            },
        ),
    )

    list_filter = UserAdmin.list_filter + ("superhost",)

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "language",
        "currency",
        "superhost",
        "is_staff",
        "is_superuser",
        "email_verified",
        "email_secret",
    )
