from django.urls import path
from . import views

urlpatterns = [
    path('', views.worm, name='worm'),
    path('servers/', views.servers, name='servers'),
    path('server/', views.server, name='server'),
]