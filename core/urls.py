from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('posters/', views.posters, name='posters'),
    path('FAQ/', views.FAQ, name='FAQ'),
    path('journals/', views.journals, name='journals'),
    
    path('Dashboard/', views.Dashboard, name='Dashboard'),
    path('Portal/', views.Portal, name='Portal'),
    path('PosterSubmit/', views.PosterSubmit, name='PosterSubmit'),
    
    path('ajax-login/', views.ajax_login, name='ajax_login'),
    
    path('signup/', views.signup, name='signup'),
]


     
    
