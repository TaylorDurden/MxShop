from datetime import datetime


from django.db import models
from django.contrib.auth import get_user_model


from goods.models import Goods


User = get_user_model()
# Create your models here.


class UserFav(models.Model):
    user = models.ForeignKey(User, verbose_name=u"用户")
    goods = models.ForeignKey(Goods, verbose_name=u"商品", help_text=u"商品Id")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"用户收藏商品"
        verbose_name_plural = verbose_name
        # 联合唯一索引
        # unique_together = ("user", "goods")

    def __str__(self):
        return self.user.username


class UserLeaveMessage(models.Model):
    """
    用户留言
    """
    MESSAGE_CHOICES = (
        (1, "留言"),
        (2, "投诉"),
        (3, "询问"),
        (4, "售后"),
        (5, "求购")
    )
    user = models.ForeignKey(User, verbose_name=u"用户")
    message_type = models.IntegerField(default=1, choices=MESSAGE_CHOICES, help_text=MESSAGE_CHOICES, verbose_name=u"留言类型")
    subject = models.CharField(max_length=100, default="", verbose_name=u"主题", help_text=u"主题")
    message = models.TextField(default="", verbose_name=u"留言内容", help_text=u"留言内容")
    file = models.FileField(upload_to="message/images", verbose_name=u"上传的文件", help_text=u"上传的文件")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"用户留言"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.message


class UserAddress(models.Model):
    """
    用户收货地址
    """
    user = models.ForeignKey(User, verbose_name=u"用户")
    province = models.CharField(max_length=100, default="", verbose_name=u"省份")
    city = models.CharField(max_length=100, default="", verbose_name=u"城市")
    district = models.CharField(max_length=100, default="", verbose_name=u"区域")
    address = models.CharField(max_length=100, default="", verbose_name=u"详细地址")
    signer_name = models.CharField(max_length=100, default="", verbose_name=u"签收人")
    signer_mobile = models.CharField(max_length=11, default="", verbose_name=u"电话")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"收货地址"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.address