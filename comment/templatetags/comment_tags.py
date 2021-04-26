# created by 2021/3/30 16:24
#自定义模板标签
from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import Comment
from ..forms import CommentForm


register = template.Library()
@register.simple_tag
def get_comment_count(obj):
    #获取对应博客的评论
    #饭返回博客屁评论数
    content_type = ContentType.objects.get_for_model(obj)
    return Comment.objects.filter(content_type=content_type, object_id=obj.pk).count()

@register.simple_tag
def get_comment_form(obj):
    #评论表单，用于用户评论
    content_type = ContentType.objects.get_for_model(obj)
    # 初始化评论表单)
    form = CommentForm(initial={
            'content_type':content_type.model,
            'object_id': obj.pk,
            'reply_comment_id':0})
    return form

@register.simple_tag
def get_comment_list(obj):
    # 对应博客的所有评论,并进行评论时间排序
    content_type = ContentType.objects.get_for_model(obj)
    comments = Comment.objects.filter(content_type=content_type, object_id=obj.pk, parent=None)
    return comments.order_by('-comment_time')