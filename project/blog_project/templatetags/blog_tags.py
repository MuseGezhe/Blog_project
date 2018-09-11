
#自定义编写编写模板标签

from django import template
from django.db.models.aggregates import Count

from blog_project.models import Post, Category, Tag

# 实例化一个template.Library类，
register = template.Library()

# 最新文章模板标签，将函数装饰为register.simple_tag,
# 这样就可以在模板中调用这个语法
@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by('-created_time')[:num]

# 归档模板标签，将函数装饰为register.simple_tag,
# 这样就可以在模板中调用这个语法
@register.simple_tag
def archives():
    return Post.objects.dates('created_time','month',order='DESC')

# 分类模板标签，将函数装饰为register.simple_tag,
# 这样就可以在模板中调用这个语法
@register.simple_tag
def get_categories():
    return Category.objects.all()

# Count 计算分类下的文章数，其接受的参数为需要计数的模型的名称
@register.simple_tag
def get_categories():
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)

# 统计标签下的文章数
@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)