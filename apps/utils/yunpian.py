# _*_ encoding:utf-8 _*_
__author__ = 'taylor lee'
import requests
import json

class YunPian(object):
    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"

    def send_sms(self, code, mobile):
        params = {
            "apikey": self.api_key,
            "mobile": mobile,
            "text": "【慕生鲜】您的验证码是{code}。如非本人操作，请忽略本短信".format(code=code)
        }

        response = requests.post(url=self.single_send_url, data=params)
        result_dict = json.loads(response.text)
        return result_dict


if __name__ == "__main__":
    yun_pian = YunPian("8e6b011ff0f976d8512aa57425bac1e7")
    yun_pian.send_sms("666666", "18202978485")
