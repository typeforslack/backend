from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import PractiseLog,Paragraph
from .serializers import PractiseLogSerializer,ParagraphSerializer
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.authtoken.models import Token
from django.utils import timezone
from random import randint
import datetime



previous_para_id=None

def generateNewParaNumber(previous_para_id,totalcount):
    new_number=None
    new_number=randint(0,totalcount-1)
    if previous_para_id==new_number:
        return generateNewParaNumber(previous_para_id,totalcount)
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
            return Response({'success':False,'error':serializers.errors})

class Paradetails(APIView):
    permission_classes=[IsAdminUser]
   
    def get(self,request):
        
        global previous_para_id

        total_para=Paragraph.objects.count()
        para_number=randint(0,total_para-1)

        if(previous_para_id==para_number):
            para_number=generateNewParaNumber(previous_para_id,total_para)

        para_details=Paragraph.objects.all()[para_number]
        serializers=ParagraphSerializer(para_details)
        previous_para_id=para_number
     
       
        return Response(serializers.data)


    def post(self,request):
        serializers=ParagraphSerializer(data=request.data)
        
        if serializers.is_valid():
            para=serializers.save()
            return Response({'success':True})
        else:
            return Response({'success':False,'error':serializers.errors})
