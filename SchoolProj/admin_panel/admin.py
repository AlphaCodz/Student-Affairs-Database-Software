from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Students

# Register your custom user model with the custom UserAdmin
admin.site.register(Students)