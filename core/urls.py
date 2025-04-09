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
    path('dashboard/', views.Dashboard, name='dashboard'),
    
    # for user portal view 
    path('Portal/', views.Portal, name='Portal'),
    # for editor portal view 
    path('editPort/', views.editPort, name='editPort'),
    # for reviewer portal view 
    path('reviewPort/', views.reviewPort, name='reviewPort'),
    # for author portal view 
    path('authPort/', views.authPort, name='authPort'),
    
    # for poster submit view 
    path('posterSub/', views.posterSub, name='posterSub'),
    # for journal submit view 
    path('journalSub/', views.journalSub, name='journalSub'),
    
    # for poster submit view 
    path('subComp/', views.subComp, name='subComp'),
    
    # for journal process submit view 
    path('JournalProc/', views.JournalProc, name='JournalProc'),
    
    

   
    # for log in view 
    path('ajax-login/', views.ajax_login, name='ajax_login'),
    # url for signup view 
    path('signup/', views.signup, name='signup'),    
]


     
    
