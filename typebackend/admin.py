from django.contrib import admin
from .models import PractiseLog,Paragraph

# Register your models here.

class TypingAdmin(admin.ModelAdmin):
    list_display=['user','para_id','speed','taken_at']

admin.site.register(PractiseLog,TypingAdmin)
admin.site.register(Paragraph)