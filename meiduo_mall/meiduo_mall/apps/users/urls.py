from django.conf.urls import url

from . import views

urlpatterns = [
    # 用户注册
    url(r'^users/$', views.UserView.as_view()),
    # 判断用户是否已存在
    url(r'^usernames/(?P<username>\w{5,20})/count/$', views.UsernameCountView.as_view()),
    # 判断手机号是否已存在
    url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view()),
]
