from django.db import models
from django.conf import settings 
from django.core.validators import FileExtensionValidator
from django.urls import reverse
from users.models import User
# Create your models here.
class News(models.Model):
    images = models.FileField(upload_to='photos/%Y/%m/%d', validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'svg'])], blank=True)
    theme = models.TextField(blank=True)
    body = models.TextField(blank=True)
    date = models.DateField(blank=True)
    time = models.TimeField(blank=True)
    viewers = models.IntegerField(blank=True,null=True)
    
    def __str__(self):
        return self.theme


class Recommandation(models.Model):
    image = models.ImageField(upload_to='photos/%y/%m/%d')
    title = models.CharField(max_length=255)
    body = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=255,choices=(('active','active'),('inactive','inactive')),default='inactive')
