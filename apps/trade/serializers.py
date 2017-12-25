# _*_ encoding:utf-8 _*_
__author__ = 'taylor lee'


from rest_framework import serializers


from goods.models import Goods
from .models import ShoppingCart
from goods.serializers import GoodsSerializer


class ShoppingCartDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)
    class Meta:
        model = ShoppingCart
        fields = "__all__"


# serializers.Serializer的灵活性比ModelSerializer的灵活性强，例如对已经加入到购物车的商品进行数量的增加，
# ModelSerializer会验证user和goods的唯一性同时会抛出异常（即使重写了create方法），Serializer则不会进行验证
class ShoppingCartSerializer(serializers.Serializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    nums = serializers.IntegerField(required=True, min_value=1,
                                    error_messages={
                                        "min_value": "商品数量最小为1",
                                        "required": "请选择购买数量"
                                    })
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all())


    def create(self, validated_data):
        user = self.context["request"].user
        nums = validated_data["nums"]
        goods = validated_data["goods"]

        existed = ShoppingCart.objects.filter(user=user, goods=goods)

        if existed:
            existed = existed[0]
            existed.nums += nums
            existed.save()
        else:
            existed = ShoppingCart.objects.create(**validated_data)

        return existed

    def update(self, instance, validated_data):
        # 修改商品数量
        instance.nums = validated_data["nums"]
        instance.save()
        return instance

    # class Meta:
    #     model = ""
    #     validator = ""