from django.shortcuts import get_object_or_404,render
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Count
from read_statistics.utils import read_statistics_once_read
from .models import Blog,BlogType

#分页的每页文章数量
each_page_blogs_number= settings.EACH_PAGE_BLOGS_NUMBER

def get_blog_list_common_date(request,blogs_all_list):    #获取博客共同的数据
    #分页器设计
    paginator = Paginator(blogs_all_list, each_page_blogs_number)  # 每10个一页，进行分页操作，
    page_num = request.GET.get('page', 1)  # 获取url的当前页面页码参数的（GET请求），没有的话获取默认1
    page_of_blogs = paginator.get_page(page_num)  # get_page会自动识别当前页码，如果输入的页码不规范，则会默认返回第一页
    currentr_page_num = page_of_blogs.number  # 获取当前页码
    # 前端分页组件设计算法，显示分页列表的范围，获取当前页面以及前后两页
    page_range = list(range(max(currentr_page_num - 2, 1), currentr_page_num)) + \
                 list(range(currentr_page_num, min(currentr_page_num + 2,
                                                   paginator.num_pages) + 1))
    # 分页组件加上省略号标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    #获取日期归档对应的博客数量
    blog_dates = Blog.objects.dates('created_time', 'month', order='DESC')
    blog_dates_dict = {}
    for blog_date in blog_dates:
        # 每年月时间的博客数量,加到对应对象的类型属性上
        blog_count = Blog.objects.filter(created_time__year=blog_date.year,
                            created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count

    context = {}
    context['blogs'] = page_of_blogs.object_list  # 返回指定具体的页(当前)的博客
    context['page_of_blogs'] = page_of_blogs
    context['blogs_all_count'] = Blog.objects.all().count()  # 统计所以博客数量，用于前端统计
    context['page_range'] = page_range
    # 获取博客分类对应的博客数量,Count('blog')关联Blog模型
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
    # 得到相关日期的列表，用于日期面板，返回的blog_dates_dict是一个字典
    context['blog_dates'] = blog_dates_dict
    return context

def blog_list(request):
    """用于显示博客列表"""
    blogs_all_list = Blog.objects.all() #获取所有的博客的博客列表
    context =get_blog_list_common_date(request,blogs_all_list)   #调用公共通用的函数方法
    return render(request,'blog/blog_list.html', context)

def blogs_with_type(request,blog_type_pk):
    """用于点击随笔等类型就显示该类型的文章"""
    blog_type = get_object_or_404(BlogType,pk=blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)  # 获取指定类型的博客的博客列表
    context = get_blog_list_common_date(request, blogs_all_list)     #调用公共的函数方法
    context['blog_type'] = blog_type
    return render(request,'blog/blogs_with_type.html', context)

def blogs_with_date(request,year,month):
    """用于点击日期分类显示该年月发表的blog文章"""
    # 获取指定类型的博客的博客列表
    blogs_all_list = Blog.objects.filter(created_time__year=year,created_time__month=month)
    context = get_blog_list_common_date(request, blogs_all_list)    #调用公共的函数方法
    context['blogs_with_date'] = '%s年%s月' %(year,month)
    return render(request,'blog/blogs_with_date.html', context)

def blog_detail(request,blog_pk):
    """用于显示博客文章"""
    blog = get_object_or_404(Blog,pk=blog_pk)
    read_cookie_key = read_statistics_once_read(request,blog)
    context = {}
    # 上一篇下一篇博客参数previous_blog,next_blog
    # 上一条博客。查询大于当前时间的最后一条
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    # 下一条博客，小于当前时间的第一条
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    context['blog'] = blog
    context['user'] = request.user
    response = render(request,'blog/blog_detail.html', context) #响应
    response.set_cookie(read_cookie_key,'true') #阅读cookie标记
    return response


