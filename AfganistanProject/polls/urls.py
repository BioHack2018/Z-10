from django.urls import path
from django.conf.urls import url


from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('get_data_from_db', views.get_data_from_db, name='get_data_from_db'),
    path('result', views.result, name='result')
]