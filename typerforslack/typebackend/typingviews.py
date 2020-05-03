from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import TypingRecord 
from .serializers import PraticeLogSerializer
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
        user_typing_log=TypingRecord.objects.filter(user_id__username=request.user,typeddate__gt=today,typeddate__lt=tmrw)
        serializers=PraticeLogSerializer(user_typing_log,many=True)

        for data in serializers.data:
            sum+=data["speed"]

        response_object={
            'avg':int(sum/len(serializers.data)) if len(serializers.data)>0 else "Didn't Type Yet Bruh",
            'logs':serializers.data
            }

        return Response(response_object)
        
    def post(self,request):
        serializers=PraticeLogSerializer(data=request.data,context={'request':request})
        
        if serializers.is_valid():  
            user=serializers.save()
            return Response({'success':serializers.data})
        else:
            print(serializers.errors)
            return Response({'success':'False'})