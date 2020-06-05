from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator


# Create your models here.

class PractiseLog(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)
    para=models.ForeignKey('Paragraph',on_delete=models.CASCADE)
    speed=models.IntegerField(db_column='Typing Speed',validators=[MaxValueValidator(400)])
    taken_at=models.DateTimeField('Practised On')
    
    def __str__(self):
        return self.user.username

class Paragraph(models.Model):
    taken_from=models.CharField('Taken from',max_length=25)
    para=models.TextField('Paragraph',unique=True)

    def __str__(self):
        return self.taken_from