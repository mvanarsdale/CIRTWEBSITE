from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('posters/', views.posters, name='posters'),
    path('FAQ/', views.FAQ, name='FAQ'),
    path('journals/', views.journals, name='journals'),
]

     
    
