from django.conf.urls import url

from blog_project import views

app_name = 'blog_project'
urlpatterns = [

    url(r'^$', views.index, name='index'),

    url(r'^post/(?P<pk>[0-9]+)/$', views.detail, name='detail'),

    url(r'archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.archives, name='archives'),

    url(r'category/(?P<pk>[0-9]+)/$', views.category, name='category'),

    url(r'tag/(?P<pk>[0-9]+)/$', views.tag, name='tag'),

    url(r'search/', views.search, name='search'),

    url(r'login/', views.login, name='login'),

    url(r'register/', views.register, name='register'),

    url(r'quit/', views.quit, name='quit'),

    url(r'^upload/', views.upload, name='upload'),

    url(r'^abort/', views.abort, name='abort'),
]