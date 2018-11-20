from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import random
from django_redis import get_redis_connection
from rest_framework import status

from . import constants
from meiduo_mall.libs.yuntongxun.sms import CCP
import logging
from celery_tasks.sms.tasks import send_sms_code


logger = logging.getLogger('django')

# Create your views here.
class SMSCodeView(APIView):
    """发送短信视图"""

    def get(self, request, mobile):
        # 连接redis数据库
        redis_conn = get_redis_connection('verify_codes')

        # 获取短信验证码标记
        send_flag = redis_conn.get('send_flag_%s'% mobile)
        if send_flag:
            return Response({'message': '频繁发送短信'}, status=status.HTTP_400_BAD_REQUEST)
        # 生成短信验证码
        sms_code = '%06d' % random.randint(0, 999999)
        logger.info(sms_code)

        # 创建管道
        pl = redis_conn.pipeline()
        # 存储短信验证码内容到redis数据库  setex(key, 过期时间, value)
        # redis_conn.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        pl.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        # 保存发送短信验证码的标记
        # redis_conn.setex('send_flag_%s' % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)
        pl.setex('send_flag_%s' % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)

        # 执行管道
        pl.execute()

        # 发送短信验证码  send_template_sms(self, to, datas, temp_id)
        # CCP().send_template_sms(mobile, [sms_code, constants.SMS_CODE_REDIS_EXPIRES // 60], 1)
        # celery异步发送短信验证码
        send_sms_code.delay(mobile, sms_code)
        # 响应发送短信验证码结果
        return Response({'message': 'ok'})
