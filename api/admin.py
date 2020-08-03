from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from api.models import *


# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    pass


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
