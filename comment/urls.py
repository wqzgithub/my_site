# created by 2021/3/15 21:27
from django.urls import path
from . import views

urlpatterns = [
    path('update_comment/',views.update_comment,name='update_comment'),
]