from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import PractiseLog,Paragraph,DashboardData
from .serializers import PractiseLogSerializer,ParagraphSerializer,StreakSerializer
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.authtoken.models import Token
from django.db.models import Sum
from django.utils import timezone
from random import randint,choice
import datetime
import json

def create_or_update_streak(user,new_entry,mode): 
    # Converting string date to datetime format
    new_entry=datetime.datetime.strptime(new_entry,'%Y-%m-%d %H:%M:%S')

    try:
        last_typed=PractiseLog.objects.filter(user=user).latest('taken_at').taken_at
    except PractiseLog.DoesNotExist:
        # When its a new user, the first if condition has to be followed. Hence setting last_typed to previous_day
        last_typed=new_entry-datetime.timedelta(1)

    # Finding the difference in days between the last log and the new log.
    days_between_recent_and_lastlog=(new_entry-last_typed).days
    data=DashboardData.objects.get(user=user)

    # Getting the existing value of the mode [practise/arcade/race] specified in the user object from the query and updating it.
    count=getattr(data,mode)+1
    #Setting the updated value of the mode count
    setattr(data,mode,count)

    # Checking for consecutive streak from the database, i.e if the difference between previous log and new log is 1, then the user has been typing consecutively
    if days_between_recent_and_lastlog==1:
        data.streak=data.streak+1
        data.total_streak=1 if data.total_streak==0 else 0 # Incase of new user
        data.longest_streak=data.streak if data.streak>data.longest_streak else data.longest_streak
    # If the difference is greater, then reset the counter
    if days_between_recent_and_lastlog>1:
        data.inactive_days=data.inactive_days+(days_between_recent_and_lastlog-1)
        data.streak=1
        data.total_streak=data.total_streak+1

    data.save()

class PostSpeed(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request):
        if request.data['mode']=='practise' or request.data['mode']=='race' or request.data['mode']=='arcade':
            serializers=PractiseLogSerializer(data=request.data,context={'request':request})
            if serializers.is_valid():
                user=request.user
                typed_at=request.data['taken_at']
                mode=request.data['mode']
                # Streak counter update 
                create_or_update_streak(user,typed_at,mode) 
                user=serializers.save()
                return Response({'success':True})
            return Response({'success':False,'error':serializers.errors},status=status.HTTP_400_BAD_REQUEST)
        return Response({'success':False,'error':'Invalid mode, should be "practise/race/arcade"'})

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
        paras_typed=PractiseLog.objects.filter(user_id=request.user.id).order_by('taken_at')
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

class GraphData(APIView):
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

class RaceTrack(APIView):
    def get(self,request):
        data=json.loads(request.query_params['data'])
        para_yet_to_be_typed=Paragraph.objects.exclude(id__in=data)
        if(len(para_yet_to_be_typed)==0):
            para_yet_to_be_typed=Paragraph.objects.all()
        chosen_paragraph=choice(para_yet_to_be_typed)
        serializers=ParagraphSerializer(chosen_paragraph)
        return Response(serializers.data)

class Dashboard(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        # { avg wpm, avg accuracy, user since, streak, Inactive days, longest streak, Total stresks, mode count }
        user_id=request.user.id

        dashboard_data={}
        dashboard_data['user_since']=str(User.objects.get(id=user_id).date_joined)[0:10]
        total_log=PractiseLog.objects.filter(user=user_id).count()
        wpm_and_accuracy=PractiseLog.objects.filter(user_id=user_id).aggregate(wpm=Sum('wpm')/total_log,accuracy=Sum('accuracy')/total_log)
        dashboard_data['wpm']=wpm_and_accuracy['wpm']
        dashboard_data['accuracy']=wpm_and_accuracy['accuracy']
        streak_data=DashboardData.objects.get(user_id=user_id)
        streak_serializer=StreakSerializer(streak_data).data
        streak_serializer.pop('id')
        dashboard_data.update(streak_serializer)

        return Response(dashboard_data)
