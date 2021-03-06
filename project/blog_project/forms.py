# 要使用 Django 的表单功能，我们首先导入 forms 模块。

from django import forms

# Django的表单类必须继承自forms.Form类或者forms.ModelForm 类
from blog_project.models import Reader


class RegisterForm(forms.ModelForm):
    class Meta:
        # 表单对应的数据库模型是 Reader 类
        model = Reader
        # 指定了表单需要显示的字段
        fields = ['username','password','phone','photo']