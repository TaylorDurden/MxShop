# _*_ encoding:utf-8 _*_
from datetime import datetime

from django.db import models
from DjangoUeditor.models import UEditorField

# Create your models here.


class GoodsCategory(models.Model):
    """
    商品类别
    """
    CATEGORY_TYPE = (
        (1, "一级类目"),
        (2, "二级类目"),
        (3, "三级类目"),
    )

    name = models.CharField(default="", max_length=30, verbose_name=u"类别名", help_text=u"类别名")
    code = models.CharField(default="", max_length=30, verbose_name=u"类别code", help_text=u"类别code")
    desc = models.CharField(default="", max_length=30, verbose_name=u"类别描述", help_text=u"类别描述")
    category_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name=u"类目级别", help_text=u"类目级别")
    # 父类指向自己这张表
    parent_category = models.ForeignKey("self", null=True, blank=True, verbose_name=u"父级类目",
                                        related_name="sub_cat")  # related_name查询可以用到
    # 是否放置到首页的header的tabs中
    is_tab = models.BooleanField(default=False, verbose_name=u"是否导航", help_text="是否导航")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"商品类别"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsCategoryBrand(models.Model):
    """
    品牌名
    """
    category = models.ForeignKey(GoodsCategory, null=True, blank=True, verbose_name=u"商品分类")
    name = models.CharField(default="", max_length=30, verbose_name=u"品牌名", help_text=u"品牌名")
    desc = models.TextField(default="", max_length=200, verbose_name=u"品牌描述", help_text=u"品牌描述")
    image = models.ImageField(max_length=200, upload_to="brands/")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"品牌"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Goods(models.Model):
    """
    商品
    """
    category = models.ForeignKey(GoodsCategory, null=True, blank=True, verbose_name=u"商品分类", help_text=u"商品分类")
    goods_sn = models.CharField(max_length=50, default="", verbose_name=u"商品唯一货号")
    name = models.CharField(max_length=300, verbose_name=u"商品名称")
    goods_num = models.IntegerField(default=0, verbose_name=u"商品数量")
    click_num = models.IntegerField(default=0, verbose_name=u"点击数")
    sold_num = models.IntegerField(default=0, verbose_name=u"商品销售量")
    fav_num = models.IntegerField(default=0, verbose_name=u"收藏数")
    market_price = models.FloatField(default=0, verbose_name=u"市场价格")
    shop_price = models.FloatField(default=0, verbose_name=u"本店价格")
    goods_brief = models.TextField(max_length=300, default=0, verbose_name=u"商品简述")
    goods_desc = UEditorField(verbose_name=u"内容", imagePath="goods/images/", width=1000, height=500,
                              filePath="goods/files/", default="")
    # 是否免运费
    ship_free = models.BooleanField(default=True, verbose_name=u"是否承担运费")
    goods_front_image = models.ImageField(max_length=200, upload_to="goods/images/", null=True, blank=True, verbose_name=u"封面图片")
    is_new = models.BooleanField(default=False, verbose_name=u"是否新品")
    is_hot = models.BooleanField(default=False, verbose_name=u"是否热销")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"商品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsImage(models.Model):
    """
    商品轮播图
    """
    goods = models.ForeignKey(Goods, verbose_name=u"商品", related_name="images")
    image = models.ImageField(max_length=200, upload_to="", verbose_name=u"图片", null=True, blank=True)
    #image_url = models.CharField(max_length=300, null=True, blank=True, verbose_name=u"图片url")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"商品图片"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class Banner(models.Model):
    """
    大图轮播的商品图片
    """
    goods = models.ForeignKey(Goods, verbose_name=u"商品")
    image= models.ImageField(max_length=200, upload_to="banner", verbose_name=u"轮播图片")
    index = models.IntegerField(default=0, verbose_name=u"轮播顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"大图轮播商品图片"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name