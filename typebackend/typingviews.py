from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import PractiseLog,Paragraph
from .serializers import PractiseLogSerializer,ParagraphSerializer
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.authtoken.models import Token
from django.utils import timezone
from random import randint
import datetime


previous_para_number=None

def generateNewParaNumber(previous_para_number,totalcount):
    new_number=randint(0,totalcount-1)
    if previous_para_number==new_number:
        return generateNewParaNumber(previous_para_number,totalcount)
    return new_number

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
            return Response({'success':False,'error':serializers.errors},status=status.HTTP_400_BAD_REQUEST)

class Paradetails(APIView):
    permission_classes=[IsAdminUser]
   
    def get(self,request):
        
        global previous_para_number
        total_no_of_paragraph=Paragraph.objects.count()
        para_position=randint(0,total_no_of_paragraph-1)

        if(previous_para_number==para_position):
            para_position=generateNewParaNumber(previous_para_number,total_no_of_paragraph)

        para_details=Paragraph.objects.all()[para_position]
        serializers=ParagraphSerializer(para_details)
        previous_para_number=para_position
    
        return Response(serializers.data)


    def post(self,request):
        serializers=ParagraphSerializer(data=request.data)
        
        if serializers.is_valid():
            para=serializers.save()
            return Response({'success':True})
        else:
            return Response({'success':False,'error':serializers.errors},status=status.HTTP_400_BAD_REQUEST)
