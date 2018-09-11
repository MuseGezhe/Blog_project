import markdown
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.html import strip_tags


class Category(models.Model):
    # 分类模型
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'categorys'



class Tag(models.Model):
    # 标签模型
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'tags'

class Post(models.Model):
   #  文章标题
   title = models.CharField(max_length=70)

   # 正文
   body = models.TextField(null=True)

   # 文章创建时间、最后修改时间
   created_time = models.DateTimeField(auto_now_add=True)
   modified_time = models.DateTimeField(auto_now_add=True)

   # 文章摘要
   excerpt = models.CharField(max_length=200,blank=True,null=True)


   # 我们在这里把文章对应的数据库表和分类、标签对应的数据库表关联了起来，但是关联形式稍微有点不同。
   # 我们规定一篇文章只能对应一个分类，但是一个分类下可以有多篇文章，所以我们使用的是 ForeignKey，即一对多的关联关系。
   # 而对于标签来说，一篇文章可以有多个标签，同一个标签下也可能有多篇文章，所以我们使用 ManyToManyField，表明这是多对多的关联关系。
   # 同时我们规定文章可以没有标签，因此为标签 tags 指定了 blank=True。
   category = models.ForeignKey(Category)
   tags = models.ManyToManyField(Tag,blank=True)


   # 文章作者，这里 User 是从 django.contrib.auth.models 导入的。
   # django.contrib.auth 是 Django 内置的应用，专门用于处理网站用户的注册、登录等流程，User 是 Django 为我们已经写好的用户模型。
   # 这里我们通过 ForeignKey 把文章和 User 关联了起来。
   # 因为我们规定一篇文章只能有一个作者，而一个作者可能会写多篇文章，因此这是一对多的关联关系，和 Category 类似。
   author = models.ForeignKey(User)
   # 为了记录文章的浏览量，需要在文章的数据库表中新增一个用于存储阅读量的字段
   views = models.PositiveIntegerField(default=0)

   def __str__(self):
       return self.title

   def get_absolute_url(self):
       return reverse('blog_project:detail', kwargs={'pk': self.pk})

   class Meta:
       db_table = 'posts'
       ordering = ['-created_time']

   # increase_views 方法首先将自身对应的 views 字段的值 +1（此时数据库中的值还没变），
   # 然后调用 save 方法将更改后的值保存到数据库。
   # 注意这里使用了 update_fields 参数来告诉 Django 只更新数据库中 views 字段的值，以提高效率。
   def increase_views(self):
       self.views += 1
       self.save(update_fields=['views'])

   # 自动生成文章摘要
   def save(self,*args,**kwargs):
       # 如果没有填写摘要
       if not self.excerpt:
           # 首先实例化一个 Markdown 类，用于渲染 body 的文本
           md = markdown.Markdown(extensions=[
               'markdown.extensions.extra',
               'markdown.extensions.codehilite',
           ])
           # 先将 Markdown 文本渲染成 HTML 文本
           # strip_tags 去掉 HTML 文本的全部 HTML 标签
           # 从文本摘取前 54 个字符赋给 excerpt
           self.excerpt = strip_tags(md.convert(self.body))[:54]

       # 调用父类的 save 方法将数据保存到数据库中
       super(Post, self).save(*args, **kwargs)


class Reader(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    photo = models.CharField(max_length=100)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'readers'
