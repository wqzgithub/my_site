import threading
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.core.mail import send_mail  #发送邮件
from django.template.loader import render_to_string

class SendMail(threading.Thread):
    #多线程发送邮件
    def __init__(self,subject, text,email,fail_silently=False,):
        self.subject = subject
        self.text = text
        self.email = email
        self.fail_silently = fail_silently
        threading.Thread.__init__(self)
    def run(self):
        send_mail(
            self.subject,
            '',
            settings.EMAIL_HOST_USER,
            [self.email],
            self.fail_silently,
            html_message=self.text)

class Comment(models.Model):
    #评论模型
    #ContentType指向任何类型
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()   #该字段可以存储您将要关联的模型中的主键值
    content_object = GenericForeignKey('content_type', 'object_id') #向其传递上述两个字段的名称
    text =models.TextField()    #评论内容
    comment_time = models.DateTimeField(auto_now_add=True)  #评论时间
    user = models.ForeignKey(User,related_name="comments",on_delete=models.CASCADE)  #评论人
    #回复功能
    root = models.ForeignKey("self",related_name="root_comment",null=True,on_delete=models.CASCADE)
    parent = models.ForeignKey('self',related_name="parent_comment",null=True,on_delete=models.CASCADE)
    reply_to = models.ForeignKey(User,related_name="replies",null=True,on_delete=models.CASCADE)

    def send_email(self):
        if self.parent is None:
            # 评论邮件通知
            subject = '有人评论你的博客'
            email = self.content_object.get_email()
        else:
            # 回复邮件通知
            subject = '有人回复你的评论'
            email = self.reply_to.email
        if email != '':
            context = {}
            context['comment_text'] = self.text
            context['url'] = 'http://127.0.0.1:8000'+self.content_object.get_blog_url()
            text = render_to_string('comment/send_mail.html',context)
            #多线程发送邮件
            send_mail = SendMail(subject, text, email)
            send_mail.start()

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['comment_time']