from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class index(APIView):
    def get(self,request):
        success={
            'status':'Server is running'
        }
        return Response(success)

class Register(APIView):
    def get(self,request):
        get_user=User.objects.all()
        serializer=RegisterSerializer(get_user,many=True)
        return Response(serializer.data)

    def post(self,request,format='json'):
        serializer=RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            return Response({'success':'Registered','token':user.key})
        else:
            return Response({'success':'false','error':serializer.errors})

class Logout(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        request.user.auth_token.delete()
        return Response({"success":"true"})



