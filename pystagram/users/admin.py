from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User


# Register your models here.
class FollowersInline(admin.TabularInline):
    model = User.following.through
    fk_name = "from_user"
    verbose_name = "내가 팔로우 하고 있는 사용자"
    verbose_name_plural = f"{verbose_name} 목록"
    extra = 1


class FollowingInline(admin.TabularInline):
    model = User.following.through
    fk_name = "to_user"
    verbose_name = "나를 팔로우 하고 있는 사용자"
    verbose_name_plural = f"{verbose_name} 목록"
    extra = 1


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = [
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        ("Additional Fields",
         {
             "fields": (
                 "profile_image", "short_description"
             )
         }
         ),
        ("Related Objects", {"fields": ("like_posts",)}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    ]
    inlines = [
        FollowersInline,
        FollowingInline
    ]
