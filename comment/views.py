from django.urls import reverse #反向解析
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from .models import Comment
from .forms import CommentForm


def update_comment(request):
    referer = request.META.get('HTTP_REFERER', reverse('home'))  # 请求头的本来的网址
    comment_form = CommentForm(request.POST,user=request.user)
    data ={}
    if comment_form.is_valid():
        comment = Comment()
        comment.user = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']
        #判断是否回复
        parent = comment_form.cleaned_data['parent']
        if parent:
            #确认root是根评论还是子评论
            comment.root = parent.root if not parent.root is None else parent
            comment.parent = parent
            comment.reply_to = parent.user
        comment.save()

        #发送邮件通知
        comment.send_email()

        #返回数据到前端ajax
        data['status'] = 'SUCCESS'
        data['username'] = comment.user.get_nickname_or_username()
        data['comment_time'] = comment.comment_time.timestamp()
        data['text'] = comment.text
        data['content_type'] = ContentType.objects.get_for_model(comment).model
        # 判断是否回复
        if not parent is None:
            data['reply_to'] = comment.reply_to.get_nickname_or_username()
        else:
            data['reply_to'] = ''
        data['pk'] = comment.pk
        data['root_pk'] = comment.root.pk if not comment.root is None else ''

    else:
        data['status'] = 'ERROR'
        data['message'] = list(comment_form.errors.values())[0][0]
    return JsonResponse(data)