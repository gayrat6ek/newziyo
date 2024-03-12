from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import pytz
from datetime import datetime
class UserManager(BaseUserManager):

    
    def create_user(self, phone_number, password, **other_fields):

        if not phone_number:
            raise ValueError("Provide phone number")
        user = self.model(phone_number=phone_number, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_number, password, **other_fields):
        other_fields.setdefault('is_staff',True)
        other_fields.setdefault('is_superuser',True)
        other_fields.setdefault('is_active',True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('staff privilege must be assigned to superuser')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('superuser privilege must be assigned to superuser')

        return self.create_user(phone_number, password, **other_fields)


class User(AbstractBaseUser,PermissionsMixin):

    phone_number = models.CharField(max_length=255,unique=True)
    email = models.EmailField(null=True, blank=True)
    full_name = models.CharField(max_length=255,null=True,blank=True)
    phone_varified_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    birth_date = models.DateField(null=True,blank=True)
    status = models.CharField(max_length=255)
    otp = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    fcm_token = models.CharField(max_length=255,null=True)
    is_active = models.BooleanField(default=False)
    tarif = models.CharField(max_length=255,choices=(('premium', 'premium'),('free', 'free'),('turbo','turbo')),blank=True,default='free')
    image = models.ImageField(upload_to='images',null=True,blank=True)
    language = models.CharField(max_length = 100,choices=(('latin','latin'),('cyrill','cyrill')),default='cyrill')
    objects = UserManager()
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []


tz = pytz.timezone("Asia/Tashkent")

class Chat(models.Model):
    
    from_user  = models.ForeignKey(User,on_delete=models.PROTECT,related_name='from_user')
    text_body = models.TextField()
    time_created = models.TimeField()
    date_field = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True,upload_to='images')
    def save(self, *args, **kwargs):
        if not self.time_created:
            self.time_created = datetime.now(tz).time().strftime('%H:%M:%S')
        super().save(*args, **kwargs)
