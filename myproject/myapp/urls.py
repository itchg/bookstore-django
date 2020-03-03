from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'test', views.test),
    url(r'moment/input', views.moments_imput),
    url(r'', views.index),
]