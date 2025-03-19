from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('posters/', views.posters, name='posters'),
]

     
    
