
"""
Django admin customization
"""
from .models import User, Profile, Room, Messages, Topic
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin


admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Messages)
