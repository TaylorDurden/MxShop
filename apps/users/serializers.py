# _*_ encoding:utf-8 _*_
__author__ = 'taylor lee'
import re  # 正则表达式模块
from datetime import datetime, timedelta

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
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


class UserRegisterSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True,
                                 max_length=4,
                                 min_length=4,
                                 error_messages={
                                     "required": "请输入验证码字段",
                                     "blank": "请输入验证码",
                                     "max_length": "验证码格式错误",
                                     "min_length": "验证码格式错误"
                                 },
                                 help_text=u"验证码",
                                 write_only=True,
                                 label=u"验证码")
    username = serializers.CharField(label=u"用户名", required=True, allow_blank=False, validators=[UniqueValidator(queryset=User.objects.all(), message=u"用户名已存在")])
    password = serializers.CharField(write_only=True, label=u"密码", style={'input_type': 'password'})

    # 在新增用户时，将密码字段进行加密, 可以用来自定义创建，这里可以使用signals文件里的信号量创建来代替
    def create(self, validated_data):
        user = super(UserRegisterSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    def validate_code(self, code):
        # 用get方法会抛异常，需要采用以下捕获异常的方式, 使用filter更方便
        # try:
        #     verify_records = VerifyCode.objects.get(mobile=self.initial_data["username"]).order_by("-add_time") #前端传过来的user
        # except VerifyCode.DoesNotExist as e:
        #     pass
        # except VerifyCode.MultipleObjectsReturned as e:
        #     pass

        verify_code_records = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by(
            "-add_time")  # 前端传过来的user
        if verify_code_records:
            last_record = verify_code_records[0]
            five_minute_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_minute_ago > last_record.add_time:
                raise serializers.ValidationError("验证码过期")
            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")
        else:
            raise serializers.ValidationError("验证码错误")

    # 此方法最后会对所有的验证进行处理，attrs集合中包含了所有验证的字段
    def validate(self, attrs):
        attrs["mobile"] = attrs["username"]
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        fields = ("username", "code", "mobile", "password")
