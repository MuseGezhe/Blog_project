from django.db import models

# 创建评论的模型
from tinymce.models import HTMLField


class Comment(models.Model):

    reader = models.ForeignKey('blog_project.Reader')

    text = HTMLField(null=True)
    # 创建评论的时间，默认成递增
    created_time = models.DateTimeField(auto_now_add=True)
    # 一篇文章会有多条评论，一对多关系
    post = models.ForeignKey('blog_project.Post')

    def __str__(self):
        return self.text[:20]
    class Meta:
        db_table = 'comments'