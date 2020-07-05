from django.contrib import admin

from api.models import *


# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass
