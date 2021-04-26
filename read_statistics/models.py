from django.db import models
from django.db.models.fields import exceptions
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

class ReadNum(models.Model):
    '''博客的阅读计数模型'''
    read_num = models.IntegerField(default=0, verbose_name='阅读数量')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()   #该字段可以存储您将要关联的模型中的主键值
    content_object = GenericForeignKey('content_type', 'object_id') #向其传递上述两个字段的名称

class ReadNumExpandMethod():
    def get_read_num(self):
        ct = ContentType.objects.get_for_model(self) #获取模型
        try:
            readnum =ReadNum.objects.get(content_type=ct, object_id=self.pk)    #获取哪篇的博客pk
            return readnum.read_num
        except exceptions.ObjectDoesNotExist:
            return 0

class ReadDetail(models.Model):
    date = models.DateField(default=timezone.now)   #DateField只记录到天的时间
    read_num = models.IntegerField(default=0,verbose_name='阅读数量')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()  # 该字段可以存储您将要关联的模型中的主键值
    content_object = GenericForeignKey('content_type', 'object_id') #设置通用的
