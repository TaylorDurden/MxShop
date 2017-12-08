# _*_ encoding:utf-8 _*_
__author__ = 'taylor lee'
import re # 正则表达式模块
import datetime
from datetime import timedelta


from rest_framework import serializers
from django.contrib.auth import get_user_model


from .models import VerifyCode
from MxShop.settings import REGEX_MOBILE

User = get_user_model()


class SMSSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validated_mobile(self, mobile):
        """
        验证手机号码
        :param mobile:
        :return:
        """

        # 手机号是否已注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("该手机号已注册！")

        # 验证手机号码是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码格式不正确")

        # 验证码发送频率
        one_minute_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)

        if VerifyCode.objects.filter(add_time__gt=one_minute_ago, mobile=mobile):
            raise serializers.ValidationError("距离上一次发送未超过60秒")

        return mobile


class UserSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True, max_length=4, min_length=4)

    def validate_code(self, code):
        # 用get方法会抛异常，需要采用以下捕获异常的方式, 使用filter更方便
        # try:
        #     verify_records = VerifyCode.objects.get(mobile=self.initial_data["username"]).order_by("-add_time") #前端传过来的user
        # except VerifyCode.DoesNotExist as e:
        #     pass
        # except VerifyCode.MultipleObjectsReturned as e:
        #     pass

        verify_code_records = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by("-add_time") #前端传过来的user
        if verify_code_records:
            last_record = verify_code_records[0]
            five_minute_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_minute_ago < last_record.add_time:
                raise serializers.ValidationError("验证码过期")
            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")
        else
            raise serializers.ValidationError("验证码错误")


    class Meta:
        model = User
        fields = ("username", "code")