# _*_ encoding:utf-8 _*_
"""MxShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
# from django.contrib import admin
import xadmin

from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token

# 处理静态图片 start
from MxShop.settings import MEDIA_ROOT
from django.views.static import serve
# 处理静态图片 end

from goods.views import GoodsListViewSet, GoodsCategoryViewSet
from users.views import SmsCodeViewSet, UserViewSet
from user_operation.views import UserFavViewSet, LeavingMessageViewSet, AddressViewSet


router = DefaultRouter()
# 配置goods的url
router.register(r'goods', GoodsListViewSet, base_name="goods")

# 配置goods categories的url
router.register(r'categories', GoodsCategoryViewSet, base_name="categories")

# 注册发送短信url
router.register(r'codes', SmsCodeViewSet, base_name="codes")

#
router.register(r'users', UserViewSet, base_name="users")

# 收藏
router.register(r'userfavs', UserFavViewSet, base_name="userfavs")

# 用户留言
router.register(r'messages', LeavingMessageViewSet, base_name="messages")

# 用户收货地址
router.register(r'address', AddressViewSet, base_name="address")


# router.register(r'hotsearchs', , base_name="categories")

# goods_list = GoodsListViewSet.as_view({
#     'get': 'list',
#     # 'post': 'create'
# })


urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # 处理静态图片url
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    # 商品列表页
    url(r"^", include(router.urls)),

    url(r'^docs/', include_docs_urls(title="慕学生鲜"), name=""),

    # drf自带的token认证模式
    url(r'^api-token-auth/', views.obtain_auth_token),

    # django jwt 认证模式
    url(r'^login/', obtain_jwt_token),
]
