# _*_ encoding:utf-8 _*_
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class UserProfile(AbstractUser):
    """
    用户
    """
    # 通过手机注册的可能不填写姓名
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name="姓名")
    birthday = models.CharField(max_length=20 ,null=True, blank=True, verbose_name="出生年月")
    gender = models.CharField(max_length=6, choices=(("male", u"男"), ("female", u"女")), default="male", blank=True,
                              verbose_name="性别")
    mobile = models.CharField(null=True, blank=True, max_length=20, verbose_name=u"电话")
    email = models.CharField(max_length=100, null=True, blank=True, verbose_name=u"邮箱")

    class Meta:
        verbose_name = u"用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class VerifyCode(models.Model):
    """
    短信验证码
    """
    code = models.CharField(max_length=10, verbose_name=u"验证码")
    mobile = models.CharField(max_length=11, verbose_name=u"电话")
    # datetime.now为在记录添加时的时间, datetime.now()为编译时的时间
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"短信验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code
