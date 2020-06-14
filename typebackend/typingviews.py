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
from random import randint,choice
import datetime
import time

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
        #For Testing Purpose
        if(request.user.id==38):
            para_ids=[1,14,15]
            para_position=choice(para_ids)
            para=Paragraph.objects.get(id=para_position)
            serializers=ParagraphSerializer(para)
            return Response(serializers.data)
        
        # Query to find the paragraph that are yet to be typed by the user
        paras_typed=PractiseLog.objects.filter(user_id=38).order_by('taken_at')
        paras_typed_ids = paras_typed.values_list('para_id', flat=True)
        para_yet_to_be_typed=Paragraph.objects.exclude(id__in=list(paras_typed_ids))

        if len(para_yet_to_be_typed)!=0:
            para_details = choice(para_yet_to_be_typed)
        else:
            # When user has typed all the paras
            # Remove last 5 paras user typed and give random from that new list
            without_last_five = paras_typed[:len(paras_typed)-5]
            chosen_one = choice(without_last_five)
            para_details = chosen_one.para

        serializers=ParagraphSerializer(para_details)
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
