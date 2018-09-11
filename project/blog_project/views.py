import json

import markdown
import os
import uuid

from blog_project.forms import RegisterForm
from project import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify

from blog_project.models import Post, Category, Tag, Reader
from comments.forms import CommentForm
from utils import mvImageFromTmp

def login(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('pwd')

        reader = Reader.objects.filter(username=username)

        if reader.exists():
            user = reader.first()

            if password == user.password:
                login_user = json.dumps({'id':user.id,
                                         'name': user.username,
                                         'photo': user.photo})

                request.session['login_user'] = login_user

                return redirect('/')
            else:
                error_msg = '用户名或者密码错误'
        else:
            error_msg = '用户%s不存在，请先注册！' %username

    return render(request,'login.html',locals())

def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():

            user = form.save()

            # 清除上传图片的临时目录
            photo = request.POST.get('photo')
            if photo:
                mvFilePath = mvImageFromTmp(photo)
                print(mvFilePath)
                user.photo = mvFilePath
                user.save()  # 更新目录

            # 将当前注册成功的用户名和id写入到session中
            request.session['login_user'] = json.dumps({'id': user.id,
                                                        'name': user.username,
                                                        'photo': user.photo})

            return redirect('/login/')  # 重定向到主页
        else:
            return render(request,'register.html',locals())
            # locals() 收集当前函数内部的可用对象，生成dict字典

def quit(request):
    request.session.clear()
    return redirect('/login/')

@csrf_exempt
def upload(request):

    # 获取上传的图片
    uImage: InMemoryUploadedFile = request.FILES.get('u_img')

    # 生成新的文件名
    imgFileName = str(uuid.uuid4()).replace('-', '') + os.path.splitext(uImage.name)[-1]

    # 指定新的文件保存的位置
    imgFilePath = os.path.join(settings.MEDIA_ROOT, 'user/' + imgFileName)

    with open(imgFilePath, 'wb') as f:
        # 按上传文件的段，写入到新的文件中
        for chunk in uImage.chunks():
            f.write(chunk)

    return JsonResponse({'path': '/static/uploads/user/' + imgFileName,
                         'status': 'ok'})



# 分页处理并展示主页
def index(request):
    if request.session.get('login_user'):
        login_user = json.loads(request.session.get('login_user'))

    post_list = Post.objects.all()
    post_paginator = Paginator(post_list,6)
    page = request.GET.get('page')
    try:
        posts = post_paginator.page(page)
    # 如果用户请求的页码号不是整数，显示第一页
    except PageNotAnInteger:
        posts = post_paginator.page(1)
    # 如果用户请求的页码号超过了最大页码号，显示最后一页
    except EmptyPage:
        posts = post_paginator.page(post_paginator.num_pages)
    return render(request, 'index.html', locals())

def detail(request,pk):
    # get_object_or_404 函数，其作用是如果用户访问的文章不存在，则返回一个 404 错误页面以提示用户访问的资源不存在
    # 相当于 post = Post.objects.get(pk=pk) 不存在文章返回404
    if request.session.get('login_user'):
        login_user = json.loads(request.session.get('login_user'))
    post = get_object_or_404(Post,pk=pk)

    # 当请求文章详情页时，调用模型中定义的函数，即阅读量+1
    post.increase_views()

    md = markdown.Markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      # 美化标题的锚点 URL
                                      # http://127.0.0.1:8000/post/8/#_1  转化为下面的样子
                                      # http://127.0.0.1:8000/post/8/#我是标题一
                                      TocExtension(slugify=slugify),
                                  ])
    post.body = md.convert(post.body)
    post.toc = md.toc

    form = CommentForm()
    # 获取这篇文章下的所有评论
    # comment_list = Comment.objects.filter(post=post)
    comment_list = post.comment_set.all()

    # 将文章，表单，以及文章下的评论列表作为模板变量传给detail.html
    return render(request, 'detail.html', locals())

# 显示指定的日期下的归档文章
def archives(request,year,month):

    # created_time 是 Python 的 date 对象，其有一个 year 和 month 属性
    # Python 中类实例调用属性的方法通常是 created_time.year，但是由于这里作为函数的参数列表，
    # Django 要求我们把点替换成了两个下划线，即 created_time__year

    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    )
    return render(request, 'index.html', {'post_list':post_list})

# 分类页面
def category(request,pk):
    # get_object_or_404 函数，其作用是如果用户访问的分类不存在，则返回一个 404 错误页面以提示用户访问的资源不存在
    # 相当于cate = Category.objects.get(pk=pk) 不存在返回404页面
    if request.session.get('login_user'):
        login_user = json.loads(request.session.get('login_user'))
    cate = get_object_or_404(Category,pk=pk)
    post_list = Post.objects.filter(category=cate)
    return render(request, 'category.html', locals())

# 在文章详情页设置标签，并能统计各标签的文章个数
def tag(request,pk):
    if request.session.get('login_user'):
        login_user = json.loads(request.session.get('login_user'))
    tag = get_object_or_404(Tag,pk=pk)
    post_list = Post.objects.filter(tags=tag)
    return render(request, 'category.html', locals())

# 查找含有搜索关键词的文章
def search(request):
    if request.session.get('login_user'):
        login_user = json.loads(request.session.get('login_user'))
    q = request.GET.get('q')
    key = ''
    if not q:
        key = '请输入关键词'
        return render(request, 'category.html', {'key':key})
    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'category.html', locals())

def abort(request):
    if request.session.get('login_user'):
        login_user = json.loads(request.session.get('login_user'))
    return render(request,'abort.html',locals())



