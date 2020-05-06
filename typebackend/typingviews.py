from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import PractiseLog 
from .serializers import PractiseLogSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.utils import timezone
import datetime

class PostSpeed(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        sum=0
        today = timezone.now().replace(hour=0,minute=0,second=0)
        tmrw=today+datetime.timedelta(days=1)
        user_typing_log=PractiseLog.objects.filter(user__username=request.user,taken_at__gt=today,taken_at__lt=tmrw)
        serializers=PractiseLogSerializer(user_typing_log,many=True)

        for data in serializers.data:
            sum+=data["speed"]

        response_object={
            'avg':int(sum/len(serializers.data)) if len(serializers.data)>0 else False,
            'logs':serializers.data
            }

        return Response(response_object)
        
    def post(self,request):
        serializers=PractiseLogSerializer(data=request.data,context={'request':request})
        
        if serializers.is_valid():  
            user=serializers.save()
            return Response({'success':True})
        else:
            return Response({'success':False,'error':serializers.errors})