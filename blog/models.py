from django.db import models
from django.urls import reverse #反向解析
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation  #反向通用关系
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadNumExpandMethod,ReadDetail


class BlogType(models.Model):   #博客的分类类型
    type_name = models.CharField(max_length=15) #文章类型
    def __str__(self):
        #返回博客类型的名字
        return self.type_name

class Blog(models.Model,ReadNumExpandMethod):   #博文模型
    title = models.CharField(verbose_name="标题",max_length=50) #标题
    blog_type = models.ForeignKey(BlogType,on_delete=models.CASCADE,verbose_name='博客类型')
    content = RichTextUploadingField()  # 内容，启用富文本编辑,使用可以上传文件
    author = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='作者')    #作者
    created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建日期')      #创建时间，自动
    last_updated_time = models.DateTimeField(auto_now=True,verbose_name='最后更新日期')      #最后更新时间，自动
    read_details = GenericRelation(ReadDetail)  #反向通用关系,用于获取过去n天内的热本博客的title

    def get_blog_url(self):
        return reverse('blog_detail',args=(self.pk,))

    def get_email(self):
        return self.author.email

    def __str__(self):
        #返回博客的标题
        return "<Blog: %s>" % self.title
    class Meta:
        #分页倒序，访问最新的先
        ordering = ['-created_time']
