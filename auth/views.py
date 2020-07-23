from typebackend.serializers import RegisterSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth.models import User
from google.auth.transport import requests
from rest_framework.views import APIView
from google.oauth2 import id_token
from rest_framework import status
from decouple import config
from random import randint
import time


class Register(APIView):
    def post(self,request):
        serializer=RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            return Response({'success':True,'token':user.key})
        else:
            return Response({'success':False,'error':serializer.errors},status=status.HTTP_400_BAD_REQUEST)

class LoginOrSignUpForGoogleUsers(APIView):
    def post(self,request):
        token=request.data['token']
        username=request.data.get('username',None)
        id_info=id_token.verify_oauth2_token(token,requests.Request(),config('CLIENT_ID'))

        if id_info['email_verified']:
            email=id_info['email']
            user_details=User.objects.filter(email=email).first()
            if username and user_details is None:
                password=hash(email)*randint(0,int(round(time.time() * 1000)))
                data={'email':email,'username':username,'password':password}
                serializer=RegisterSerializer(data=data)
                if serializer.is_valid():
                    user=serializer.save()
                    return Response({'success':True,'token':user.key})
                return Response({'success':False,'error':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
            elif user_details:
                if username is None:
                    token,created=Token.objects.get_or_create(user=user_details)
                    return Response({'token':token.key})
                return Response({'error':'Account exists!'},status=status.HTTP_400_BAD_REQUEST)
            return Response({'error':'New account, please register!'},status=status.HTTP_400_BAD_REQUEST)
        return Response({'error':'Invalid email ID '},status=status.HTTP_400_BAD_REQUEST)

class Logout(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        request.user.auth_token.delete()
        return Response({"success":True})