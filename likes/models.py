from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

class LikeCount(models.Model):
    #点赞数
    liked_num = models.IntegerField(default=0)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()  # 该字段可以存储您将要关联的模型中的主键值
    content_object = GenericForeignKey('content_type', 'object_id')  # 向其传递上述两个字段的名称

class LikeRecord(models.Model):
    #点赞对象
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 点赞对象
    like_time = models.DateTimeField(auto_now_add=True)         #点赞时间
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()  # 该字段可以存储您将要关联的模型中的主键值
    content_object = GenericForeignKey('content_type', 'object_id')  # 向其传递上述两个字段的名称