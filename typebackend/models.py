from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator


# Create your models here.

class PractiseLog(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)
    para=models.ForeignKey('Paragraph',on_delete=models.CASCADE)
    wpm=models.IntegerField(db_column='Typing Speed',validators=[MaxValueValidator(400)])
    taken_at=models.DateTimeField('Practised On')
    correct_words=models.IntegerField(db_column='Total correct words')
    wrong_words=models.IntegerField(db_column='Wrong Words')
    total_words=models.IntegerField(db_column='Total Words')
    accuracy=models.FloatField(db_column='Accuracy')
    mode=models.CharField(max_length=9)
    def __str__(self):
        return self.user.username

class Paragraph(models.Model):
    taken_from=models.CharField('Taken from',max_length=25)
    para=models.TextField('Paragraph',unique=True)

    def __str__(self):
        return self.taken_from

class DashboardData(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)
    streak=models.IntegerField(default=0)
    inactive_days=models.IntegerField(default=0)
    longest_streak=models.IntegerField(default=0)
    total_streak=models.IntegerField(default=0)
    arcade=models.IntegerField(db_column='Arcade count',default=0)
    practise=models.IntegerField(db_column='Practise count',default=0)
    race=models.IntegerField(db_column='Race count',default=0)
    wpm=models.IntegerField(db_column='WPM Average',default=0)
    accuracy=models.IntegerField(db_column='Accuracy Average',default=0)

    def __str__(self):
        return self.user.username