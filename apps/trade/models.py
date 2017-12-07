# _*_ encoding:utf-8 _*_
from datetime import datetime


from django.db import models
from django.contrib.auth import get_user_model
from goods.models import Goods


User = get_user_model()
# Create your models here.


class ShoppingCart(models.Model):
    """
    购物车
    """
    user = models.ForeignKey(User, verbose_name=u"用户")
    goods = models.ForeignKey(Goods, verbose_name=u"商品")
    good_num = models.IntegerField(default=0, verbose_name=u"购买数量")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"购物车"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s(%d)".format(self.goods.name, self.good_num)


class OrderInfo(models.Model):
    """
    订单
    """

    PAY_STATUS = (
        ("success", "成功"),
        ("cancel", "取消"),
        ("pending", "待支付")
    )
    PAY_TYPE = (
        ("alipay", "支付宝"),
        ("wechat", "微信")
    )

    user = models.ForeignKey(User, verbose_name=u"用户")
    order_sn = models.CharField(max_length=30, verbose_name=u"订单号")
    trade_no = models.CharField(max_length=100, null=True, blank=True, verbose_name=u"交易号")
    post_script = models.CharField(max_length=200, verbose_name=u"订单留言")
    pay_status = models.CharField(choices=PAY_STATUS, max_length=10, verbose_name=u"支付状态")
    order_amount = models.CharField(max_length=50, default=0.0, verbose_name=u"订单金额")
    pay_time = models.DateTimeField(null=True, blank=True, verbose_name=u"支付金额")

    # 用户信息
    address = models.CharField(max_length=100, default="", verbose_name=u"收货地址")
    sign_name = models.CharField(max_length=20, default="", verbose_name=u"签收人")
    signer_mobile = models.CharField(max_length=11, verbose_name=u"联系电话")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"订单商品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order_sn)


class OrderGoods(models.Model):
    """
    订单的商品详情
    """
    order = models.ForeignKey(OrderInfo, verbose_name=u"订单信息")
    goods = models.ForeignKey(Goods, verbose_name=u"商品")
    goods_num = models.IntegerField(default=0, verbose_name=u"商品数量")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"订单商品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order.order_sn)