from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import PractiseLog, DashboardData
from django.db.models import F
import datetime

@receiver(pre_save,sender=PractiseLog)
def create_or_update_streak(sender, instance, *args, **kwargs): 
    user=instance.user
    new_entry=instance.taken_at
    mode=instance.mode
    wpm=instance.wpm
    accuracy=instance.accuracy

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
        data.longest_streak=data.streak if data.streak>data.longest_streak else data.longest_streak
    # If the difference is greater, then reset the counter
    if days_between_recent_and_lastlog>1:
        data.inactive_days=data.inactive_days+(days_between_recent_and_lastlog-1)
        data.streak=1
        data.total_streak=data.total_streak+1

    para_typed=DashboardData.objects.filter(user=user).annotate(total=F('arcade')+F('practise')+F('race'))[0].total+1
    data.wpm=((data.wpm*(para_typed-1))+int(wpm))/para_typed
    data.accuracy=((data.accuracy*(para_typed-1))+int(accuracy))/para_typed

    data.save()