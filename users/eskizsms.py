import os,sys
import requests
from dotenv import load_dotenv
load_dotenv()

ESKIZ_BASE_URL = os.getenv("ESKIZ_BASE_URL")
ESKIZ_LOGIN = os.getenv("ESKIZ_LOGIN")
ESKIZ_PASSWORD = os.getenv("ESKIZ_PASSWORD")


def get_token():
    url = f"{ESKIZ_BASE_URL}/api/auth/login"
    data = {
        "email": ESKIZ_LOGIN,
        "password": ESKIZ_PASSWORD
    }
    response = requests.post(url, data=data)
    return response.json()['data']['token']


def send_sms(phone,message):
    print('hello')
    token = get_token()
    url = f"{ESKIZ_BASE_URL}/api/message/sms/send"

    data = {
        "mobile_phone": phone,
        "message": message,
        'from':4546
    }
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.post(url, data=data, headers=headers)
    return response.json()