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

def generateNewParaNumber(paraid,totalcount):
    new_number=randint(1,totalcount)
    if new_number==paraid:
        return generateNewParaNumber(paraid,totalcount)
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

        # Query to find the paragraph that are yet to be typed by the user
        para_typed=PractiseLog.objects.filter(user_id=request.user).values_list('para_id',flat=True)
        para_yet_to_be_typed=Paragraph.objects.exclude(id__in=list(para_typed))

        paragraph_count=Paragraph.objects.count()
        para_position=randint(1,paragraph_count)
     
        if len(para_yet_to_be_typed)==0 and previous_typed==para_position:
                para_position=generateNewParaNumber(para_position,paragraph_count)

        elif len(para_yet_to_be_typed)!=0:
                para_position=para_yet_to_be_typed[0].id

        para_details=Paragraph.objects.get(id=para_position)
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

class DashboardData(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request,days=0):  
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