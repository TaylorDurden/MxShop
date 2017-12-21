from django.shortcuts import render

# Create your views here.
from random import choice


from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import viewsets, status, mixins, permissions, authentication
from rest_framework.mixins import CreateModelMixin
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


from .serializers import SMSSerializer, UserRegisterSerializer, UserDetailSerializer
from .models import VerifyCode
from utils.yunpian import YunPian
from MxShop.settings import SMS_API_KEY

User = get_user_model()


class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username)|Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewSet(CreateModelMixin, viewsets.GenericViewSet):
    """
    发送短信验证码
    """
    serializer_class = SMSSerializer

    def generate_code(self):
        """
        生成4位数字的验证码
        :return:
        """
        seeds = "123456789"
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))
        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data["mobile"]
        sms = YunPian(SMS_API_KEY)

        code = self.generate_code()
        sms_send_status = sms.send_sms(code=code, mobile=mobile)
        if sms_send_status["code"] != 0: #失败
            return Response({
                "mobile": sms_send_status["detail"]
            }, status=status.HTTP_400_BAD_REQUEST)
        else: #成功
            sms_record = VerifyCode(code=code, mobile=mobile)
            sms_record.save()
            return Response({
                "mobile": mobile
            }, status=status.HTTP_201_CREATED)


class UserViewSet(CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    用户
    """
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    # permission_classes = (permissions.IsAuthenticated, )

    # 动态定义serializer
    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        elif self.action == "create":
            return UserRegisterSerializer

        # 其他情况默认返回Detail
        return UserDetailSerializer

    # 动态定义permission
    def get_permissions(self):
        if self.action == "retrieve":
            return [permissions.IsAuthenticated()]
        elif self.action == "create":
            return []

        return []

    # 重写CreateModelMixin的create方法
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    # 重写CreateModelMixin的perform_create方法
    def perform_create(self, serializer):
        return serializer.save()

    # 重写GenericView的get_object方法来取user, 包含了d字段
    def get_object(self):
        return self.request.user