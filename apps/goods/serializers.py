# _*_ encoding:utf-8 _*_
__author__ = 'taylor lee'


from rest_framework import serializers


from goods.models import Goods, GoodsCategory


class GoodsCategorySerializer3(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = '__all__' # 取所有字段


class GoodsCategorySerializer2(serializers.ModelSerializer):
    sub_cat = GoodsCategorySerializer3(many=True)
    class Meta:
        model = GoodsCategory
        fields = '__all__' # 取所有字段


class GoodsCategorySerializer(serializers.ModelSerializer):
    # sub_cat在parent_category中为related_name，作为关联
    sub_cat = GoodsCategorySerializer2(many=True) # 一定要加上many=True，来获取所有子级分类
    class Meta:
        model = GoodsCategory
        fields = '__all__' # 取所有字段


class GoodsSerializer(serializers.ModelSerializer):
    category = GoodsCategorySerializer()
    class Meta:
        model = Goods
        fields = '__all__' # 取所有字段
        # fields = ('name', 'click_num', 'market_price', 'add_time')