# created by 2021/3/7 16:50
from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Q

from read_statistics.utils import get_seven_days_read_data,get_today_hot_data,\
    get_yesterday_hot_data,get_7_days_blog_hot
from blog.models import Blog

def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates,read_nums = get_seven_days_read_data(blog_content_type)

    #获取7天内的博客热度的数据缓存
    # key应该是str，并且value可以是任何可挑选的Python对象。
    # 该timeout参数是可选的，默认为timeout在适当的后端的参数CACHES设置）。
    # 这是该值应存储在缓存中的秒数。
    # 传递 Nonefortimeout将永远缓存该值。
    # 一个timeout的0 将不缓存值。
    # 如果对象在缓存中不存在，
    # 则cache.get()返回None：
    hot_blogs_for_7_days = cache.get('hot_blogs_for_7_days')
    if hot_blogs_for_7_days is None:
        hot_blogs_for_7_days = get_7_days_blog_hot()
        cache.set('hot_blogs_for_7_days', hot_blogs_for_7_days, 30*60)  #缓存存在30分钟

    context = {}
    context['read_nums'] = read_nums
    context['dates'] = dates
    context['today_hot_data'] = get_today_hot_data(blog_content_type)
    context['yesterday_hot_data'] = get_yesterday_hot_data(blog_content_type)
    context['hot_blogs_for_7_days'] = hot_blogs_for_7_days
    return render(request,'home.html',context)

def search(request):
    search_words = request.GET.get('wd','')
    #分词：按空格 & | ~
    condition = None
    for word in  search_words.split(' '):
        if condition is None:
            condition = Q(title__icontains=word)
        else:
            condition = condition | Q(title__icontains=word)

    search_blogs =[]
    if condition:
        #筛选：搜索
        search_blogs = Blog.objects.filter(condition) #包含搜索

    #分页
    paginator = Paginator(search_blogs, 10)  # 每10个一页，进行分页操作，
    page_num = request.GET.get('page', 1)  # 获取url的当前页面页码参数的（GET请求），没有的话获取默认1
    page_of_blogs = paginator.get_page(page_num)  # get_page会自动识别当前页码，如果输入的页码不规范，则会默认返回第一页

    context ={}
    context['search_words'] = search_words
    context['search_blogs_count'] = search_blogs.count()
    context['page_of_blogs'] = page_of_blogs
    return render(request,'search.html', context)


