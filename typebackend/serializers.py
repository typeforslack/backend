from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import PractiseLog,Paragraph,DashboardData
from django.utils import timezone

class ParagraphSerializer(serializers.ModelSerializer):
    class Meta:
        model=Paragraph
        fields=['id','taken_from','para']        

    def create(self,validated_data):
        taken_from=validated_data['taken_from'].lower()
        savedpara=Paragraph.objects.create(taken_from=taken_from,para=validated_data['para'])
        return savedpara


class PractiseLogSerializer(serializers.ModelSerializer):
    class Meta:
        model=PractiseLog
        fields="__all__"
        extra_kwargs = {'para': {'write_only': True},'user':{'write_only':True}}

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','password','email']
    
    def create(self,validated_data):
        user=User.objects.create_user(username=validated_data['username'],password=validated_data['password'],email=validated_data['email'])
        token=Token.objects.create(user=user)
        return token,user

class StreakSerializer(serializers.ModelSerializer):
    class Meta:
        model=DashboardData
        fields='__all__'
        extra_kwargs={'user':{'write_only':True}}

    