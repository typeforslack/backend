from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator


# Create your models here.

class PractiseLog(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)
    speed=models.IntegerField(db_column='Typing Speed',validators=[MaxValueValidator(400)])
    taken_at=models.DateTimeField('Practised On')
    
    def __str__(self):
        return self.user_id.username