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

previous_typed=None

def generateNewParaNumber(typed_para,totalcount):
    new_number=randint(0,totalcount)
    if new_number in typed_para:
        return generateNewParaNumber(typed_para,totalcount)
    return new_number

class PostSpeed(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request):
        serializers=PractiseLogSerializer(data=request.data,context={'request':request})
        
        if serializers.is_valid():  
            user=serializers.save()
            return Response({'success':True})
        else:
            return Response({'success':False,'error':serializers.errors},status=status.HTTP_400_BAD_REQUEST)

class Paradetails(APIView):
    permission_classes=[IsAuthenticated]
   
    def get(self,request):
        global previous_typed
        typed_para=[]

        userlog=PractiseLog.objects.filter(user=request.user)

        for data in userlog:
            typed_para_id=data.para.id-1
            typed_para.append(typed_para_id)

        total_no_of_paragraph=Paragraph.objects.count()-1
        para_position=randint(0,total_no_of_paragraph)

        if total_no_of_paragraph in typed_para:
            if previous_typed==para_position:
                para_position=generateNewParaNumber([para_position],total_no_of_paragraph)
        else:
            if para_position in typed_para:
                para_position=generateNewParaNumber(typed_para,total_no_of_paragraph)
            
        para_details=Paragraph.objects.all()[para_position]
        serializers=ParagraphSerializer(para_details)
        previous_typed=para_position
    
        return Response(serializers.data)

    def post(self,request):
        serializers=ParagraphSerializer(data=request.data)
        
        if serializers.is_valid():
            para=serializers.save()
            return Response({'success':True})
        else:
            return Response({'success':False,'error':serializers.errors},status=status.HTTP_400_BAD_REQUEST)

class Graphdata(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request,days):  
        date_typed_log={}

        userlog=PractiseLog.objects.filter(user=request.user,taken_at__gte=timezone.now()-datetime.timedelta(days=int(days)))
        log_serializer=PractiseLogSerializer(userlog,many=True)

        for data in log_serializer.data:
    
            date_typed=str(data["taken_at"])[0:10]
            data.pop('taken_at')
    
            if date_typed_log.get(date_typed):
                date_typed_log[date_typed].append(data)        
            else:
                date_typed_log[date_typed]=[data]

        return Response(date_typed_log)