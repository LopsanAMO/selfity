import requests
import json
from django.conf import settings


class SmsService():
    def __init__(self):
        self.url = settings.SMSURL
        self.headers = {
            'content-type': 'application/json',
            'x-api-key': settings.SMSAPIKEY
        }

    def send_sms(self, number, message):
        payload = {
            "nbr": number,
            "msg": message
        }
        request = requests.post(
            url=self.url,
            data=json.dumps(payload),
            headers=self.headers
        )
        if request.status_code != 200:
            raise Exception('data not valid')
        return request.json()