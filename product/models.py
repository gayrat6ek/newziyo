from django.db import models
from users.models import User
import pytz
from django.utils import timezone
from datetime import datetime
from django.core.validators import FileExtensionValidator
# Create your models here.
class CreateCategoryModel(models.Model):
    name = models.CharField(max_length=200,unique=True,blank=True)
    icon = models.FileField(upload_to='photos/%Y/%m/%d',validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'svg'])],blank=True)
    def __str__(self):
        return self.name

class SubCategoryModel(models.Model):
    parent = models.ForeignKey(CreateCategoryModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=155)
    def __str__(self):
        return self.name


class SubCategoryParams(models.Model):
    subcategory = models.ForeignKey(SubCategoryModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    type_of_value = models.CharField(max_length=255,choices=(('string','string'),('integer','integer'),('select','select'),('multiselect','multiselect')))


class ParamSelectValues(models.Model):
    parent_param = models.ForeignKey(SubCategoryParams,on_delete=models.CASCADE,related_name='children')
    value = models.CharField(max_length=255)


tz = pytz.timezone("Asia/Tashkent")

class AnnouncementModel(models.Model):
    subcategory = models.ForeignKey(SubCategoryModel,on_delete=models.CASCADE,related_name='subcategory')
    title = models.CharField(max_length=255,null=True)
    currency = models.CharField(max_length=255,choices=(('Dollar', 'dollar'),('Som','som')),null=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField()
    body = models.TextField(null=True)
    price = models.FloatField(null=True)
    location = models.TextField(null=True)
    district = models.CharField(max_length=255,null=True)
    image = models.FileField(upload_to = 'photos/%Y/%m/%d',validators=[FileExtensionValidator(['jpg', 'jpeg','png','svg'])],null=True)
    images = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=255,choices=(('inactive', 'inactive'), ('rejected', 'rejected'),('published','published')),default='inactive',blank=True)
    notisification = models.CharField(max_length=255,blank=True,null=True)
    viewers = models.IntegerField(blank=True,null=True)
    contact_number = models.CharField(max_length=255,blank=True)
    contact_name = models.CharField(max_length=255,blank=True)
    likers = models.ManyToManyField(User,related_name='likers',blank=True)
    user_controller = models.CharField(max_length=255,choices=(('active','active'),('inactive','inactive')),default='active')
    kelishuv = models.BooleanField(default=False,null=True)

    def save(self, *args, **kwargs):
        if not self.time:
            self.time = datetime.now(tz).time().strftime('%H:%M:%S')
        super().save(*args, **kwargs)


class SubCategoryValues(models.Model):
    params = models.ForeignKey(SubCategoryParams,on_delete=models.CASCADE)
    announcement = models.ForeignKey(AnnouncementModel,on_delete=models.CASCADE,related_name='announcements')
    string = models.CharField(max_length=255,blank=True,null=True)
    integer = models.IntegerField(blank=True,null=True)
    selecttion = models.ForeignKey(ParamSelectValues,null=True,blank=True,on_delete=models.CASCADE)


class NotisificationModel(models.Model):
    theme = models.CharField(max_length=255)
    value = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    is_sended = models.BooleanField(default=False)




    