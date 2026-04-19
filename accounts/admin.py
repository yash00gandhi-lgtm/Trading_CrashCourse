from django.contrib import admin
from .models import Profile

admin.site.register(Profile)
# accounts/admin.py
from .models import ContactMessage

admin.site.register(ContactMessage)