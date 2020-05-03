from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import TypingRecord

class PraticeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model=TypingRecord
        fields="__all__"

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','password']
    
    def create(self,validated_data):
        user=User.objects.create_user(username=validated_data['username'],password=validated_data['password'])
        token,status=Token.objects.get_or_create(user=user)
        return token
