from django.urls import path
from . import views

urlpatterns = [
    # for default / homepage (index) view
    path('', views.index, name='index'),
    # for poster view
    path('posters/', views.posters, name='posters'),
    # for faq view
    path('FAQ/', views.FAQ, name='FAQ'),
    # for journal view
    path('journals/', views.journals, name='journals'),
    # for dashboard view 
    path('Dashboard/', views.Dashboard, name='Dashboard'),
    # for user portal view 
    path('Portal/', views.Portal, name='Portal'),
    # for poster submit view 
    path('PosterSubmit/', views.PosterSubmit, name='PosterSubmit'),
    # for log in view 
    path('ajax-login/', views.ajax_login, name='ajax_login'),
    # url for signup view 
    path('signup/', views.signup, name='signup'),    
]


     
    
