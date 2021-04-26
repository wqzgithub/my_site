from django.contrib import admin
from .models import BlogType,Blog

@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ("id","type_name")
    ordering = ("id",)  # 元组，留一个逗号，-id是倒序,后台显示博客类型得序号

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("id","title","blog_type","author","get_read_num"
                    ,"created_time","last_updated_time")