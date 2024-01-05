from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User


@admin.register(User)
class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "phone_number", "password")}),
        ("Персональная информация", {"fields": ("first_name",
                                                "last_name",
                                                "business_type",
                                                "legal_name",
                                                "inn",
                                                "kpp",
                                                "legal_address",
                                                "file_with_contacts",
                                                "fax",
                                                "company",
                                                "address1",
                                                "address2",
                                                "city",
                                                "index",
                                                "country",
                                                "mailing",)
                                     }
         ),
        (
            "Полномочия",
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
        ("Важные даты", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "phone_number", "password1", "password2"),
            },
        ),
    )

    list_display = ("email", "phone_number", "first_name", "last_name")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("email", "phone_number", "first_name", "last_name")
    ordering = ("email", )
