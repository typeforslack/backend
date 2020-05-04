from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import PractiseLog
from django.utils import timezone

class PractiseLogSerializer(serializers.ModelSerializer):
    class Meta:
        model=PractiseLog
        fields=["user","speed","taken_at"]

    def create(self,validated_data):
        user=self.context['request'].user
        result=user.practiselog_set.create(speed=validated_data['speed'],taken_at=validated_data['taken_at'])
        return result

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','password']
    
    def create(self,validated_data):
        user=User.objects.create_user(username=validated_data['username'],password=validated_data['password'])
        token=Token.objects.create(user=user)
        return token
