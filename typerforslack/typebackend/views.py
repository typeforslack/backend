from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.


def index(request):
    success={
        'status':'Server is running'
    }
    return JsonResponse(success)

class Register(APIView):
    def post(self,request,format='json'):
        serializer=RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            return Response({'success':serializer.data})
        else:
            return Response({'success':'false','error':serializer.errors})

class Logout(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        request.user.auth_token.delete()
        return Response({"success":"true"})



