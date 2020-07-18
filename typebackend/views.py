from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from .serializers import RegisterSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from google.auth.transport import requests
from rest_framework.views import APIView
from django.shortcuts import render
from google.oauth2 import id_token
from rest_framework import status
from decouple import config
from random import randint
import time


# Create your views here.


class index(APIView):
    renderer_classes = [JSONRenderer]
    def get(self,request):
        success={
            'status':'Server is running!'
        }
        return Response(success)

class UserNameAvailability(APIView):
    def get(self,request):
        username=request.GET.get('username',None)
        
        data={
            'is_taken':User.objects.filter(username=username).exists(),
        }
        if data['is_taken']:
            data['error']='Username already exists'

        return Response(data)

class Register(APIView):
    def post(self,request):
        serializer=RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            return Response({'success':True,'token':user.key})
        else:
            return Response({'success':False,'error':serializer.errors},status=status.HTTP_400_BAD_REQUEST)

class RegisterForGoogleUsers(APIView):
    def post(self,request):
        token=request.data['token']
        username=request.data['username']
        id_info=id_token.verify_oauth2_token(token,requests.Request(),config('CLIENT_ID'))
        email=id_info['email']
        password=hash(email)*randint(0,int(round(time.time() * 1000)))
        data={'email':email,'username':username,'password':password}
        serializer=RegisterSerializer(data=data)
        if serializer.is_valid():
            user=serializer.save()
            return Response({'success':True,'token':user.key})
        else:
            return Response({'success':False,'error':serializer.errors},status=status.HTTP_400_BAD_REQUEST)

class LoginForGoogleUsers(APIView):
    def post(self,request):
        token=request.data['token']
        id_info=id_token.verify_oauth2_token(token,requests.Request(),config('CLIENT_ID'))
        email=id_info['email']
        user_details=User.objects.get(email=email)
        if user_details:
            token=Token.objects.create(user=user_details)
            return Response({'token':token.key})
        else:
            return Response({'error':'Invalid Credential'},status=status.HTTP_400_BAD_REQUEST)

class Logout(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        request.user.auth_token.delete()
        return Response({"success":True})