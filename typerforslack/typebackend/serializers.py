from rest_framework import serializers
from django.contrib.auth.models import User
import . from models

class PraticeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model=TypingRecord
        fields="__all__"


