# _*_ encoding:utf-8 _*_
__author__ = 'taylor lee'

from django.shortcuts import render

# Create your views here.
from .serializers import GoodsSerializer, GoodsCategorySerializer
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import mixins, generics, viewsets, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from .models import Goods, GoodsCategory
from .filters import GoodsFilter


class GoodsPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100

class GoodsListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    商品列表页，单个商品详情，分页，搜索，过滤，排序
    """
    # 在for循环遍历的时候才会查询
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = GoodsFilter
    # authentication_classes = (TokenAuthentication,)
    # =name 是name字段精确搜索
    search_fields = ('name', 'goods_brief', 'goods_desc')
    ordering_fields = ('sold_num', 'shop_price')

    # def get_queryset(self):
    #     price_min = self.request.query_params.get("price_min", 0)
    #     if price_min:
    #         self.queryset = Goods.objects.filter(shop_price__gt=int(price_min))
    #     return self.queryset

    # def get(self, request, format=None):
    #     goods = Goods.objects.all()[:10]
    #     goods_serializer = GoodsSerializer(goods, many=True) # many=True序列化成一个数组对象
    #     return Response(goods_serializer.data)

    # def post(self, request, format=None):
    #     serializer = GoodsSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# mixins.ListModelMixin返回列表数据/categories, mixins.RetrieveModelMixin检索某个数据/categories/:ID
class GoodsCategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        商品分类列表数据
    retrieve:
        获取商品分类详情
    """
    queryset = GoodsCategory.objects.filter(category_type=1) # 取第一级的分类
    serializer_class = GoodsCategorySerializer