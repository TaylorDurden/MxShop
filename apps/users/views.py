from django.shortcuts import render

# Create your views here.
from random import choice


from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.mixins import CreateModelMixin


from .serializers import SMSSerializer
from .models import VerifyCode
from utils.yunpian import YunPian
from MxShop.settings import SMS_API_KEY

User = get_user_model()


class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username)|Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewSet(CreateModelMixin, viewsets.GenericViewSet):
    """
    发送短信验证码
    """
    serializer_class = SMSSerializer

    def generate_code(self):
        """
        生成4位数字的验证码
        :return:
        """
        seeds = "123456789"
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))
        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data["mobile"]
        sms = YunPian(SMS_API_KEY)

        code = self.generate_code()
        sms_send_status = sms.send_sms(code=code, mobile=mobile)
        if sms_send_status["code"] != 0: #失败
            return Response({
                "mobile": sms_send_status["detail"]
            }, status=status.HTTP_400_BAD_REQUEST)
        else: #成功
            sms_record = VerifyCode(code=code, mobile=mobile)
            sms_record.save()
            return Response({
                "mobile": mobile
            }, status=status.HTTP_201_CREATED)


class UserViewSet(CreateModelMixin, viewsets.GenericViewSet):
    """
    用户
    """
