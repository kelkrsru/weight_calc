from django.urls import path

from dealcard import views

app_name = 'dealcard'

urlpatterns = [
    path('', views.index, name='index'),
    path('calculate/', views.calculate, name='calculate'),
    path('send-deal/', views.send_deal, name='send-deal'),
]
