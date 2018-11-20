# 定义耗时的异步任务
from .yuntongxun.sms import CCP
from . import constants
from celery_tasks.main import celery_app


# 装饰器将send_sms_code 装饰为异步任务,并设置别名
@celery_app.task(name='send_sms_code')
def send_sms_code(mobile, sms_code):
    """
    定义发短信异步任务
    :param mobile: 接收验证码的手机
    :param sms_code:  验证码
    :return: None
    """
    CCP().send_template_sms(mobile, [sms_code, constants.SMS_CODE_REDIS_EXPIRES // 60], constants.SEND_SMS_TEMPLATE_ID)
