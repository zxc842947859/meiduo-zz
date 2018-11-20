from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.
class SMSCodeView(APIView):
    """发送短信视图"""

    def get(self, request, mobile):
        """
        GET /sms_codes/(?P<mobile>1[3-9]\d{9})/
        :param request: Request类型的请求对象
        :param mobile:  手机号
        :return: None
        """
        return Response({'message': 'ok'})
