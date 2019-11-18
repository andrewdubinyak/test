from django.contrib import admin
from .models import UserType

@admin.register(UserType)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user',]