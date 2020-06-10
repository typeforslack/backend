from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from rest_framework.permissions import IsAuthenticated

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

class Logout(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        request.user.auth_token.delete()
        return Response({"success":True})