import json

from django.shortcuts import render, get_object_or_404, redirect
from blog_project.models import Post, Reader

from comments.models import Comment


def post_comment(request,post_pk):
    if request.session.get('login_user'):
        login_user = json.loads(request.session.get('login_user'))
        reader = Reader.objects.filter(id=login_user['id']).first()
        # 先获取被评论的文章，因为后面需要把评论和被评论的文章关联起来。
        # 这里我们使用了 Django 提供的一个快捷函数 get_object_or_404，
        # 这个函数的作用是当获取的文章（Post）存在时，则获取；否则返回 404 页面给用户。
        post = get_object_or_404(Post, pk=post_pk)
        # HTTP 请求有 get 和 post 两种，一般用户通过表单提交数据都是通过 post 请求，
        # 因此只有当用户的请求为 post 时才需要处理表单数据。
        if request.method == 'POST':
            text = request.POST.get('text')
            comment = Comment(post=post,reader=reader,text=text)
            comment.save()
                # 重定向到 post 的详情页，实际上当 redirect 函数接收一个模型的实例时，它会调用这个模型实例的 get_absolute_url 方法，
                # 然后重定向到 get_absolute_url 方法返回的 URL。
            return redirect(post)
        # 不是 post 请求，说明用户没有提交数据，重定向到文章详情页。
        return redirect(post)