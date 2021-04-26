# created by 2021/3/14 10:58
import datetime
from django.core.cache import cache
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from .models import ReadNum,ReadDetail
from blog.models import Blog

def read_statistics_once_read(request, obj):
    #每次阅读数统计
    ct = ContentType.objects.get_for_model(obj)  # 获取模型
    key ="%s_%s_read" %(ct.model, obj.pk)
    #不存在cookie就+1，不存在代表没访问过
    if not request.COOKIES.get(key):
        #get_or_create根据条件获取，没有的话就创建，创建时返回的时一个元组
        #所有的阅读数
        readnum ,created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        readnum.read_num += 1
        readnum.save()
        date = timezone.now().date()
        #当天的阅读数
        readDetail,created = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)
        readDetail.read_num += 1
        readDetail.save()
    #返回key，cookie的键名，需要时候进行创建
    return key

def get_seven_days_read_data(content_type):
    #近一周的博客阅读量
    read_nums = []
    dates =[]
    today = timezone.now().date()
    for i in range(6,-1,-1):    #(6,-1,-1)
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))    #日期转换字符串并格式化取月日
        read_details = ReadDetail.objects.filter(content_type=content_type,date=date)
        result = read_details.aggregate(read_num_sum = Sum('read_num'))        #聚合运算，求和，总的
        read_nums.append(result['read_num_sum'] or 0)
    return  dates,read_nums

def get_today_hot_data(content_type):
    #今天的热门博客阅读数排行
    today = timezone.now().date()
    read_details = ReadDetail.objects.filter(content_type=content_type,date=today).order_by('-read_num') #阅读数倒序
    return read_details[:5]

def get_yesterday_hot_data(content_type):
    #昨天的热门博客
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)  #days=1一天时间
    read_details = ReadDetail.objects.filter(content_type=content_type,date=yesterday).order_by('-read_num')
    return read_details[:5]

def get_7_days_blog_hot():
    # 近7天内的热门博客推荐（阅读数排行）
    today = datetime.date.today()
    date = today - datetime.timedelta(days=7)
    blog = Blog.objects.filter(read_details__date__lte=today,read_details__date__gte=date)\
        .values('id','title')\
        .annotate(read_num_sum=Sum('read_details__read_num'))\
        .order_by('-read_num_sum')
    #分组,values,计数annotate，排序order_by
    return blog[:5]
