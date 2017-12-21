# _*_ encoding:utf-8 _*_
__author__ = 'taylor lee'


import django_filters
from django.db.models import Q


from .models import Goods


class GoodsFilter(django_filters.rest_framework.FilterSet):
    """
    商品的过滤类
    """
    # gte -- >=, lte -- <=
    pricemin = django_filters.NumberFilter(help_text=u"最低价格", name="shop_price", lookup_expr='gte')
    pricemax = django_filters.NumberFilter(name="shop_price", lookup_expr='lte')
    top_category = django_filters.NumberFilter(method='top_category_filter')
    # 名称字段的模糊查询，如果去掉lookup_expr，就会精确查找
    # name = django_filters.CharFilter(name="name", lookup_expr='icontains')

    # 找1级分类下的所有分类, id => value
    def top_category_filter(self, queryset, name, value):
        return queryset.filter(Q(category_id=value)|Q(category__parent_category_id=value)|Q(category__parent_category__parent_category_id=value))

    class Meta:
        model = Goods
        fields = ['pricemin', 'pricemax', 'is_hot']