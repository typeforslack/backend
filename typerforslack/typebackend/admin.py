from django.contrib import admin
from .models import PractiseLog

# Register your models here.

class TypingAdmin(admin.ModelAdmin):
    list_display=['user','speed','taken_at']

admin.site.register(PractiseLog,TypingAdmin)