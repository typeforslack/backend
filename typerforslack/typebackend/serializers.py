from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import TypingRecord
from django.utils import timezone

class PraticeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model=TypingRecord
        fields=["user_id","speed","typeddate"]

    def create(self,validated_data):
        user=self.context['request'].user
        result=user.typingrecord_set.create(speed=validated_data['speed'],typeddate=validated_data['typeddate'])
        return result

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','password']
    
    def create(self,validated_data):
        user=User.objects.create_user(username=validated_data['username'],password=validated_data['password'])
        token=Token.objects.create(user=user)
        return token
