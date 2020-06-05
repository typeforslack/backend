from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import PractiseLog,Paragraph
from django.utils import timezone

class ParagraphSerializer(serializers.ModelSerializer):
    class Meta:
        model=Paragraph
        fields="__all__"

    def create(self,validated_data):
        savedpara=Paragraph.objects.create(taken_from=validated_data['taken_from'],para=validated_data['para'])
        return savedpara


class PractiseLogSerializer(serializers.ModelSerializer):
    class Meta:
        model=PractiseLog
        fields=["para","speed","taken_at"]

    def create(self,validated_data):
        user=self.context['request'].user
        result=user.practiselog_set.create(para=validated_data['para'],speed=validated_data['speed'],taken_at=validated_data['taken_at'])
        return result

    def to_representation(self,instance):
        response=super(PractiseLogSerializer,self).to_representation(instance)
        response['para']=Paragraph.objects.get(id=instance.para.id).para
        return response
    

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','password','email']
    
    def create(self,validated_data):
        user=User.objects.create_user(username=validated_data['username'],password=validated_data['password'],email=validated_data['email'])
        token=Token.objects.create(user=user)
        return token
