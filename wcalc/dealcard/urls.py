from django.urls import path
from dealcard import views

app_name = 'dealcard'

urlpatterns = [
    path('', views.index, name='index'),
]