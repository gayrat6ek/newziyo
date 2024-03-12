from django.core.mail import send_mail
from django.conf import settings
import random
import re
import phonenumbers
from .utils import Config
import requests
from .models import User
from .eskizsms import send_sms



conf = Config()



def sender(phone_number):
    otp = random.randint(100000, 999999)
    message = f"Sizning varifikatsiya ko'dingiz {otp}"
    user_obj = User.objects.get(phone_number=phone_number)
    user_obj.otp = otp
    user_obj.save()
    send_sms(phone_number,message)
    return True



def phonecheck(s):
    if s.isupper() or s.islower():
        return False
    else:
        try:
            my_number = phonenumbers.parse(s)
            result = phonenumbers.is_valid_number(my_number)
        except: 
            result = False
        return result

def phone_or_mail(mail):
    phone_check = phonecheck(mail)
    if phone_check:
        sender(mail)
        return True
    else:
        return False
