"""
Django settings for my_site project.

Generated by 'django-admin startproject' using Django 2.0.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""
from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
DATABASE_PASSWORD = os.environ['DATABASE_PASSWORD']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'my_site_db',
        'USER': 'wqz',
        'PASSWORD': DATABASE_PASSWORD,
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

#发送邮件设置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'wqz_blog@qq.com'    #发送人
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']    #授权码
#EMAIL_USE_TLS = True    #与SMTP服务器通信时是否使用TLS（安全）连接
EMAIL_USE_SSL = True    #与SMTP服务器通信时是否使用TLS（安全）连接，465端口需要
EMAIL_SUBJECT_PREFIX = '[wqz的博客]'   #发送的电子邮件的主题行前缀