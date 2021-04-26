# created by 2021/3/31 0:18
from django.urls import path
from . import views

urlpatterns = [
    path('like_change',views.like_change,name='like_change'),
]