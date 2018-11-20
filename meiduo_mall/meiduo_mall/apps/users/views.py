from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import CreateUserSerializer
from .models import User


# Create your views here.
# url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view()),
class MobileCountView(APIView):
    """判断手机号是否已存在"""

    def get(self, request, mobile):
        """获取手机号数量"""
        count = User.objects.filter(mobile=mobile).count()

        data = {
            'mobile': mobile,
            'count': count
        }

        return Response(data)

# url(r'^usernames/(?P<username>\w{5,20})/count/$', views.UsernameCountView.as_view()),
class UsernameCountView(APIView):
    """判断用户名是否已存在"""

    def get(self, request, username):
        """获取用户数量"""
        count = User.objects.filter(username=username).count()

        data = {
            'username': username,
            'count': count
        }

        return Response(data)


# url(r'^users/$', views.UserView.as_view()),
class UserView(CreateAPIView):
    """注册视图"""

    # 指定序列化器:剩下的CreateAPIView都做了
    serializer_class = CreateUserSerializer