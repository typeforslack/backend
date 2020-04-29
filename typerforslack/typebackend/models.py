from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator


# Create your models here.

class TypingRecord(models.Model):
    user_id=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    speed=models.IntegerField(db_column='Typing Speed',validators=[MaxValueValidator(3)])
    typeddate=models.DateTimeField('Practised On')
    
    def __str__(self):
        return self.speed