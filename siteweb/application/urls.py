from django.urls import path
from . import views

urlpatterns = [
    path('', views.worm, name='worm'),
    path('servers/', views.servers, name='servers'),
    path('server/', views.server, name='server'),

    path('persons/', views.persons, name='persons'),
    path('person/', views.person, name='person'),
]