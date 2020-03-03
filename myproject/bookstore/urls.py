from django.conf.urls import url
from . import views
from . import views_book
from . import views_sysinfo

urlpatterns = [
    #########################图书信息#####################
    # url(r'test', views.test),
    url(r'books', views_book.query),
    url(r'book/edit', views_book.edit),
    #支持url参数的写法一
    #url(r'^book/(\d+)$', views_book.queryOneBook),
    #支持url参数的写法二，变量名称bookId需要跟方法参数名对应
    url(r'^book/(?P<bookId>\d+)$', views_book.queryOneBook),
    url(r'book/del/(?P<bookId>\d+)$', views_book.delBook),
    url(r'book/add', views_book.addBook),

    #########################系统监控信息#########################
    url(r'sys/cntByCountry', views_sysinfo.listContries),
    url(r'sys/cntByCategory', views_sysinfo.countBookByCategory),

    #默认匹配
    url(r'', views.index),
]